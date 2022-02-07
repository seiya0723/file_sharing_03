# Generated by Django 3.2.10 on 2022-01-24 06:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日')),
                ('name', models.CharField(max_length=500, verbose_name='ファイル名')),
                ('content', models.FileField(upload_to='share/document/content', verbose_name='ファイル')),
                ('mime', models.TextField(blank=True, null=True, verbose_name='MIMEタイプ')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
        ),
    ]