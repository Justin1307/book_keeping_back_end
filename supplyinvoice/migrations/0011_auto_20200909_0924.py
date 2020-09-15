# Generated by Django 3.1.1 on 2020-09-09 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplyinvoice', '0010_auto_20200908_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_files', models.FileField(blank=True, default='', upload_to='')),
                ('is_processed', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='File',
        ),
    ]
