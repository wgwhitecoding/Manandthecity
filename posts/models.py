from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField  # ✅ CKEditor field

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('date', 'Date Night'),
        ('ex', 'Ex Files'),
        ('fun', 'Love & Laughs'),
        ('intimate', 'The Intimate Edit'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    intro = models.TextField(blank=True)

    # ✅ Replace basic TextField with CKEditor
    content = RichTextUploadingField()

    is_premium = models.BooleanField(default=False)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    # Ratings
    chemistry_rating = models.IntegerField(default=0)
    banter_rating = models.IntegerField(default=0)
    looks_rating = models.IntegerField(default=0)
    vibe_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')
    position = models.PositiveIntegerField(help_text="Paragraph number after which this image should appear.")

    def __str__(self):
        return f"Image for '{self.post.title}' after paragraph {self.position}"


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.email} on {self.post.title}"




