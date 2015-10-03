import sys
import json
import re
import urllib2
import urllib
#from urllib import quote, unquote, urlencode
from glob import addon_log
from BeautifulSoup import BeautifulSoup

import constants


def parse_video_url(provider, searchString):
  if provider == constants.ID_990_RO:
    
    return getTitlesData990ro(searchString)
    
  #elif provider == constants.ID_FILMEONLINE2013_BIZ:
   # path = constants.URL_FILMEONLINE2013_BIZ
    


def getTitlesData990ro(searchString):
  url = constants.URL_990_RO +"functions/search3/live_search_using_jquery_ajax/search.php"
  
  try:
    #addon_log("SEARCHING FOR : " + searchString + "  IN : " + url)
    
    values = {"kw":searchString}
    
    data = urllib.urlencode(values)

    request = urllib2.Request(url, data)
    request.add_header("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
    request.add_header('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0')
    #request.add_header('Cookie', "__utma=242714698.1120184440.1416404442.1443778294.1443784084.5; __utmz=242714698.1443422520.2.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); cookie_accepted=yes; PHPSESSID=420404141400b0711c876b2d8608f97a; __utmc=242714698; __utmb=242714698.1.10.1443784084; __utmt=1")
    #request.add_header('Host', "www.990.ro");
    request.add_header('Referer', "http://www.990.ro/");
    #request.add_header('Accept', "*/*");
    #request.add_header("Content-Length" ,	"9")

    response = urllib2.urlopen(request)
    
    movieList = []
    titles = []
    hrefs = [] 
    
    if response:
      html = response.read()
      tree = parseHTMLData(html)
      #addon_log(tree.findAll('a'))
      for a in tree.findAll('a'):
        href = a.get('href')
        addon_log(href)
        #addon_log(a.contents)
        #div = a.find('div', {'id': 'rest'})
        
        #title = div.find(text=True)
        #addon_log(title)
        hrefs.append({
            #'title': "",#title,
            'href': href
        })
        
      for divTitle in tree.findAll('div', {'id': 'rest'}):
        title = divTitle.find(text=True)
        addon_log(title)
        titles.append({
            'title': title
        })
      
      movieList[0] = titles
      movieList[1] = href
      

  except NameError, e:
    addon_log(">>>>>> ERROR:" + str(e).split("'")[1])
    movieList = []
    
  except:
    movieList = []

  return movieList


def parseHTMLData(html):
  tree = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
  return tree
