# Generated by Django 4.2.16 on 2024-10-24 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.artist'),
        ),
        migrations.AlterField(
            model_name='track',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category'),
        ),
        migrations.AlterField(
            model_name='track',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='covers/'),
        ),
        migrations.AlterField(
            model_name='track',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='track',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
