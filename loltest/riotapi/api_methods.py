from riotwatcher import LolWatcher, ApiError
from time import gmtime
from .champions import champions_by_id
from .keys import key
from urllib.error import HTTPError


class RiotApiMethods:
    
    def __init__(self, region, name):
        self.lol_watcher = LolWatcher(key)
        self.my_region = region
        try:
            self.profile = self.lol_watcher.summoner.by_name(self.my_region, name)
        except ApiError as err:
            if err.response.status_code == 404:
                raise HTTPError(code=404, url=None, msg=None, hdrs=None, fp=None)
            elif err.response.status_code == 403:
                raise HTTPError(code=403, url=None, msg=None, hdrs=None, fp=None)
            elif err.response.status_code == 429: 
                raise HTTPError(code=429, url=None, msg=None, hdrs=None, fp=None)
            else:
                raise HTTPError(code=503, url=None, msg=None, hdrs=None, fp=None)
    def get_API_name(self):
        return self.profile['name']
        
    def player_profile_info(self):
        return [self.profile['name'], self.profile['summonerLevel']]

    def ranked_info(self):
        try:
            ranked_stats = self.lol_watcher.league.by_summoner(self.my_region, self.profile['id'])
            infoAll = []
            for type in ranked_stats:
                info = []
                info.append(type['queueType'])
                info.append(type['tier'] + " " + type['rank'])
                info.append(type['leaguePoints'])
                info.append(type['wins'])
                info.append(type['losses'])
                info.append(round(type['wins']/(type['wins'] + type['losses'])*100, 2))
                infoAll.append(info)
        except ApiError:
                raise HTTPError(code=503, url=None, msg=None, hdrs=None, fp=None)
        return infoAll

    def maestry_info(self):
        try:
            champion_masteries = self.lol_watcher.champion_mastery.by_summoner(self.my_region, self.profile['id'])
            maestryAll = []
            for m in champion_masteries[:10]:
                maestry = []
                maestry.append(champions_by_id[m['championId']])
                maestry.append(m['championPoints'])
                maestryAll.append(maestry)
        except ApiError:
                raise HTTPError(code=503, url=None, msg=None, hdrs=None, fp=None)
        return maestryAll

    def matches_info(self):
        try:
            my_matches = self.lol_watcher.match.matchlist_by_puuid(self.my_region, self.profile['puuid'])
            matchesAll = []
            for match in my_matches:
                match_detail = self.lol_watcher.match.by_id(self.my_region, match)
                my_id = match_detail['metadata']['participants'].index(self.profile['puuid'])
                match = []
                player = match_detail['info']['participants'][my_id]
                match.append(player['championName'])
                match.append(player['win'])
                match.append(player['kills'])
                match.append(player['deaths']) 
                match.append(player['assists'])
                match.append(match_detail['info']['gameMode'])
                try:
                    epoch_timestamp = match_detail['info']['gameEndTimestamp']
                except KeyError:
                    match.append("")
                    match.append(0)
                else:
                    epoch_shorter = int(str(epoch_timestamp)[:len(str(epoch_timestamp))-3])
                    timeE = gmtime(epoch_shorter)
                    match.append(str(timeE.tm_mday) + "/" + str(timeE.tm_mon) + "/" + str(timeE.tm_year))
                    match.append(epoch_shorter)
                matchesAll.append(match)
        except ApiError:
                raise HTTPError(code=503, url=None, msg=None, hdrs=None, fp=None)
        return matchesAll

    

# m1 = RiotApiMethods("euw1", "G2 BOOMER")
# # print(m1.player_profile_info())
# # print(m1.ranked_info())
# # print(m1.maestry_info())
# print(m1.matches_info())