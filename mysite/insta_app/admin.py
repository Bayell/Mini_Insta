from django.contrib import admin
from .models import (
    UserProfile, Follow, Hashtag, Post, PostContent,
    PostLike, Comments, CommentLike, Favorite, FavoriteItem
)


class PostContentInline(admin.TabularInline):
    model = PostContent
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostContentInline]
    list_display = ['id', 'author', 'description', 'created_date', 'hashtag_count']
    filter_horizontal = ['hashtag', 'user']

    def hashtag_count(self, obj):
        return obj.hashtag.count()
    hashtag_count.short_description = 'Hashtags'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'date_registered', 'is_official']


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ['id', 'hashtag_name']


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'text', 'created_date']


admin.site.register(Follow)
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)
