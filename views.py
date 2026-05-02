import random
from django.shortcuts import render,redirect,get_object_or_404
from . models import*
from django.contrib import messages
from .models import Registration, Skill, Post, Follow,Comment
from django.http import JsonResponse
# Create your views here.


from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from datetime import datetime, timedelta
import json


def create_post(request):
    """
    Handle post creation with image upload and skill tagging
    """
    if request.method == 'POST':
        form = post(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Create post instance but don't save yet
                post = form.save(commit=False)
                post.user = request.user.userprofile
                
                # Save the post to get an ID
                post.save()
                
                # Handle skills tagging
                skills_data = request.POST.get('skills', '')
                if skills_data:
                    skill_ids = [int(skill_id) for skill_id in skills_data.split(',') if skill_id.strip()]
                    post.skills.add(*skill_ids)
                
                # Handle privacy settings if needed
                privacy = request.POST.get('privacy', 'public')
                # You can store privacy in post model if you add the field
                
                messages.success(request, 'Post created successfully!')
                
                # Return JSON for AJAX requests or redirect for normal form submission
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Post created successfully!',
                        'post_id': post.id
                    })
                else:
                    return redirect('user_index')
                    
            except Exception as e:
                error_msg = f"Error creating post: {str(e)}"
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': error_msg
                    }, status=400)
                else:
                    messages.error(request, error_msg)
        else:
            # Form validation failed
            error_msg = "Please correct the errors below."
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': error_msg,
                    'form_errors': form.errors
                }, status=400)
            else:
                messages.error(request, error_msg)
    
    # GET request - show empty form
    else:
        form = post()
    
    # Get available skills for the form
    available_skills = Skill.objects.all()
    
    context = {
        'form': form,
        'available_skills': available_skills,
    }
    
    return render(request, 'create_post.html', context)

@require_POST
def like_post(request, post_id):
    """
    Handle post liking/unliking via AJAX
    """
    try:
        post = get_object_or_404(Post, id=post_id)
        user_profile = request.user.userprofile
        
        if user_profile in post.likes.all():
            post.likes.remove(user_profile)
            liked = False
        else:
            post.likes.add(user_profile)
            liked = True
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'like_count': post.like_count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@require_POST
def toggle_bookmark(request, post_id):
    """
    Handle post bookmarking via AJAX
    """
    try:
        post = get_object_or_404(Post, id=post_id)
        user_profile = request.user.userprofile
        
        saved_post, created = post.objects.get_or_create(
            user=user_profile,
            post=post
        )
        
        if not created:
            saved_post.delete()
            bookmarked = False
        else:
            bookmarked = True
        
        return JsonResponse({
            'success': True,
            'bookmarked': bookmarked
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@require_POST
def add_comment(request, post_id):
    """
    Handle adding comments to posts via AJAX
    """
    try:
        post = get_object_or_404(Post, id=post_id)
        user_profile = request.user.userprofile
        
        content = request.POST.get('content', '').strip()
        if not content:
            return JsonResponse({
                'success': False,
                'error': 'Comment cannot be empty'
            }, status=400)
        
        # Create comment
        comment = Comment.objects.create(
            post=post,
            user=user_profile,
            content=content
        )
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'user_name': comment.user.name,
                'user_initials': comment.user.initials,
                'created_at': comment.created_at.strftime('%b %d, %Y %I:%M %p'),
                'time_ago': comment.created_at.strftime('%H:%M')
            },
            'comment_count': post.comment_count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@require_POST
def delete_post(request, post_id):
    """
    Handle post deletion
    """
    try:
        post = get_object_or_404(Post, id=post_id)
        user_profile = request.user.userprofile
        
        # Check if user owns the post
        if post.user != user_profile:
            return JsonResponse({
                'success': False,
                'error': 'You can only delete your own posts'
            }, status=403)
        
        post.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Post deleted successfully'
            })
        else:
            messages.success(request, 'Post deleted successfully!')
            return redirect('user_index')
            
    except Exception as e:
        error_msg = f"Error deleting post: {str(e)}"
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': error_msg
            }, status=400)
        else:
            messages.error(request, error_msg)
            return redirect('user_index')


