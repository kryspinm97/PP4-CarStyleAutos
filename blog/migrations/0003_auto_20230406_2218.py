# Generated by Django 3.2.18 on 2023-04-06 22:18

from django.db import migrations
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_car_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='rundown',
            field=django_summernote.fields.SummernoteTextField(),
        ),
        migrations.AlterField(
            model_name='car',
            name='specifications',
            field=django_summernote.fields.SummernoteTextField(),
        ),
    ]
