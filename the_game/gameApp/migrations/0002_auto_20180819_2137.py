# Generated by Django 2.0.5 on 2018-08-19 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gameApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userscores',
            name='id',
        ),
        migrations.AlterField(
            model_name='userscores',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
