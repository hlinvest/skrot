 # numplade http://www.nummerplade.net/ajax/cardata.html?type=regnr&data=ga88294
 # stelnum http://www.nummerplade.net/ajax/cardata.html?type=stelnr&data=
# -*- coding: utf-8 -*- 
from bs4 import BeautifulSoup as bs
import urllib2

def getCarDataByPlateOrStel(plate=None, stel=None):
    if stel is None:
        splate=plate.replace(" ","")
        url="http://www.nummerplade.net/ajax/cardata.html?type=regnr&data="+splate
  
    else:
        splate=stel.replace(" ","")
        url="http://www.nummerplade.net/ajax/cardata.html?type=stelnr&data="+splate

    
    hdr = {'Accept':'*/*',
            'Accept-Encoding':'gzip,deflate,sdch',
            'Accept-Language':'da-DK,da;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,zh;q=0.2,zh-TW;q=0.2,nb;q=0.2',
            'Connection':'keep-alive',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36}'}
    req = urllib2.Request(url, headers=hdr)
    content=""
    cardata={}
    try:
        page = urllib2.urlopen(req)  
      
    except urllib2.HTTPError, e:
        content=bs(e.fp.read()) # read the error handling
        stro=content.findAll('strong')
        print stro
    
        if not stro:
            print "no car with this number"
            return None
        else:
            for i in stro:
                tag=i.string
                string=i.parent.findNext('td').string
                cardata[tag]=string
            
            print cardata
            return cardata
       
        

  
  
if __name__=="__main__":
    getCarDataByPlateOrStel(stel='ga8888294')  