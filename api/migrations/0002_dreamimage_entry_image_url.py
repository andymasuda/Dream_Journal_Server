# Generated by Django 4.1.6 on 2023-02-04 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DreamImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='image_url',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.dreamimage'),
            preserve_default=False,
        ),
    ]