def get_post_comments(request, post_id):
    """
    Get comments for a specific post
    """
    try:
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all().order_by('created_at')[:10]  # Get latest 10 comments
        
        comments_data = []
        for comment in comments:
            comments_data.append({
                'id': comment.id,
                'content': comment.content,
                'user_name': comment.user.name,
                'user_initials': comment.user.initials,
                'created_at': comment.created_at.strftime('%b %d, %Y %I:%M %p'),
                'time_ago': comment.created_at.strftime('%H:%M')
            })
        
        return JsonResponse({
            'success': True,
            'comments': comments_data,
            'comment_count': post.comment_count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


def edit_post(request, post_id):
    """
    Handle post editing
    """
    post = get_object_or_404(Post, id=post_id)
    user_profile = request.user.userprofile
    
    # Check if user owns the post
    if post.user != user_profile:
        messages.error(request, 'You can only edit your own posts')
        return redirect('user_index')
    
    if request.method == 'POST':
        form = post(request.POST, request.FILES, instance=post)
        
        if form.is_valid():
            try:
                # Save the updated post
                updated_post = form.save()
                
                # Update skills
                skills_data = request.POST.get('skills', '')
                if skills_data:
                    skill_ids = [int(skill_id) for skill_id in skills_data.split(',') if skill_id.strip()]
                    updated_post.skills.set(skill_ids)
                else:
                    updated_post.skills.clear()
                
                messages.success(request, 'Post updated successfully!')
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Post updated successfully!'
                    })
                else:
                    return redirect('user_index')
                    
            except Exception as e:
                error_msg = f"Error updating post: {str(e)}"
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': error_msg
                    }, status=400)
                else:
                    messages.error(request, error_msg)
    
    # GET request - show form with existing data
    else:
        form = post(instance=post)
    
    # Get available skills and current post skills
    available_skills = Skill.objects.all()
    current_skills = post.skills.all()
    
    context = {
        'form': form,
        'post': post,
        'available_skills': available_skills,
        'current_skills': current_skills,
        'editing': True
    }
    
    return render(request, 'create_post.html', context)

















@csrf_exempt
def user_index(request):
    user_id = request.session.get("u_id")
    if not user_id:
        return redirect("login")

    user = Registration.objects.get(id=user_id)

    # 🟩 Create a new post (AJAX or normal form)
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")
        tags = request.POST.get("tags")

        new_post = Post.objects.create(
            user=user,
            title=title,
            content=content,
            image=image,
            tags=tags
        )

        # Return JSON for AJAX update
        return JsonResponse({
            "status": "success",
            "id": new_post.id,
            "user": user.name,
            "title": new_post.title,
            "content": new_post.content,
            "image": new_post.image.url if new_post.image else "",
            "tags": new_post.tags or "",
            "created_at": new_post.created_at.strftime("%b %d, %Y"),
        })

    # 🟦 Fetch all posts from all users
    posts = Post.objects.select_related("user").order_by("-created_at")

    # 🟡 Stories & other data
    colors = ["#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#9B59B6",
              "#1ABC9C", "#E67E22", "#E74C3C", "#2ECC71", "#3498DB"]

    other_users = Registration.objects.exclude(id=user.id)[:10]
    stories = [
        {
            "username": u.name,
            "initials": "".join([n[0].upper() for n in u.name.split()][:2]),
            "color": random.choice(colors),
        }
        for u in other_users
    ]

    user_initials = "".join([n[0].upper() for n in user.name.split()][:2])

    # 🟠 Dynamic Suggested for You Section
    all_users = Registration.objects.exclude(id=user.id)
    following_ids = Follow.objects.filter(follower_id=user_id).values_list('following_id', flat=True)

    suggested_list = []
    for u in all_users[:5]:
        suggested_list.append({
            "user": {
                "id": u.id,
                "name": u.name,
                "skill": u.skills_offered or "SkillSwap User",
                "color": random.choice(colors),
                "initials": u.name[0].upper(),
            },
            "is_following": u.id in following_ids,
        })

    # 🟩 Final render
    return render(request, "user_index.html", {
        "user": user,
        "posts": posts,
        "stories": stories,
        "user_initials": user_initials,
        "suggested_list": suggested_list,  # ✅ added context
    })



def logout(request): 
    request.session.flush() 
    messages.success(request, "You have been logged out successfully.") 
    return redirect("auth")




def home(request):
    return render(request, 'home.html')


def auth(request):
    if request.method == "POST":
        # -------- LOGIN --------
        if "login_btn" in request.POST:
            email = request.POST.get("email")
            password = request.POST.get("password")

            # 🔹 Super admin login (hardcoded)
            if email == "admin@com" and password == "admin":
                request.session["user_id"] = 0
                request.session["u_name"] = "Super Admin"
                request.session["is_admin"] = True
                return redirect("admin_index")

            # 🔹 Normal user login
            user = Registration.objects.filter(email=email).first()
            if user and user.check_password(password):
                request.session["u_id"] = user.id
                request.session["u_name"] = user.name
                request.session["is_admin"] = False
                return redirect("user_index")
            else:
                messages.error(request, "Invalid email or password")
                return redirect("auth")

        # -------- REGISTER --------
        elif "register_btn" in request.POST:
            name = request.POST.get("name")
            email = request.POST.get("email")
            phone_no = request.POST.get("phone_no")
            skills_offered = request.POST.get("skills_offered")
            skills_needed = request.POST.get("skills_needed")
            raw_password = request.POST.get("password")

            # Check if email already exists
            if Registration.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect("auth")

            # 🔹 Save new user (including phone number)
            user = Registration(
                name=name,
                email=email,
                phone_no=phone_no,  
                skills_offered=skills_offered,
                skills_needed=skills_needed # ✅ now saving the phone number
            )
            user.set_password(raw_password)
            user.save()

            # Create session after registration
            request.session["u_id"] = user.id
            request.session["u_name"] = user.name
            request.session["is_admin"] = False

            messages.success(request, "Registration successful!")
            return redirect("user_index")

    return render(request, "auth.html")




