# Generated by Django 3.1.1 on 2020-11-24 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_app', '0002_auto_20201118_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='language',
            field=models.CharField(choices=[('ur-PK', 'Urdu'), ('en-IN', 'English')], default='ur-PK', max_length=15),
        ),
    ]
