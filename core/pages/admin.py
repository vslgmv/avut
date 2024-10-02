from django.contrib import admin
from django.utils.html import format_html

from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'thumbnail', 'views')
    search_fields = ('title', 'text',)
    list_filter = ('pub_date',)
    readonly_fields = ('views',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('title',)
        return self.readonly_fields

    def get_fields(self, request, obj=None):
        if obj:
            return ('title', 'text', 'image', 'pub_date', 'category', 'views')
        return ('title', 'text', 'image', 'pub_date', 'category')

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: auto;"/>', obj.image.url)
        return 'No Image'
    thumbnail.short_description = 'Thumbnail'
