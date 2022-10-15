from django.contrib import admin

from .models import Player, Ranks, Favourites, Games

# Register your models here.

admin.site.register(Player)
admin.site.register(Ranks)
admin.site.register(Favourites)
admin.site.register(Games)