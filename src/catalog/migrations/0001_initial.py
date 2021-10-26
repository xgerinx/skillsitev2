# Generated by Django 2.2.6 on 2021-08-25 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('mnemo', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField()),
                ('logo', models.CharField(default='default.png', max_length=120)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('mnemo', models.CharField(max_length=200, unique=True)),
                ('color', models.CharField(default='00FF00', help_text='Hex background color of a course', max_length=7)),
                ('description', models.TextField()),
                ('price', models.PositiveIntegerField()),
                ('old_price', models.PositiveIntegerField()),
                ('video', models.URLField(blank=True, default=None, null=True)),
                ('logo', models.CharField(default='default.png', max_length=120)),
                ('slogan_goal', models.CharField(blank=True, max_length=600, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='courses', to='catalog.Categorie')),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=7)),
                ('rate', models.FloatField()),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('old_price', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('time', models.PositiveIntegerField(blank=True, default=0)),
                ('description', models.TextField()),
                ('full_description', models.TextField()),
                ('logo', models.CharField(default='default.png', max_length=120)),
                ('cover', models.CharField(blank=True, default='', max_length=120)),
                ('video', models.URLField(blank=True, default=None, null=True)),
                ('mnemo', models.CharField(max_length=120, unique=True)),
                ('order', models.CharField(blank=True, default='', max_length=120)),
                ('seo_title', models.CharField(blank=True, default='', max_length=120)),
                ('dev', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('storyline', models.CharField(max_length=255)),
                ('demo_storyline', models.CharField(max_length=255)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='modules', to='catalog.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('user_id', models.PositiveIntegerField()),
                ('course_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TargetAudience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(max_length=200)),
                ('logo', models.CharField(max_length=200)),
                ('courses', models.ManyToManyField(related_name='target_audience', to='catalog.Course')),
                ('perm_courses', models.ManyToManyField(related_name='permanent_audience', to='catalog.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.TextField()),
                ('courses', models.ManyToManyField(blank=True, related_name='study_in_course', to='catalog.Course')),
                ('modules', models.ManyToManyField(blank=True, related_name='study_in_module', to='catalog.Module')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sections', to='catalog.Module')),
            ],
        ),
        migrations.AddField(
            model_name='module',
            name='rating',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='module_rating', to='catalog.Rating'),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('express', models.BooleanField(default=False)),
                ('demo', models.BooleanField(default=False)),
                ('duration', models.DurationField()),
                ('video', models.FileField(default=None, upload_to='uploads/video/lessons/')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='lessons', to='catalog.Section')),
            ],
        ),
        migrations.CreateModel(
            name='GetToKnow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('courses', models.ManyToManyField(related_name='get_to_know', to='catalog.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Filling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('logo', models.CharField(max_length=200)),
                ('courses', models.ManyToManyField(related_name='filling', to='catalog.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=200)),
                ('logo', models.CharField(max_length=200)),
                ('courses', models.ManyToManyField(blank=True, related_name='course_features', to='catalog.Course')),
                ('modules', models.ManyToManyField(blank=True, related_name='module_features', to='catalog.Module')),
            ],
        ),
    ]
