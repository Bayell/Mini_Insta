from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from insta_app.models import (
    UserProfile, Hashtag, Post, PostContent, Comments,
    Follow, PostLike, CommentLike, Favorite, FavoriteItem
)


class Command(BaseCommand):
    help = 'Добавляет по 5 записей каждой модели в админку'

    def handle(self, *args, **options):
        # 5 UserProfile
        users_data = [
            {'username': 'user1', 'email': 'user1@test.com', 'first_name': 'Иван', 'last_name': 'Петров'},
            {'username': 'user2', 'email': 'user2@test.com', 'first_name': 'Мария', 'last_name': 'Сидорова'},
            {'username': 'user3', 'email': 'user3@test.com', 'first_name': 'Алексей', 'last_name': 'Козлов'},
            {'username': 'user4', 'email': 'user4@test.com', 'first_name': 'Анна', 'last_name': 'Новикова'},
            {'username': 'user5', 'email': 'user5@test.com', 'first_name': 'Дмитрий', 'last_name': 'Морозов'},
        ]
        users = []
        for u in users_data:
            user, _ = UserProfile.objects.get_or_create(username=u['username'], defaults={
                'email': u['email'], 'first_name': u['first_name'], 'last_name': u['last_name']
            })
            user.set_password('pass1234')
            user.save()
            users.append(user)

        self.stdout.write(f'Users: {len(users)}')

        # 5 Hashtag
        hashtags_data = ['travel', 'food', 'nature', 'music', 'art']
        hashtags = []
        for h in hashtags_data:
            tag, _ = Hashtag.objects.get_or_create(hashtag_name=h)
            hashtags.append(tag)

        self.stdout.write(f'Hashtags: {len(hashtags)}')

        # 5 Post
        posts_data = [
            'Отличный день в горах!',
            'Вкусный завтрак',
            'Закат у моря',
            'Новый трек в работе',
            'Выставка современного искусства',
        ]
        posts = []
        for i, desc in enumerate(posts_data):
            post = Post.objects.create(author=users[i % len(users)], description=desc)
            post.hashtag.set([hashtags[i % len(hashtags)]])
            posts.append(post)

        self.stdout.write(f'Posts: {len(posts)}')

        # 5 PostContent (нужен file - создаём заглушку)
        for i, post in enumerate(posts[:5]):
            if not PostContent.objects.filter(post=post).exists():
                pc = PostContent(post=post)
                pc.file.save(f'content_{post.id}.txt', ContentFile(b'placeholder'), save=True)
        self.stdout.write('PostContent: 5')

        # 5 Comments
        comments_data = [
            'Класс!', 'Супер!', 'Красиво!', 'Нравится!', 'Отлично!'
        ]
        comments = []
        for i, text in enumerate(comments_data):
            c = Comments.objects.create(
                user=users[i % len(users)],
                post=posts[i % len(posts)],
                text=text
            )
            comments.append(c)
        self.stdout.write(f'Comments: {len(comments)}')

        # 5 Follow
        for i in range(5):
            Follow.objects.get_or_create(
                follower=users[i % len(users)],
                following=users[(i + 1) % len(users)]
            )
        self.stdout.write('Follow: 5')

        # 5 PostLike
        for i in range(5):
            PostLike.objects.get_or_create(
                user=users[i % len(users)],
                post=posts[i % len(posts)],
                defaults={'like': True}
            )
        self.stdout.write('PostLike: 5')

        # 5 CommentLike
        for i in range(5):
            CommentLike.objects.get_or_create(
                user=users[i % len(users)],
                comment=comments[i % len(comments)],
                defaults={'like': True}
            )
        self.stdout.write('CommentLike: 5')

        # 5 Favorite + FavoriteItem
        for i in range(5):
            fav, _ = Favorite.objects.get_or_create(user=users[i % len(users)])
            FavoriteItem.objects.get_or_create(favorite=fav, post=posts[i % len(posts)])
        self.stdout.write('Favorite/FavoriteItem: 5')

        self.stdout.write(self.style.SUCCESS('Done! 5 records per model added.'))
