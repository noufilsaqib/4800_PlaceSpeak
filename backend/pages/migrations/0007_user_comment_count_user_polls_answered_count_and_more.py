# Generated by Django 5.0.4 on 2024-05-14 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_alter_user_badges'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='comment_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='polls_answered_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='post_count',
            field=models.IntegerField(default=0),
        ),
    ]
