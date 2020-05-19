# Generated by Django 3.0.6 on 2020-05-19 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_auto_20200518_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteMetaData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.PositiveIntegerField(default=0)),
                ('clones', models.PositiveIntegerField(default=0)),
                ('note', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='meta_data', to='notes.Note')),
            ],
        ),
    ]