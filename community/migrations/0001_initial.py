# Generated by Django 3.1.1 on 2023-11-23 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
                ('is_make', models.BooleanField()),
                ('category', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('major', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('is_major', models.BooleanField()),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('img', models.TextField(null=True)),
                ('time', models.DateTimeField()),
                ('duksung', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('time', models.DateTimeField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.post')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('keyword', models.ManyToManyField(related_name='users', to='community.Keyword')),
                ('major', models.ManyToManyField(related_name='users', to='community.Major')),
                ('post', models.ManyToManyField(related_name='users', to='community.Post')),
            ],
        ),
        migrations.CreateModel(
            name='TeamComment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('time', models.DateTimeField()),
                ('secret', models.BooleanField()),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.user')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.user'),
        ),
    ]