from django.db import models
from django.utils import timezone

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
    content = models.TextField()
    is_premium = models.BooleanField(default=False)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    # Ratings
    chemistry_rating = models.IntegerField(default=0)
    banter_rating = models.IntegerField(default=0)
    looks_rating = models.IntegerField(default=0)
    vibe_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title


