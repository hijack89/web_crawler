# coding = utf-8

import os
import urllib2
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class QSBK():
    def __init__(self,page,number):
        self.page = page
        self.number = number
        self.user_agent = r"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        self.headers = {
            "User-Agent": self.user_agent
        }
        self.url = r'http://www.qiushibaike.com/hot/page/'
        self.pattern = re.compile('<h2>(.*?)</h2>'
                             '[\s\S]*?'
                             '<div class="content">\n*?'
                             '<span>(.*?)</span>'
                             '[\s\S]*?'
                             '<span class="stats-vote"><i class="number">([0-9]*)')

    def get_content(self,page):
        self.fails = 0
        while self.fails < 5 :
            try:
                request = urllib2.Request(self.url+page, headers=self.headers)
                response = urllib2.urlopen(request,timeout=5)
                content = response.read().decode('utf-8')
                return re.findall(self.pattern, content)
            except Exception, e:
                print e
                print 'trying connect again'
                self.fails+=1
            if self.fails==0:
                break
        return 0

    def start(self):
        try:
            os.mkdir("QSBK")
        except:
            pass
        for i in range(1,self.page+1):
            f = open("QSBK/page%d.txt"%i,'w')
            print '-'*40
            print 'catching page %d'%i
            items=self.get_content(str(i))
            if items == 0:
                print "catch page %d failed" % i
                continue
            f.write( 'page: %d'%i + '\n')
            f.write( '---'*20+'\n')
            for (item,j) in zip(items,range(1,len(items)+1)):
                if(int(item[2]) >= self.number):
                    f.write('number: %d'%j + '\n')
                    f.write('author:' + item[0].strip()+'\n')
                    f.write('content:\n' + item[1].replace("<br/>", "\n")+'\n')
                    f.write('praise:' + item[2]+'\n'*3)
            print 'catch page %d succeeded'%i
            f.close()
        print 'OK'

if __name__ == '__main__':
    try:
        p=input("please input the number of pages:")
        n = input("please input the number of upvote:")
    except Exception,e:
        p=1
        n=0
    test=QSBK(p,n)
    test.start()