def chklogin(request): 
    if request.method == "POST": 
        email = request.POST.get("email") 
        password = request.POST.get("password") # ✅ Hardcoded admin login 
        if email == "admin@com" and password == "admin": 
            request.session["is_admin"] = True 
            request.session["u_name"] = "Admin" 
            return redirect("admin_index") # ✅ Normal user login 
        user = Registration.objects.filter(email=email).first() 
        if user and user.check_password(password): 
            request.session["u_id"] = user.id 
            request.session["u_name"] = user.name 
            request.session["is_admin"] = False 
            return redirect("user_index") 
        messages.error(request, "Invalid email or password") 
        return redirect("auth") 
    return redirect("auth") # ---------- REGISTER ---------- 


def save_user(request): 
    if request.method == "POST": 
        name = request.POST.get("name") 
        email = request.POST.get("email") 
        raw_password = request.POST.get("password") 
        if Registration.objects.filter(email=email).exists():
             messages.error(request, "Email already exists") 
             return redirect("auth") 
        user = Registration(name=name, email=email) 
        user.set_password(raw_password) # ✅ hashed password
        user.save() # Auto login after register 
        request.session["u_id"] = user.id 
        request.session["u_name"] = user.name 
        request.session["is_admin"] = False 
        return redirect("user_index") 
    return redirect("auth")




def user_profile(request):
    user_id = request.session.get("u_id")
    if not user_id:
        return redirect("auth")

    user = Registration.objects.filter(id=user_id).first()
    if not user:
        return redirect("auth")

    skills_offered = user.skills_offered.split(",") if user.skills_offered else []
    skills_needed = user.skills_needed.split(",") if user.skills_needed else []
    user_initials = "".join([n[0] for n in user.name.split()][:2]).upper()

    return render(request, "user_profile.html", {   # ✅ updated
        "user": user,
        "user_initials": user_initials,
        "skills_offered": skills_offered,
        "skills_needed": skills_needed,
    })



# FOLLOW / UNFOLLOW (POST)
def follow_user(request, user_id):
    if request.method != 'POST':
        return redirect('user_index')

    follower_id = request.session.get('user_id')
    if not follower_id:
        messages.error(request, "Please log in.")
        return redirect('auth')

    follower = get_object_or_404(Registration, id=follower_id)
    to_follow = get_object_or_404(Registration, id=user_id)

    # Prevent following yourself
    if follower.id == to_follow.id:
        messages.error(request, "You cannot follow yourself.")
        return redirect('user_index')

    # ✅ Toggle follow/unfollow
    relation, created = Follow.objects.get_or_create(
        follower=follower,
        followed=to_follow
    )

    if created:
        # Create notification
        Notification.objects.create(
            user=to_follow,
            message=f"{follower.name} started following you."
        )
        messages.success(request, f"You are now following {to_follow.name}")
    else:
        relation.delete()
        messages.success(request, f"You unfollowed {to_follow.name}")

    return redirect('user_index')




def settings_view(request):
    # You can later pass user-specific settings if needed
    user = request.user if request.user.is_authenticated else None
    context = {
        'user': user
    }
    return render(request, 'settings.html', context)


def help_view(request):
    user = request.user if request.user.is_authenticated else None
    context = {
        'user': user
    }
    return render(request, 'help.html', context)

# My Learning page
def my_learning_view(request):
    user_id = request.session.get('u_id')
    if not user_id:
        return redirect('auth')
    user = get_object_or_404(Registration, id=user_id)
    sessions = user.sessions_joined.all().order_by('-date')
    return render(request, 'my_learning.html', {'user': user, 'sessions': sessions})


# My Skills page
def my_skills_view(request):
    user_id = request.session.get('u_id')
    if not user_id:
        return redirect('auth')
    user = get_object_or_404(Registration, id=user_id)
    skills = [s.strip() for s in (user.skills_offered or "").split(',') if s.strip()]
    return render(request, 'my_skills.html', {'user': user, 'skills': skills})


# Saved posts page
def saved_posts_view(request):
    user_id = request.session.get("u_id")

    # if user not logged in
    if not user_id:
        return redirect("auth")  # or your login page name

    try:
        user = Registration.objects.get(id=user_id)
    except Registration.DoesNotExist:
        # if user not found in DB
        request.session.flush()  # clear session
        return redirect("auth")

    saved_posts = Post.objects.filter(bookmarked_by=user)
    return render(request, "saved_posts.html", {"saved_posts": saved_posts})




def toggle_bookmark(request, post_id):
    user_id = request.session.get("u_id")
    user = get_object_or_404(Registration, id=user_id)
    post = get_object_or_404(Post, id=post_id)

    # Check if post is already bookmarked
    if post in user.bookmarked_posts.all():
        user.bookmarked_posts.remove(post)
    else:
        user.bookmarked_posts.add(post)

    return redirect('user_index')


