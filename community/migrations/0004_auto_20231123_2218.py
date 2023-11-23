# Generated by Django 3.1.1 on 2023-11-23 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0003_auto_20231123_2023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='secret',
            new_name='issecret',
        ),
        migrations.RenameField(
            model_name='keyword',
            old_name='is_make',
            new_name='ismake',
        ),
        migrations.RenameField(
            model_name='keyword',
            old_name='label',
            new_name='keywordname',
        ),
        migrations.RenameField(
            model_name='major',
            old_name='major',
            new_name='majorname',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='duksung',
            new_name='isduksung',
        ),
        migrations.RemoveField(
            model_name='post',
            name='is_major',
        ),
        migrations.AddField(
            model_name='post',
            name='major',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='community.major'),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=225, null=True),
        ),
    ]
