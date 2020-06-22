# Generated by Django 3.0.6 on 2020-06-22 14:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registration', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(blank=True, default=5, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('review_text', models.TextField(blank=True, null=True)),
                ('is_published', models.BooleanField(default=False)),
                ('publish_date', models.DateField(blank=True, null=True)),
                ('link_key', models.CharField(max_length=19)),
                ('corresponding_stay', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='registration.Stay')),
            ],
        ),
    ]
