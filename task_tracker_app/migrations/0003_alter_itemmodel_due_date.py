# Generated by Django 5.1.1 on 2024-09-26 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_tracker_app', '0002_itemmodel_created_at_itemmodel_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemmodel',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]