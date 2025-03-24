from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'is_premium')
    prepopulated_fields = {'slug': ('title',)}
    fields = (
        'title', 'slug', 'date', 'category',
        'intro', 'content', 'image', 'is_premium',
        'chemistry_rating', 'banter_rating', 'looks_rating', 'vibe_rating',
    )

admin.site.register(Post, PostAdmin)

