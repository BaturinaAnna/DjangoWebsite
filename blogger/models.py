from django.db.models import *
from django.contrib.auth.models import User


class Blog(Model):
    title = CharField(max_length=50)
    created_at = DateTimeField('creation timestamp', auto_now_add=True)
    updated_at = DateTimeField('update timestamp', auto_now=True)
    author = ForeignKey(User, on_delete=CASCADE, default=1)
    avatar = ImageField(upload_to='media/user_photo', default='avatar.png')
    views = PositiveIntegerField(default=0)
    bio = TextField(max_length=300, default="I'm Empty")
    permission = BooleanField(default=False)

    def __str__(self):
        return str(self.title)


class Post(Model):
    blog = ForeignKey(Blog, on_delete=CASCADE)
    subject = CharField(max_length=50)
    text = TextField(max_length=1000)
    created_at = DateTimeField('creation timestamp', auto_now_add=True)
    updated_at = DateTimeField('update timestamp', auto_now=True)
    # Information about building
    address = CharField(max_length=80, default='NN')
    photo = ImageField(upload_to='media/user_photo/')
    likes = PositiveIntegerField(default=0)
    # year_of_construction = ????

    def __str__(self):
        return str(self.subject)


class Like(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    post = ForeignKey(Post, on_delete=CASCADE)
    created = DateTimeField(auto_now_add=True)


class Follow(Model):
    following = ForeignKey(User, on_delete=CASCADE, related_name='following')
    follower = ForeignKey(User, on_delete=CASCADE, related_name='follower')
    created = DateTimeField(auto_now_add=True)


class Comment(Model):
    comment_post = CharField(max_length=300)
    author = ForeignKey(User, on_delete=CASCADE)
    commented_image = ForeignKey(Post, on_delete=CASCADE)
    complaints = PositiveIntegerField(default=0)
    created_at = DateTimeField('creation timestamp', auto_now_add=True)


class Complaint(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    comment = ForeignKey(Comment, on_delete=CASCADE)
    created = DateTimeField(auto_now_add=True)


class View(Model):
    viewer = ForeignKey(User, on_delete=CASCADE)
    blog = ForeignKey(Blog, on_delete=CASCADE)
    created_at = DateTimeField('creation timestamp', auto_now_add=True)