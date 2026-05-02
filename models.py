from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    skills_offered = models.CharField(max_length=200, blank=True, null=True)
    skills_needed = models.CharField(max_length=200, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
        # 🔹 Add this line for bookmarks
    bookmarks = models.ManyToManyField('Post', blank=True, related_name='bookmarked_by')  
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name}"




class Session(models.Model):
    skill = models.CharField(max_length=100)
    mentor = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='mentored_sessions')
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=[('upcoming', 'Upcoming'), ('completed', 'Completed')],
        default='upcoming'
    )
    participants = models.ManyToManyField(Registration, related_name='sessions_joined', blank=True)

    def __str__(self):
        return f"{self.skill} - {self.mentor.name} ({self.status})"
    


class Review(models.Model):
    reviewer_name = models.CharField(max_length=100)
    skill_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    date_submitted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.reviewer_name} - {self.skill_name} ({self.rating}/5)"
    


class Skill(models.Model):
    name = models.CharField(max_length=100)
    learners = models.IntegerField(default=0)
    icon = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    


class Suggestion(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Post(models.Model):
    user = models.ForeignKey(Registration, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.name} - {self.title}"

    class Meta:
        ordering = ['-created_at']

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_comments')
    user = models.ForeignKey('Registration', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.name} on {self.post.title}"
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.name} on {self.post}"



class Follow(models.Model):
    follower = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['follower', 'following']
        indexes = [
            models.Index(fields=['follower', 'following']),
        ]
    
    def __str__(self):
        return f"{self.follower.name} follows {self.following.name}"
    
    def save(self, *args, **kwargs):
        # Prevent self-follow
        if self.follower == self.following:
            raise ValueError("Users cannot follow themselves.")
        super().save(*args, **kwargs)

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('mention', 'Mention'),
    ]
    
    user = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='notifications')
    from_user = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type} notification for {self.user.name}"
    
    @property
    def message(self):
        if self.notification_type == 'like':
            return f"{self.from_user.name} liked your post"
        elif self.notification_type == 'comment':
            return f"{self.from_user.name} commented on your post"
        elif self.notification_type == 'follow':
            return f"{self.from_user.name} started following you"
        elif self.notification_type == 'mention':
            return f"{self.from_user.name} mentioned you in a post"
        return "New notification"