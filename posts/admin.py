from django.contrib import admin
from .models import Post, PostImage

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'is_premium')
    prepopulated_fields = {'slug': ('title',)}
    fields = (
        'title', 'slug', 'date', 'category',
        'intro', 'content', 'image', 'is_premium',
        'chemistry_rating', 'banter_rating', 'looks_rating', 'vibe_rating',
    )
    inlines = [PostImageInline]

admin.site.register(Post, PostAdmin)
admin.site.register(PostImage)
