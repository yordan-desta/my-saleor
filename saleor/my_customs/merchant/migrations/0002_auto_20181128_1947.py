# Generated by Django 2.1.3 on 2018-11-28 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='merchant',
            options={'ordering': ('-modified_on',)},
        ),
    ]
