# Generated by Django 2.2 on 2019-04-07 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kms', '0002_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
