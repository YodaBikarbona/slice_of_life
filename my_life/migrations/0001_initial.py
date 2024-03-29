# Generated by Django 3.0.4 on 2020-04-30 08:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('google_drive_link', models.CharField(max_length=10000)),
                ('file_name', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.CharField(max_length=128)),
                ('comment', models.BooleanField(default=False)),
                ('views', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('path', models.CharField(blank=True, max_length=256, null=True)),
                ('postImage', models.BooleanField(default=False)),
                ('uniqueId', models.CharField(blank=True, max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('edited', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=126)),
                ('content', models.TextField(max_length=65535)),
                ('comment', models.BooleanField(default=False)),
                ('views', models.IntegerField(default=0)),
                ('uniqueId', models.CharField(blank=True, max_length=256, null=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_life.Image')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_name', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('activated', models.BooleanField(default=False)),
                ('newsletter', models.BooleanField(default=False)),
                ('blocked', models.BooleanField(default=False)),
                ('salt', models.CharField(default="^Me':(@0i&0;?E(KN0ys-Y@AKsmo2ZKU", max_length=255)),
                ('admin_password', models.CharField(blank=True, max_length=25, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_life.Role')),
            ],
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.CharField(max_length=128)),
                ('approved', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_life.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_life.User')),
            ],
        ),
        migrations.CreateModel(
            name='ImageComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.CharField(max_length=128)),
                ('approved', models.BooleanField(default=False)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_life.Image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_life.User')),
            ],
        ),
    ]
