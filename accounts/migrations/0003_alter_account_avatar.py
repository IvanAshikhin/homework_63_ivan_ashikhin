# Generated by Django 4.1.7 on 2023-03-26 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='avatar',
            field=models.ImageField(blank=True, default='https://thumbs.dreamstime.com/b/default-avatar-profile-icon-social-media-user-image-210115353.jpg', null=True, upload_to='', verbose_name='Аватар'),
        ),
    ]