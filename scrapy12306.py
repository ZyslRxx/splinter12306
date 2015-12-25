#coding:utf-8
from splinter.browser import Browser
import ConfigParser
import sys
import time
import codecs
class Scrapy12306():

    def __init__(self):

        config = ConfigParser.ConfigParser()
        config.readfp(codecs.open("12306.conf", "r", "utf-8"))
        self.url = config.get("config","url")
        self.username = config.get("config","username")
        self.password = config.get("config","password")
        self.bType = config.get("config","browser")
        #self._from = config.get("config","_from")
        #self._to = config.get("config","_to")
        self._from = u'北京'
        self._to = u'邯郸'
        self.date = config.get("config","date")
        
        print "browser :%s url:%s" % (self.bType,self.url)
        self.browser = Browser(self.bType)
        self.browser.visit(self.url)

    def login(self):
        if self.username=="" or self.password=="":
            print "error:username and password must not be empty"
            self.browser.quit()
            sys.exit(-1)
        self.browser.fill("loginUserDTO.user_name",self.username)
        self.browser.fill("userDTO.password",self.password)
        time.sleep(10)
        self.browser.find_by_id("loginSub").click()
        loginFlag = self.browser.find_by_id("link_4_myTicket")
        return not loginFlag.is_empty()


    def getTicket(self):
        self.browser.find_by_xpath("//a[@href='/otn/leftTicket/init']")[0].click()
        #self.browser.fill("leftTicketDTO.from_station_name",self._from)
        #self.browser.fill("leftTicketDTO.to_station_name",self._to)
        self.browser.cookies.add({"_jc_save_fromStation":"%u5317%u4EAC%2CBJP"})
        self.browser.cookies.add({'_jc_save_toStation':'%u90AF%u90F8%2CHDP'})
        #self.browser.fill("leftTicketDTO.train_date",self.date)
        self.browser.cookies.add({"_jc_save_fromDate":self.date})
        isload = False
        while not isload:
            self.browser.reload()
            isload = self.browser.is_element_present_by_id("query_ticket",wait_time=10)
            if not isload:
                time.sleep(30)
                continue

            qt = self.browser.find_by_id("query_ticket")
            qt.click()

        print self.browser.cookies.all()
        flag = False
        while not flag:
            try:
                stations = self.browser.find_by_text(u"预订")
                station = []
                for i in range(11,21):

                    station = stations[i]
                    flag =station.has_class("btn72")
                     
                    if flag:
                        break

                if not flag:
                    qt = self.browser.find_by_id("query_ticket").click()
                    time.sleep(2)
                    continue
                station.click()
                time.sleep(1)
            except Exception as e:
                print  e.message
                
                flag = False

        p1 = self.browser.find_by_xpath("//label[@for='normalPassenger_0']")
        p2 = self.browser.find_by_xpath("//label[@for='normalPassenger_3']")
        print 'p1,p2:%s %s' % (p1,p2)

        if p1.is_empty():
            p1 = self.browser.find_by_id("normalPassenger_0")[0].click()
        else :
            p1[0].click()

        if p2.is_empty():
            p2 = self.browser.find_by_id("normalPassenger_3")[0].click()
        else :
            p2[0].click()
        self.browser.evaluate_script("confirm('抢到票了帅哥,订票吗')")
        time.sleep(15)
        self.browser.find_by_id("submitOrder_id").click()


if __name__ == "__main__":


    scrapy = Scrapy12306()
    flag = scrapy.login()
    while not flag:
        flag = scrapy.login()

    scrapy.getTicket()
