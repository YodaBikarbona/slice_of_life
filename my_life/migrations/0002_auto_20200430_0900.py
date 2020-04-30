# Generated by Django 3.0.4 on 2020-04-30 09:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('my_life', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=126, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='salt',
            field=models.CharField(default='D$q]D5T-}~u&U0m-sVI+\\P:q(`Ar0h27', max_length=255),
        ),
        migrations.AddField(
            model_name='image',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='my_life.Album'),
        ),
    ]
