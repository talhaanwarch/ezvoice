# Generated by Django 3.1.1 on 2020-11-18 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='language',
            field=models.CharField(choices=[('ur-PK', 'Urdu'), ('en-US', 'English')], default='ur-PK', max_length=15),
        ),
    ]
