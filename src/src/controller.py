
import time
import lxml.html

SLEEP = 1
SLEEP_MINI = 0.1


class Logic (object):

    def __init__(self, driver):
        self.driver = driver

    def leftSwitchVer (self):
        self.driver.execute_script('window.frames["leftFrame"].document.getElementsByClassName ( "leftSwitchVer" )[0].click();')
        time.sleep(SLEEP)

    def runLive (self):
        self.driver.execute_script("jQuery('.text').click()") # run live
        time.sleep(SLEEP)

    def allUnselect (self):
        try:
            self.driver.execute_script('jQuery(".category-sportList-main[title=All] div").click();')  # all unselect
        except:
            time.sleep(SLEEP)

    def openTabs (self):
        time.sleep(SLEEP)

    def matchNum(self):

        cmd = """
        var done3 = arguments[0];
        var SoccerNum = 0;
        var BasketballNum = 0;
        var TennisNum = 0;
        try { SoccerNum =  $(".icon-sport1").find(".amount").text() } catch (err) { SoccerNum = 0};
        try { BasketballNum = $(".icon-sport2").find(".amount").text() } catch (err) { BasketballNum =0};
        try { TennisNum = $(".icon-sport5").find(".amount").text() } catch (err) {TennisNum =0 };
        if (SoccerNum ==''){SoccerNum = 0};
        if (BasketballNum ==''){BasketballNum = 0};
        if (TennisNum ==''){TennisNum = 0};
        done3({
        'Soccer': SoccerNum,
        'Basketball': BasketballNum,
        'Tennis': TennisNum,
        });
        """
        done3 = self.driver.execute_async_script(cmd)
        return done3



    def jsStart(self):
        cmd = """
        setTimeout( function() {

        try { $(".category-sportList-main[title=" + window.maxBetName + "] div").click(); } catch (err) { };
        try { $(".category-sportList-main[title=" + window.maxBetName2 + "] div").click(); } catch (err) { };
        try { $(".category-sportList-main[title=" + window.maxBetName3 + "] div").click(); } catch (err) { };


        } , 1000);
        """
        self.driver.execute_script(cmd)
        time.sleep(SLEEP_MINI)

    """All,Live Casino,Soccer,Number Game,E-Sports,Basketball,Tennis,Snooker/Pool,Handball,Mix Parlay"""
    def js(self):
        cmd = """
        (function () {
            var SoccerNum = 0;
            var BasketballNum = 0;
            var TennisNum = 0;
            window.maxBetTriger = true;
            window.maxBetData = [];
            window.maxBetNums = 0;
            window.maxBetName = 'Soccer';
            window.maxBetName2 = 'Tennis';
            window.maxBetName3 = 'Basketball';
            WebSocket.prototype._send = WebSocket.prototype.send;
            WebSocket.prototype.send = function (data) {
                this._send(data);
                this.addEventListener('message', function (msg) {
                window.maxBetLogics(msg.data);
                }, false);
                this.send = function (data) {
                    this._send(data);
                    window.maxBetLogics(data);
                };
                window.maxBetLogicsh(data);
            };
            window.maxBetLogics = function maxBetLogics(value) {
                //console.log("maxBetLogics");
                window.maxBetData.push(value);
                if (window.maxBetTriger == false)return;
                if ( $(".icon-sport1").find(".amount").text() ==""){Soccer_ = 0}else{Soccer_ = 1;}
                if ( $(".icon-sport2").find(".amount").text() ==""){Basketball_ = 0}else{Basketball_ = 1;}
                if ( $(".icon-sport5").find(".amount").text() ==""){Tennis_ = 0}else{Tennis_ = 1;}

                var summ = Soccer_ + Basketball_ + Tennis_;
                var summR = 0;
                for (i in window.maxBetData) {
                    //console.log(window.maxBetData[i]);
                    console.log("summ, summR: ", summ, summR);
                    if (window.maxBetData[i].indexOf("reset") >= summ) {
                        summR = summR + 1;
                    }
                }//end for
                if (summR >= summ) {
                    //stop
                    window.maxBetTriger = false; //есть данные
                    console.log("summ, summR..: ", summ, summR);
                    console.log("есть данные");
                } //end if


            }


        })()
        """
        self.driver.execute_script(cmd)
        time.sleep(SLEEP_MINI)





























