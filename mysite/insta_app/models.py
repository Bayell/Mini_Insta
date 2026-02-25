from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ImageField
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    user_link = models.URLField(null=True, blank=True)
    is_official = models.BooleanField(default=False)
    phone_number = PhoneNumberField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f'{self.follower} follows {self.following}'

class Hashtag(models.Model):
    hashtag_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.hashtag_name

class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='authors')
    description = models.TextField(null=True, blank=True)
    music = models.FileField(upload_to='music', null=True, blank=True)
    hashtag = models.ManyToManyField(Hashtag, related_name='hashtags')
    user = models.ManyToManyField(UserProfile, related_name='users')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.description[:20]}'

class PostContent(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='contents')
    file = models.FileField(upload_to='post_contents')

    def __str__(self):
        return f'{self.post} - {self.file.name}'


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} likes {self.post}'

class Comments(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.text[:20]}'


class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f'{self.user} likes {self.comment}'

class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} favorites'

class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name='favorite_items')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.favorite.user} - {self.post}'


class Chat(models.Model):
    person = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='person')
    date = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='dates')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.person} - {self.date}'

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='images', null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.text}'