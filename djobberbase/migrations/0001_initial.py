# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 13:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djobberbase.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('slug', models.SlugField(blank=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('category_order', models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name='Category order')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['category_order'],
            },
            bases=(models.Model, djobberbase.models.TreeNodeMixin),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Company admin')),
                ('logo', models.ImageField(upload_to='logos', verbose_name='Company logo')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('salary_range_min', models.PositiveIntegerField(blank=True, db_index=True, null=True, verbose_name='Salary range minimum')),
                ('description', models.TextField(verbose_name='Description')),
                ('description_html', models.TextField(blank=True, verbose_name='Description in HTML')),
                ('url', models.URLField(blank=True, null=True, verbose_name='External job URL')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('valid_until', models.DateTimeField(blank=True, null=True, verbose_name='Valid until')),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text='You can hide the posting from others by unchecking this option.', verbose_name='Created on')),
                ('spotlight', models.BooleanField(db_index=True, default=False, verbose_name='Spotlight')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='djobberbase.Category', verbose_name='Category')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='djobberbase.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Job',
                'verbose_name_plural': 'Jobs',
            },
        ),
        migrations.CreateModel(
            name='JobSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(max_length=100, verbose_name='Keywords')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created on')),
            ],
            options={
                'verbose_name': 'Search',
                'verbose_name_plural': 'Searches',
            },
        ),
        migrations.CreateModel(
            name='JobStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('stat_type', models.CharField(blank=True, choices=[('A', 'Application'), ('H', 'Hit'), ('S', 'Spam')], db_index=True, max_length=1)),
                ('description', models.TextField(verbose_name='Description')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='djobberbase.Job')),
                ('submitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Job Stat',
                'verbose_name_plural': 'Job Stats',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('slug', models.SlugField(blank=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('place_type', models.IntegerField(choices=[(0, 'Continent'), (1, 'Region'), (2, 'Country'), (3, 'State'), (4, 'County'), (5, 'City'), (6, 'Street')], default=5, verbose_name='Place Type')),
            ],
            options={
                'verbose_name': 'Place',
                'verbose_name_plural': 'Places',
                'ordering': ['place_type'],
            },
            bases=(models.Model, djobberbase.models.TreeNodeMixin),
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Job type',
                'verbose_name_plural': 'Job types',
            },
        ),
        migrations.AddField(
            model_name='job',
            name='jobtype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='djobberbase.Type', verbose_name='Job Type'),
        ),
        migrations.AddField(
            model_name='job',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='djobberbase.Place', verbose_name='Place'),
        ),
    ]
