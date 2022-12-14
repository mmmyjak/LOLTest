# Generated by Django 4.0.4 on 2022-06-10 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_name', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=10)),
                ('search_count', models.IntegerField(default=0)),
                ('recommended', models.BooleanField(default=False)),
                ('level', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Ranks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('rank', models.CharField(max_length=50)),
                ('lp', models.IntegerField(default=0)),
                ('wins', models.IntegerField(default=0)),
                ('losses', models.IntegerField(default=0)),
                ('winrate', models.IntegerField(default=0)),
                ('player_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loltest.player')),
            ],
        ),
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('champ', models.CharField(max_length=50)),
                ('kda', models.CharField(max_length=20)),
                ('gamemode', models.CharField(max_length=50)),
                ('date', models.CharField(max_length=20)),
                ('epoch', models.IntegerField(default=0)),
                ('player_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loltest.player')),
            ],
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('champ_name', models.CharField(max_length=50)),
                ('champ_points', models.IntegerField(default=0)),
                ('player_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loltest.player')),
            ],
        ),
    ]
