
import redis
import sys
import datetime
import time
import hashlib
import re
import simplejson as json

from src.ldb import db
# log = db.get('log')
from src import logger
log = logger.Log('maxBetLog.log', logger.Log.CRITICAL, timePrefix=True)

red = redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True)




def fromMalay(odd):
    try: odd =float(odd)
    except:
        log('fromMalay except odd: ', odd, level=db.get('log').CRITICAL)
    if odd == 0.0: return 0
    if odd > 0: return odd + 1
    return round(-1/odd+ 1, 3)

def xreny(value1, value2):
    if value1 == value2 and value1==0: return 0,0
    value1 = float(value1); value2 = float(value2)
    if value1 == False: value1 = value2; value2 = value1*-1
    else: value2 = value1; value1 = value2 * -1
    return value1, value2


def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return days, hours, minutes, seconds


def nData(DATA2):
    FULLMATCH = []
    for sport in DATA2:
        match_ =  DATA2[sport].get('match', None)
        if not match_ :
            log("exept //  странно но почемуто нет match: ", DATA2[sport], ' : ', sport, ' : <<<< ', DATA2, ' >>>> ', level=db.get('log').DEBUG)
            continue

        for match in DATA2[sport]['match']:
            matchInfo = DATA2[sport]['match'][match].get('info', None)
            if not matchInfo:
                log('nData not matchInfo ', DATA2[sport]['match'][match], level=db.get('log').DEBUG)
                continue
            matchRate = DATA2[sport]['match'][match]['rate']
            liveperiod = matchInfo.get('liveperiod', 100)

            if liveperiod==0:
                liveperiod_ = "HT"
            elif liveperiod==1:
                liveperiod_ = "1H"
            elif liveperiod==2:
                liveperiod_ = "2H"
            else:
                liveperiod_ = ""

            if matchInfo['sporttype'] == 1:
                tstamp = int(matchInfo['tstamp'])
                livetimer = int(matchInfo['livetimer']) #* 1000
                kickofftime = int(matchInfo['kickofftime'])#* 1000
                sporttype_ = 'Soccer'
                ts = time.time()
                diff = (datetime.datetime.fromtimestamp(ts) - datetime.datetime.fromtimestamp(livetimer))
                kf = 0
                date = str(int((diff.total_seconds() % 3600) // 60)+kf) + "'"
                if liveperiod_ == "HT":
                    if matchInfo.get('gv', None):
                        date = liveperiod_
                    else:
                        date = 'LIVE'
                else:
                    date = liveperiod_ + ' ' + date

            elif matchInfo['sporttype'] == 2:
                sporttype_ = 'Basketball'
                date = "!Live"

            elif matchInfo['sporttype'] == 5:
                sporttype_ = 'Tennis'
                date = "!Live"
            else:
                date = "!Live"
                sporttype_ =   matchInfo['sporttype']

            timestamp = lambda: int(round(time.time() * 1000))
            MATCH = {
                "away_team": matchInfo['ateamnameen'],
                "date": date,
                "timestamp": timestamp(),
                "home_team": matchInfo['hteamnameen'],
                "is_live": 1,
                "league": matchInfo['leaguenameen'],
                "mainline_bets": [],
                "red_card_a": matchInfo['awayred'],
                "red_card_h": matchInfo['homered'],
                "score_a": matchInfo['liveawayscore'],
                "score_h": matchInfo['livehomescore'],
                "sport": sporttype_
            }

            for rate in matchRate:
                oddsstatus = rate.get('oddsstatus', None)
                if oddsstatus != "running": continue

                bettype = rate.get('bettype', None)
                if bettype == 1:
                    hdp1, hdp2 = xreny(rate['hdp1'], rate['hdp2'])
                    MATCH['mainline_bets'].append({"odd": fromMalay(rate['odds1a']), "opt": hdp1, "type": "FT_HDP_h", "bettype": rate['bettype']})
                    MATCH['mainline_bets'].append({"odd": fromMalay(rate['odds2a']), "opt": hdp2, "type": "FT_HDP_a", "bettype": rate['bettype']})

                elif bettype == 2:
                    MATCH['mainline_bets'].append ({"not": rate})

                elif bettype == 3:
                    if sporttype_ == 'Tennis':
                        MATCH['mainline_bets'].append({"odd": fromMalay(rate['odds1a']), "opt": rate['hdp1'], "type": "FH_OU_o", "bettype": rate['bettype']})
                        MATCH['mainline_bets'].append({"odd": fromMalay(rate['odds2a']), "opt": rate['hdp1'], "type": "FH_OU_u", "bettype": rate['bettype']})
                    else:
                        MATCH['mainline_bets'].append({"odd": fromMalay(rate['odds1a']), "opt": rate['hdp1'], "type": "FT_OU_o", "bettype": rate['bettype']})
                        MATCH['mainline_bets'].append({"odd": fromMalay(rate['odds2a']), "opt": rate['hdp1'], "type": "FT_OU_u", "bettype": rate['bettype']})

                elif bettype == 4:
                    MATCH['mainline_bets'].append({"not": rate})

                elif bettype == 5:
                    MATCH['mainline_bets'].append({"odd": rate['com1'], "type": "FT_1X2_h", "bettype": rate['bettype']})
                    MATCH['mainline_bets'].append({"odd": rate['com2'], "type": "FT_1X2_a", "bettype": rate['bettype']})
                    MATCH['mainline_bets'].append({"odd": rate['comx'], "type": "FT_1X2_d", "bettype": rate['bettype']})

                elif bettype == 6:
                    MATCH['mainline_bets'].append({"not": rate})

                elif bettype == 7:
                    hdp1, hdp2 = xreny(rate['hdp1'], rate['hdp2'])
                    MATCH['mainline_bets'].append({"odd": fromMalay(rate['odds1a']), "opt": hdp1, "type": "FH_HDP_h", "bettype": rate['bettype']})
                    MATCH['mainline_bets'].append({"odd": fromMalay(rate['odds2a']), "opt": hdp2, "type": "FH_HDP_a", "bettype": rate['bettype']})

                elif bettype == 8:
                    MATCH['mainline_bets'].append({"odd": fromMalay(rate['odds1a']), "opt": rate['hdp1'], "type": "FH_OU_o", "bettype": rate['bettype']})
                    MATCH['mainline_bets'].append({"odd": fromMalay(rate['odds2a']), "opt": rate['hdp1'], "type": "FH_OU_u", "bettype": rate['bettype']})

                elif bettype == 15:
                    MATCH['mainline_bets'].append({"odd": rate['com1'], "type": "FH_1X2_h", "bettype": rate['bettype']})
                    MATCH['mainline_bets'].append({"odd": rate['com2'], "type": "FH_1X2_a", "bettype": rate['bettype']})
                    MATCH['mainline_bets'].append({"odd": rate['comx'], "type": "FH_1X2_d", "bettype": rate['bettype']})

                elif bettype == 20:
                    MATCH['mainline_bets'].append({"odd": fromMalay(rate['odds1a']), "type": "FT_1X2_h", "bettype": rate['bettype']} )
                    MATCH['mainline_bets'].append({"odd": fromMalay(rate['odds2a']), "type": "FT_1X2_a", "bettype": rate['bettype']})

                elif bettype == 153:
                    hdp1, hdp2 = xreny(rate['hdp1'], rate['hdp2'])
                    MATCH['mainline_bets'].append({"odd": fromMalay(rate['odds1a']), "opt": hdp1, "type": "FH_HDP_h", "bettype": rate['bettype']})
                    MATCH['mainline_bets'].append({"odd": fromMalay(rate['odds2a']), "opt": hdp2, "type": "FH_HDP_a", "bettype": rate['bettype']})


                else:
                    MATCH['mainline_bets'].append({"not": rate})


            FULLMATCH.append(MATCH)

    return FULLMATCH





def sParser(i, sporttype, associations, DATA, match):
    if type(i) == type(int()):
        log('sParser return ', level=db.get('log').INFO)
        return sporttype, associations, DATA, match

    if i[0] == 'subscribe':
        associations[i[2]['id']] = i[2]['id']
        if i[2]['condition'].get('sporttype', None):
            sporttype[i[2]['id']] = i[2]['condition']['sporttype']
            DATA = {}
        elif i[2]['condition'].get('matchid', None):
            sporttype[i[2]['id']] = i[2]['condition']['matchid']
            match[i[2]['id']] = i[2]['condition']['matchid'] #TODO !!!!!!!!
        else:
            log('непонятно что делать с этими данными нет matchid ', level=db.get('log').DEBUG)
            return sporttype, associations, DATA, match


    if i[0] == 'r':
        if associations.get(i[1][0], None):
            key = str(i[1][1]).replace('[', '').replace(']', '').replace("'", '')
            associations[i[1][0]] = key
            DATA[key] = {'sporttype': sporttype[i[1][0]]}

    if i[0] == 'p':
        if i[1][0][0] == 'r4':
            return sporttype, associations, DATA, match
        else:
            key1 = str(i[1][0][0]).replace('[', '').replace(']', '').replace("'", '')
            if DATA.get(key1, None):
                courentSport = key1
                if i[1][0][1][0].get('type', None) == 'reset':
                    for x1 in i[1][0][1][1:]:
                        matchid = str([x1['matchid']]).replace('[', '').replace(']', '').replace("'", '')
                        if x1.get('hteamnameen', None):
                            try:
                                DATA[courentSport]['match'][matchid] = {'info': x1, 'rate': []}  #
                            except:
                                DATA[courentSport]['match'] = {}
                                DATA[courentSport]['match'][matchid] = {'info': x1, 'rate': []}

                        elif x1.get('matchid', None):
                            if not DATA[courentSport].get('match', None): DATA[courentSport]['match'] = {}
                            if not DATA[courentSport]['match'].get(matchid, None): DATA[courentSport]['match'][matchid] = {}
                            if not DATA[courentSport]['match'][matchid].get('rate', None): DATA[courentSport]['match'][matchid]['rate'] = []
                            DATA[courentSport]['match'][matchid]['rate'].append(x1)

                elif i[1][0][1][0].get('type', None) == 'o':
                    for oo in i[1][0][1]:
                        hteamnameen = oo.get('hteamnameen', None)
                        matchid = oo.get('matchid', None)
                        if hteamnameen:
                            try:
                                DATA[courentSport]['match'][matchid] = {'info': oo, 'rate': []}  #
                            except:
                                DATA[courentSport]['match'] = {}
                                DATA[courentSport]['match'][matchid] = {'info': oo, 'rate': []}


                        elif matchid:
                            if not DATA[courentSport].get('match', None): DATA[courentSport]['match'] = {}
                            if not DATA[courentSport]['match'].get(matchid, None): DATA[courentSport]['match'][matchid] = {}
                            if not DATA[courentSport]['match'][matchid].get('rate', None): DATA[courentSport]['match'][matchid]['rate'] = []
                            DATA[courentSport]['match'][matchid]['rate'].append(oo)


                elif i[1][0][1][0].get('type', None) == 'm':
                    pass
                elif i[1][0][1][0].get('type', None) == 'dm':
                    pass
                else:
                    pass
            else:
                pass

    return sporttype, associations, DATA, match


HASH = ''
class Parser(object):

    def __init__(self):
        pass

    def pars(self, maxBetData):
        sporttype = {}
        associations = {}
        DATA = {}
        match = {}
        for i in maxBetData:
            try:
                sporttype, associations, DATA, match = sParser(json.loads(i.replace('42[', '[')), sporttype, associations, DATA, match)
            except:
                log('<Parser>.pars EXEPT данные не распарсил return i: ', i, level=db.get('log').CRITICAL)
                return False

        oData = json.dumps(DATA)
        if DATA:
            red.set("maxbet",  oData )
        hash = hashlib.md5(oData.encode()).hexdigest()


        matchList = nData(DATA)
        oData1 = json.dumps(matchList)
        if matchList:
            log('<Parser>.pars matchList len: ', len(matchList), level=db.get('log').INFO)
            red.set("maxbetList", oData1)
        hash1 = hashlib.md5(oData1.encode()).hexdigest()

        log('<Parser>.pars hash redis new data : ', hash, level=db.get('log').INFO)

        log('<Parser>.pars hash redis new data hash1 : ', hash1, level=db.get('log').INFO)
        log('<Parser>.pars hash redis new data oData1 : ', oData1, level=db.get('log').INFO)
        oor = {'Soccer': 0, 'Tennis': 0, 'Basketball': 0}
        if matchList:
            for ioor in matchList:
                oor[ioor['sport']] = oor[ioor['sport']]  +1

        if not matchList:
            log('<Parser>.pars oData1 == []', level=db.get('log').CRITICAL)
            return False

        if HASH == hash1:
            log('<Parser>.pars HASH == hash1', level=db.get('log').CRITICAL)
            return False
        else:
            return oor







if __name__ == '__main__':
    pass


