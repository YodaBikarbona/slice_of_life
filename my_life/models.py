import random
import string
from datetime import (
    datetime,
    timedelta
)
import uuid
import django
from django.db import models
from django.db.models import Q
from django.core.validators import ValidationError
from django.core.mail import send_mail
from jose import jwt
from .helper import (
    new_salt,
    new_psw
)
from .constants import (
    secret_key_word
)


class Role(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class User(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    user_name = models.CharField(
        max_length=20,
        unique=True,
    )
    email = models.EmailField(
        max_length=50,
        unique=True
    )
    activated = models.BooleanField(
        default=False
    )
    newsletter = models.BooleanField(
        default=False
    )
    blocked = models.BooleanField(
        default=False
    )
    salt = models.CharField(
        max_length=255,
        default=new_salt(),
    )
    admin_password = models.CharField(
        max_length=25,
        null=True,
        blank=True
    )
    password = models.CharField(
        null=True,
        blank=True,
        max_length=255
    )

    # Relationships

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user_name

    def save(self, *args, **kwargs):
        """
        This method is override of main method!
        """
        if self.admin_password:
            if not User.password_strength(self.admin_password):
                raise ValueError(f'Password is not valid!')
            self.password = new_psw(self.salt, self.admin_password)
            self.admin_password = None
        super(User, self).save(*args, **kwargs)

    @staticmethod
    def get_user_by_username(username):
        return User.objects.filter(user_name=username).first()

    @staticmethod
    def password_strength(password):
        """
        This method will check the password strength.
        The password need have at least 8 symbols and less than 26 symbols.
        The password need have at least one digit, at least one upper character, at least one lower character and
        at least one special symbol. The password checking will stop when the all conditions are True, no need to check
        the whole password, only if the last symbol ist one of the condition.
        :return: True or False
        """
        is_lower = False
        is_upper = False
        is_digit = False
        is_special_character = False
        spec = "@#$%^&+=.!/?*-"
        if not password:
            return False
        if (len(password) < 8) and (len(password) > 25):
            return False
        for let in password:
            try:
                let = int(let)
                is_digit = True
            except Exception as ex:
                # print(ex)
                if let in spec:
                    is_special_character = True
                if let.isalpha() and let == let.upper():
                    is_upper = True
                if let.isalpha() and let == let.lower():
                    is_lower = True
            if is_digit and is_special_character and is_upper and is_lower:
                return True
        return False

    def security_token(self):
        signed = jwt.encode(
            {'email': f'{self.email}',
             'username': f'{self.user_name}',
             'role': f'{self.role.name}',
             'user_id': self.id
             }, secret_key_word, algorithm='HS256')
        return signed


class Album(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    name = models.CharField(
        max_length=126,
        unique=True
    )


class Image(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    # image = models.ImageField('Uploaded image')
    google_drive_link = models.CharField(
        max_length=10000,
    )
    file_name = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )
    description = models.CharField(
        max_length=128
    )
    comment = models.BooleanField(
        default=False
    )
    views = models.IntegerField(
        default=0
    )
    likes = models.IntegerField(
        default=0
    )
    type = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    path = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    postImage = models.BooleanField(
        default=False
    )

    uniqueId = models.CharField(
        null=True,
        blank=True,
        max_length=256
    )

    # Relationships

    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        # self.type = self.image.name.split('.')[-1]
        # if not self.file_name:
        #     self.file_name = f'{uuid.uuid4()}.{self.type}'
        #     self.image.name = self.file_name
        # self.path = f'media/{self.file_name}'
        if not self.uniqueId:
            self.uniqueId = uuid.uuid4().int
        super(Image, self).save(*args, **kwargs)

    @staticmethod
    def get_all_photo_gallery():
        return Image.objects.filter(postImage=False).order_by('-id').all()

    @staticmethod
    def get_image_by_unique_id(id):
        return Image.objects.filter(uniqueId=id, postImage=False).first()

    @staticmethod
    def get_next_image(image_id):
        images = Image.objects.filter(postImage=False).order_by('id').all()
        ids = []
        current_index = -1
        index = -1
        if images:
            ids = [image.id for image in images]
            current_index = ids.index(image_id)
            index = current_index - 1 if current_index > 0 else -1
            if index == -1:
                return False
        return Image.objects.filter(id=ids[index], postImage=False).first()

    @staticmethod
    def get_previous_image(image_id):
        images = Image.objects.filter(postImage=False).order_by('id').all()
        ids = []
        current_index = -1
        index = -1
        if images:
            ids = [image.id for image in images]
            current_index = ids.index(image_id)
            index = current_index + 1 if current_index < len(ids) - 1 else -1
            if index == -1:
                return False
        return Image.objects.filter(id=ids[index], postImage=False).first()

    def increase_views(self):
        self.views += 1
        self.save()


class Post(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    edited = models.DateTimeField(
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=126
    )
    content = models.TextField(
        max_length=65535
    )
    comment = models.BooleanField(
        default=False
    )
    views = models.IntegerField(
        default=0
    )
    uniqueId = models.CharField(
        null=True,
        blank=True,
        max_length=256
    )

    # Relationships

    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.uniqueId:
            self.uniqueId = uuid.uuid4().int
        super(Post, self).save(*args, **kwargs)

    @staticmethod
    def get_home_posts():
        posts = Post.objects.filter().order_by('-id').all()
        return posts[:5] if len(posts) > 5 else posts

    @staticmethod
    def get_post_by_unique_id(id):
        return Post.objects.filter(uniqueId=id).first()

    @staticmethod
    def get_posts(offset, limit):
        posts = Post.objects.filter().order_by('-id').all()
        if offset and limit and limit > offset:
            posts = posts[offset*limit:(offset*limit)+limit]
        elif not offset and limit and limit > offset:
            posts = posts[:offset+limit]
        return posts

    @staticmethod
    def count_posts():
        posts_number = Post.objects.filter().count()
        return posts_number

    def increase_views(self):
        self.views += 1
        self.save()


class ImageComment(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    content = models.CharField(
        max_length=128
    )
    approved = models.BooleanField(
        default=False
    )

    # Relationships

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.image.file_name

    @staticmethod
    def get_comments_by_image_id(image_id):
        comments = ImageComment.objects.filter(
            image_id=image_id,
            approved=True,
            user__blocked=False
        ).order_by('id').all()
        return comments


class PostComment(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    content = models.CharField(
        max_length=128
    )
    approved = models.BooleanField(
        default=False
    )

    # Relationships

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.post.title

    @staticmethod
    def get_comments_by_post_id(post_id):
        comments = PostComment.objects.filter(
            post_id=post_id,
            approved=True,
            user__blocked=False
        ).order_by('id').all()
        return comments
