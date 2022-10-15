from urllib.error import HTTPError
from django.shortcuts import redirect, render, HttpResponse
from .models import Player
from .riotapi.api_methods import RiotApiMethods
from .riotapi.languages import EN, PL
from re import match
import datetime
# Create your views here.

def mainPage(request):
    recommended = list(Player.objects.filter(recommended=True).order_by('?')[:5])
    visited = list(Player.objects.order_by('-search_count')[:5])
    text = EN if 'text' not in request.session else request.session['text']
    if 'error' in request.session:
        error = request.session['error']
        del request.session['error']
        return render(request, 'loltest/home.html', {'recs': recommended, 'vis': visited, 'error': error, 'text': text})
    else: return render(request, 'loltest/home.html', {'recs': recommended, 'vis': visited, 'text': text})
       
def account(request, server, nickname):
    text = EN if 'text' not in request.session else request.session['text']
    if 'playerdb' in request.session:
        playerDB = Player.objects.get(player_name = request.session['playerdb'], region=server)
        del request.session['playerdb']
    else: 
        try:
            serverAPI = "eun1" if server == "eune" else "euw1"
            playerAPI = RiotApiMethods(serverAPI, nickname)            
            nickname = playerAPI.get_API_name()
            try:
                playerDB = Player.objects.get(player_name = nickname, region=server)
            except:       
                profile_info = playerAPI.player_profile_info() # [name, level]
                p = Player(player_name=profile_info[0], region=server, level=profile_info[1])
                p.save()
                playerDB = Player.objects.get(player_name = nickname, region = server)
            else:
                playerDB.search_count +=1
                playerDB.save()
        except HTTPError as err:
            if err.status == 503:
                request.session['error'] = text['Error503']
            elif err.status == 404:
                request.session['error'] = text['Error404']
            elif err.status == 403:
                request.session['error'] = text['Error403']
            elif err.status == 429:
                request.session['error'] = text['Error429']
            return redirect("/")   
    ranked_info = playerDB.ranks_set.all()
    maestry_info = playerDB.favourites_set.all()
    games_info = playerDB.games_set.all()
    _stats = stats(games_info)
    return render(request, 'loltest/info.html', {'player': playerDB, "ranks":ranked_info, "maestries": maestry_info, "games": games_info, "stats": _stats, 'text': text})

def update(request, server, nickname):
    if request.method == 'POST':
        text = EN if 'text' not in request.session else request.session['text']
        try:
            serverAPI = "eun1" if server == "eune" else "euw1"
            playerAPI = RiotApiMethods(serverAPI, nickname)
            nickname = playerAPI.get_API_name()
            playerDB = Player.objects.get(player_name = nickname, region = server)
            playerDB.ranks_set.all().delete()
            playerDB.favourites_set.all().delete()
            playerDB.games_set.all().delete()
            profile_info = playerAPI.player_profile_info() # [name, level]
            playerDB.player_name = profile_info[0]
            playerDB.region = server
            playerDB.level = profile_info[1]
            playerDB.update_date = datetime.date.today()
            playerDB.save()
            rankeds = playerAPI.ranked_info() # [[type,rank,lp,wins,losses,winrate]]
            for ranked in rankeds:
                r = playerDB.ranks_set.create(type=ranked[0], rank=ranked[1], lp=ranked[2], wins=ranked[3], losses=ranked[4], winrate=ranked[5])
                r.save()
            maestries = playerAPI.maestry_info() #[[name, points]]
            for maestry in maestries:
                m = playerDB.favourites_set.create(champ_name=maestry[0], champ_points=maestry[1])
                m.save()
            games = playerAPI.matches_info() # [[champ, bool, kills, deaths, assists, mode, date, epoch]]
            for game in games:
                g = playerDB.games_set.create(champ=game[0], win=game[1], kills=game[2], deaths=game[3], assists=game[4], gamemode=game[5], date=game[6], epoch=game[7])
                g.save()
            request.session['playerdb'] = playerDB.player_name
        except HTTPError as err:
            if err.status == 503:
                request.session['error'] = text['Error503']
            elif err.status == 404:
                request.session['error'] = text['Error404']
            elif err.status == 403:
                request.session['error'] = text['Error403']
            elif err.status == 429:
                request.session['error'] = text['Error429']
            return redirect("/")   
        return redirect("/%s/%s" % (server, nickname))
    else:
        return redirect("/")

