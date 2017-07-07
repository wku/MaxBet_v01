
import time
from argparse import ArgumentParser
from pyvirtualdisplay import Display
import sys
import simplejson as json

from src import Parser, Logic
from src import login, base_url, Userlogin, UserPassword, login_UserName_loc, login_Password_loc, login_SignIn_loc, SERVER, PORTS, LOGER
from src import logger
from src.ldb import db
import redis
import time
import datetime


parser = ArgumentParser()
parser.add_argument("--login", help="1 or 2", default='1')
args = vars(parser.parse_args())


red = redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True)

if LOGER:
    log = logger.Log('maxBetLog.log', logger.Log.INFO, timePrefix=True)
else:
    log = logger.Log('maxBetLog.log', logger.Log.CRITICAL, timePrefix=True)



db.set('log', log)



if SERVER:
    display = Display(visible=0, size=(1600, 900))
    display.start()


SLEEP = 0.1


def get_change(current, previous):
    if current == previous:
        return 0
    if current > previous:
        return 0
    try:
        return ((abs(current - previous)) / previous)*100.0
    except:
        return 0


def fMatchNum(matchNum):
    s = 0
    for f in matchNum:
        try: s = s + int(matchNum[f])
        except: pass
    return s


def main(params, l):

    time_start = datetime.datetime.fromtimestamp(time.time())
    print('<main> time_start: ', time_start)
    l.url = base_url
    l.user_Login(Userlogin[params['login']], UserPassword[params['login']])

    # l.maximize_window()
    lo = Logic(l.driver)
    time.sleep(2)
    lo.leftSwitchVer()
    time.sleep(5)
    lo.runLive()
    time.sleep(5)
    lo.openTabs()
    time.sleep(5)
    lo.allUnselect()
    time.sleep(5)
    lo.js()
    time.sleep(2)


    while True:
        time_old = datetime.datetime.fromtimestamp(time.time())
        time.sleep(0.5)
        matchNum = lo.matchNum()
        s= fMatchNum(matchNum)
        cmd = """
        var done1 = arguments[0];
        window.maxBetTriger = true;
            setTimeout( function() {
            //true если есть
            //$(".category-sportList-main[title=Soccer] div").hasClass( "checkbox-checked" )

                try { $(".category-sportList-main[title=" + window.maxBetName + "] div").click(); } catch (err) { };
                try { $(".category-sportList-main[title=" + window.maxBetName2 + "] div").click(); } catch (err) { };
                try { $(".category-sportList-main[title=" + window.maxBetName3 + "] div").click(); } catch (err) { };
            } , 400);
        done1(1);
        """
        time.sleep(1)

        try:
            cmd = """
           var done = arguments[0];
            (window.foo=function foo(){ if (window.maxBetTriger == false){ return done(window.maxBetData);}; delay = 1000; setTimeout(foo, delay);})();


            """
            done = l.execute_async_script(cmd)
            time.sleep(1)

            pa = Parser()
            rez, fsource, fmatch  = pa.pars(done)
            previous = matchNum
            current = rez
            previous = sum([int(previous[key]) for key in previous if previous[key] != ""])
            current = sum([int(current[key]) for key in current if current[key] != ""])
            rezik = get_change(current, previous)
            if previous > 8 and int(rezik) >= 20:
                pass

            else:
                time_current = datetime.datetime.fromtimestamp(time.time())
                time_old = time_current
                red.set("maxbet", json.dumps(fsource))
                red.set("maxbetList", json.dumps(fmatch) )

            cmd = """
            var done1 = arguments[0];
            window.maxBetData=[];
            window.maxBetTriger = true;

            setTimeout( function() {
                try { $(".category-sportList-main[title=" + window.maxBetName + "] div").click(); } catch (err) { };
                try { $(".category-sportList-main[title=" + window.maxBetName2 + "] div").click(); } catch (err) { };
                try { $(".category-sportList-main[title=" + window.maxBetName3 + "] div").click(); } catch (err) { };
            } , 400);
            done1(1);
            """
            # done1 = l.execute_script(cmd)
            done1 = l.execute_async_script(cmd)
            time.sleep(1)


        except:
            l.exit()
            l.close()



    l.exit()
    l.close()


if __name__ == '__main__':
    log('argument: ', args, level=log.INFO)
    l = login(login_UserName_loc, login_Password_loc, login_SignIn_loc, PORTS[args['login']], SERVER)
    main(args, l)

    if SERVER:
        display.stop()



