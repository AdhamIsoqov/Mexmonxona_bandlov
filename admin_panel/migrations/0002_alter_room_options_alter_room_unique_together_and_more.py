# Generated by Django 5.1.6 on 2025-04-04 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['room_number'], 'verbose_name': 'Xona', 'verbose_name_plural': 'Xonalar'},
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='room',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Narxi'),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_number',
            field=models.CharField(max_length=10, unique=True, verbose_name='Xona raqami'),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_type',
            field=models.CharField(choices=[('ST', 'Standart'), ('CF', 'Komfort'), ('LX', 'Lyuks')], default='ST', max_length=2, verbose_name='Xona turi'),
        ),
        migrations.RemoveField(
            model_name='room',
            name='capacity',
        ),
        migrations.RemoveField(
            model_name='room',
            name='description',
        ),
        migrations.RemoveField(
            model_name='room',
            name='has_breakfast',
        ),
        migrations.RemoveField(
            model_name='room',
            name='hotel',
        ),
        migrations.RemoveField(
            model_name='room',
            name='price_per_night',
        ),
        migrations.RemoveField(
            model_name='room',
            name='updated_at',
        ),
        migrations.DeleteModel(
            name='Hotel',
        ),
    ]