def rdr(request):
    if request.method == 'POST':
        text = EN if 'text' not in request.session else request.session['text']
        server = request.POST.get("server")
        nick = request.POST.get("nick")
        if  match("^(\w)|[ ]$", nick):
            return redirect("/%s/%s/" % (server, nick))
        else:
            print(text)
            request.session['error'] = text['ErrorMatch']
            return redirect("/")
    else:
        return redirect("/")

def language(request):
    if request.method == 'POST':
        language = request.POST.get("myselect")
        request.session['text'] = globals()[language]
        return redirect(request.POST.get("last"))
    else:
        return redirect("/")

### making stats out of db

def stats(games):

    statDict = {'ALL': {'amount':0, 'wins':0, 'losses':0, 'winrate':0, 'kills':0, 'deaths':0, 'assists':0, 'kda':0},
   'CLASSIC': {'amount':0, 'wins':0, 'losses':0, 'winrate':0, 'kills':0, 'deaths':0, 'assists':0, 'kda':0}, 
   'ARAM': {'amount':0, 'wins':0, 'losses':0, 'winrate':0, 'kills':0, 'deaths':0, 'assists':0, 'kda':0}, 
   'EVENT': {'amount':0, 'wins':0, 'losses':0, 'winrate':0, 'kills':0, 'deaths':0, 'assists':0, 'kda':0}}
    for game in games:

        statDict['ALL']['amount']+=1
        statDict['ALL']['kills']+=game.kills
        statDict['ALL']['deaths']+=game.deaths
        statDict['ALL']['assists']+=game.assists
        if game.gamemode in statDict:
            statDict[game.gamemode]['amount']+=1
            statDict[game.gamemode]['kills']+=game.kills
            statDict[game.gamemode]['deaths']+=game.deaths
            statDict[game.gamemode]['assists']+=game.assists
            if game.win:
                statDict['ALL']['wins']+=1
                statDict[game.gamemode]['wins']+=1
            else:
                statDict['ALL']['losses']+=1
                statDict[game.gamemode]['losses']+=1
        else:
            statDict['EVENT']['amount']+=1
            statDict['EVENT']['kills']+=game.kills
            statDict['EVENT']['deaths']+=game.deaths
            statDict['EVENT']['assists']+=game.assists
            if game.win:
                statDict['ALL']['wins']+=1
                statDict['EVENT']['wins']+=1
            else:
                statDict['ALL']['losses']+=1
                statDict['EVENT']['losses']+=1

    to_delete = []
    for key in statDict.keys():
        if statDict[key]['amount'] > 0:
            try:       
                statDict[key]['kda'] = round((statDict[key]['kills'] + statDict[key]['assists']) / statDict[key]['deaths'], 2)
            except ZeroDivisionError:
                statDict[key]['kda'] = "PERFECT"
            statDict[key]['winrate'] = round(statDict[key]['wins'] / (statDict[key]['wins'] + statDict[key]['losses'])*100, 2)
            if int(statDict[key]['winrate']) ==  statDict[key]['winrate']:  statDict[key]['winrate'] = str(int(statDict[key]['winrate'])) + "%"
            else: statDict[key]['winrate'] = str(statDict[key]['winrate']) + "%"
        else: to_delete.append(key)
        del statDict[key]['kills']
        del statDict[key]['deaths']
        del statDict[key]['assists']

    for td in to_delete:
        del statDict[td]
    return statDict