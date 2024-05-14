# Generated by Django 4.2 on 2024-05-11 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('private', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'video'), (2, 'audio')], default=1)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'not_answered'), (2, 'answered'), (3, 'canceled'), (4, 'reject')], default=1)),
                ('callee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calls_callee', to=settings.AUTH_USER_MODEL)),
                ('caller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calls_caller', to=settings.AUTH_USER_MODEL)),
                ('private_chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calls', to='private.privatechat')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
