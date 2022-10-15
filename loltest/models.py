from django.db import models


# Create your models here.

class Player(models.Model):
    player_name = models.CharField(max_length=50)
    region = models.CharField(max_length=10)
    search_count = models.IntegerField(default=0)
    recommended = models.BooleanField(default=False)
    level = models.IntegerField(default=0)
    update_date = models.DateField(default="2010-01-01")

    def __str__(self):
        return self.player_name

class Ranks(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    rank = models.CharField(max_length=50)
    lp = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    winrate = models.IntegerField(default=0)

    def __str__(self):
        return str(self.player_id) + " " + self.type

class Favourites(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    champ_name = models.CharField(max_length=50)
    champ_points = models.IntegerField(default=0)
    def __str__(self):
        return str(self.player_id) + " " + self.champ_name

class Games(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    champ = models.CharField(max_length=50)
    win = models.BooleanField(default=False)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    gamemode = models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    epoch = models.IntegerField(default=0)
    def __str__(self):
        return str(self.player_id) + " " + self.champ + " - " + str(self.epoch)