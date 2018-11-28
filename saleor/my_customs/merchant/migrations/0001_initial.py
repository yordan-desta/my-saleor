# Generated by Django 2.1.3 on 2018-11-28 08:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shipping', '0014_auto_20180920_0956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('modified_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Active'), ('S', 'Suspended'), ('C', 'Closed')], max_length=5)),
                ('company_name', models.CharField(max_length=30)),
                ('company_desc', models.CharField(max_length=200)),
                ('company_web_link', models.URLField(verbose_name='company website')),
                ('company_image', models.ImageField(upload_to='', verbose_name='company image')),
                ('company_email', models.EmailField(max_length=254)),
                ('company_phone', models.CharField(max_length=12)),
                ('shipping_method', models.ManyToManyField(related_name='merchants', to='shipping.ShippingMethod')),
                ('shipping_zone', models.ManyToManyField(related_name='merchants', to='shipping.ShippingZone')),
            ],
            options={
                'ordering': ['-modified_on'],
            },
        ),
    ]
