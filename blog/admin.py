from django.contrib import admin
from .models import Category, Tag, Post
from django.utils import timezone
from django.utils.html import format_html

# ------------> Models Registered<------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)
    @admin.display(description='Posts')
    def post_count(self, obj):
        return obj.posts.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)
    @admin.display(description='Posts')
    def post_count(self, obj):
        return obj.posts.count()
    

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'colored_status',
        'author',
        'published_at',
        'created_at',
    )

    list_filter = ('status', 'created_at', 'category')
    search_fields = ('title', 'content')

    prepopulated_fields = {"slug": ("title",)}

    readonly_fields = ('created_at', 'updated_at')

    date_hierarchy = 'published_at'

    actions = ['publish_posts', 'make_draft']

    @admin.display(description='Status')
    def colored_status(self, obj):

        if obj.status == Post.Status.PUBLISHED:
            color = 'green'
        elif obj.status == Post.Status.DRAFT:
            color = 'orange'
        else:
            color = 'red'

        return format_html(
            '<strong style="color:{};">{}</strong>',
            color,
            obj.get_status_display()
        )

    @admin.action(description='Publish selected posts')
    def publish_posts(self, request, queryset):
        queryset.update(
            status=Post.Status.PUBLISHED,
            published_at=timezone.now()
        )

    @admin.action(description='Move selected posts to draft')
    def make_draft(self, request, queryset):
        queryset.update(
            status=Post.Status.DRAFT,
            published_at=None
        )