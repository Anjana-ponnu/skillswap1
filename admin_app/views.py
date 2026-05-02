from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Avg, Count
from django.contrib import messages
from .models import AdminProfile
from user_app.models import Registration ,Session,Review # admin & user stored here


def admin_index(request):
    if not request.session.get("is_admin"):
        return redirect("auth")

    # dummy data
    context = {
        "admin_user": {"name": request.session.get("u_name", "Admin")},
        "total_users": Registration.objects.count(),
        "recent_activities": ["User John registered", "User Alice registered"],
        "popular_skills": [{"name": "Python", "count": 10}]
    }
    return render(request, "admin_index.html", context)



def admin_users(request): 
    users = Registration.objects.all()  # Fetch all users
    return render(request, 'admin_users.html', {'users': users})

def admin_skills(request):
    users = Registration.objects.all()
    skills_data = {}

    for user in users:
        # Offered skills
        if user.skills_offered:
            for skill in [s.strip() for s in user.skills_offered.split(",") if s.strip()]:
                if skill not in skills_data:
                    skills_data[skill] = {"offered_by": [], "needed_by": []}
                skills_data[skill]["offered_by"].append(user.name)

        # Needed skills
        if user.skills_needed:
            for skill in [s.strip() for s in user.skills_needed.split(",") if s.strip()]:
                if skill not in skills_data:
                    skills_data[skill] = {"offered_by": [], "needed_by": []}
                skills_data[skill]["needed_by"].append(user.name)

    # Convert to list for easy looping
    all_skills = []
    for skill, info in skills_data.items():
        all_skills.append({
            "name": skill,
            "offered_by": info["offered_by"],
            "needed_by": info["needed_by"],
            "offered_count": len(info["offered_by"]),
            "needed_count": len(info["needed_by"]),
        })

    return render(request, "admin_skills.html", {"skills": all_skills})

def admin_sessions(request):
    sessions = Session.objects.all()  # Replace with your actual model name
    return render(request, "admin_sessions.html", {"sessions": sessions})


def admin_reviews(request):
    reviews = Review.objects.all().order_by("-date_submitted")
    return render(request, "admin_reviews.html", {"reviews": reviews})

def admin_analytics(request):
    total_users = Registration.objects.count()
    total_sessions = Session.objects.count()
    total_reviews = Review.objects.count()
    average_rating = Review.objects.aggregate(Avg("rating"))["rating__avg"]

    context = {
        "total_users": total_users,
        "total_sessions": total_sessions,
        "total_reviews": total_reviews,
        "average_rating": round(average_rating or 0, 2),
    }
    return render(request, "admin_analytics.html", context)

def admin_settings(request):
    admin = AdminProfile.objects.first()  # fetch admin details from DB
    return render(request, 'admin_settings.html', {'admin': admin})

def edit_profile(request):
    # Get the admin profile (first record)
    admin = AdminProfile.objects.first()

    # If no admin exists, create a default one
    if admin is None:
        admin = AdminProfile.objects.create(
            name="Admin User",
            email="admin@skillswap.com",
            role="Administrator",
            password="admin123"
        )

    if request.method == "POST":
        admin.name = request.POST.get("name")
        admin.email = request.POST.get("email")
        admin.role = request.POST.get("role", admin.role)
        admin.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("admin_settings")

    return render(request, "edit_profile.html", {"admin": admin})


def change_password(request):
    admin = AdminProfile.objects.first()
    if request.method == 'POST':
        new_pass = request.POST.get('new_password')
        admin.password = new_pass
        admin.save()
        messages.success(request, "Password changed successfully!")
        return redirect('admin_settings')
    return render(request, 'change_password.html', {'admin': admin})

def logout(request):
    # Clear the session
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect("auth")



def edit_user(request, user_id):
    user = get_object_or_404(Registration, id=user_id)

    if request.method == "POST":
        user.name = request.POST.get("name")
        user.email = request.POST.get("email")
        user.phone_no = request.POST.get("phone_no")
        user.skills_offered = request.POST.get("skills_offered")
        user.skills_needed = request.POST.get("skills_needed")
        user.save()
        return redirect('admin_users')

    return render(request, 'edit_user.html', {'user': user})


def delete_user(request, user_id):
    user = get_object_or_404(Registration, id=user_id)
    user.delete()
    return redirect('admin_users')



def edit_skill(request, skill_name):
    # Get all users that have this skill
    offered_users = Registration.objects.filter(skills_offered=skill_name)
    needed_users = Registration.objects.filter(skills_needed=skill_name)

    if request.method == "POST":
        new_name = request.POST.get("skill_name")
        
        # Update offered skills
        for u in offered_users:
            u.skills_offered = new_name
            u.save()
        # Update needed skills
        for u in needed_users:
            u.skills_needed = new_name
            u.save()

        return redirect('admin_skills')

    return render(request, 'edit_skill.html', {'skill_name': skill_name})


def delete_skill(request, skill_name):
    # Remove this skill from all users
    Registration.objects.filter(skills_offered=skill_name).update(skills_offered=None)
    Registration.objects.filter(skills_needed=skill_name).update(skills_needed=None)
    return redirect('admin_skills')
