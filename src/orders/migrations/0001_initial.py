# Generated by Django 2.2.6 on 2021-08-25 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_module', to='catalog.Module')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='user.Profile')),
            ],
        ),
    ]
