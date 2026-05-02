from django.contrib import admin
from .models import Registration,Post
from .models import Session
from .models import Review
from .models import Skill
from .models import Suggestion

# Register your models here.

admin.site.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    # This controls which columns appear in the table
    list_display = ("name", "email", "phone_no", "skills_offered", "skills_needed", "date_joined")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('skill', 'mentor', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('skill', 'mentor__name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("reviewer_name", "skill_name", "rating", "date_submitted")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "learners")


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ("name", "role")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "created_at", "like_count")

    def like_count(self, obj):
        return obj.likes.count()
