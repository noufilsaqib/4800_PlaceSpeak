# Generated by Django 5.0.4 on 2024-05-21 18:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0013_comment_post_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="address",
            name="address_type",
        ),
        migrations.AddField(
            model_name="address",
            name="apt_suite",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="address",
            name="ownership_type",
            field=models.CharField(
                blank=True,
                choices=[("RENT", "Rent"), ("OWN", "Own"), ("MANAGE", "Manage")],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="address",
            name="property_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("HOME", "Home"),
                    ("WORK", "Work"),
                    ("RECREATIONAL", "Recreational"),
                    ("INVESTMENT", "Investment"),
                    ("MANAGEMENT", "Management"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]