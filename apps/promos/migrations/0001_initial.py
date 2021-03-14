# Generated by Django 3.1.7 on 2021-03-14 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promo_code', models.CharField(max_length=255, unique=True)),
                ('points', models.PositiveIntegerField()),
                ('type', models.CharField(max_length=10)),
                ('creation_time', models.DateTimeField(auto_now=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField()),
                ('description', models.TextField()),
            ],
        ),
    ]
