# Generated by Django 4.2.7 on 2024-03-02 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organizedBy', models.CharField(default='turistaklitomici@gmail.cz', max_length=100)),
                ('event_type', models.CharField(choices=[('vylet', 'Výlet'), ('tabor_vyprava', 'Tábor/Výprava'), ('oddilovka', 'Oddílovka'), ('akce_pro_verejnost', 'Akce pro veřejnost'), ('jine', 'Jiné')], default='vylet', max_length=50)),
                ('name', models.CharField(max_length=80)),
                ('destination', models.CharField(max_length=80)),
                ('meeting', models.DateTimeField()),
                ('ending', models.DateTimeField(blank=True)),
                ('departure', models.CharField(max_length=100)),
                ('arrival', models.CharField(blank=True, default='Včas upřesníme', max_length=100)),
                ('notes', models.CharField(blank=True, default='Dobrou náladu', max_length=500)),
                ('price', models.IntegerField(default=0)),
                ('capacity', models.IntegerField(blank=True, default=50)),
                ('description', models.CharField(blank=True, default=' ', max_length=500)),
                ('travel', models.BooleanField(blank=True, default=True)),
                ('assigned', models.ManyToManyField(blank=True, related_name='assigned', to='Accounts.member')),
                ('attendance', models.ManyToManyField(blank=True, related_name='attendance', to='Accounts.member')),
            ],
        ),
    ]
