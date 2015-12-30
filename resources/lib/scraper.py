import sys
import json
import re
import urllib2
import urllib
import string
#from urllib import quote, unquote, urlencode
from glob import addon_log,addon, Downloader

import xbmc, xbmcgui

from BeautifulSoup import BeautifulSoup

from xbmcswift2 import Plugin, xbmcgui
plugin = Plugin()

import constants

class NetworkError(Exception):
    pass


class TerritoryError(Exception):
    pass

def parse_video_url(provider):#, searchString):
  if provider == str(constants.ID_990_RO):
    addon_log(provider)
  #  return getTitlesData990ro(searchString)
    return getTitlesData990ro() 
    
  elif provider == str(constants.ID_FILMEONLINE2013_BIZ):
  #  return getTitlesFilmeOnline2013Biz(searchString)
    return getTitlesFilmeOnline2013Biz()



def getTitlesFilmeOnline2013Biz():#searchString
  #dialog = xbmcgui.Dialog()
  #dialog.notification('www.filmeonline2013.biz', 'Sorry, Feature is not available at the moment...', xbmcgui.NOTIFICATION_INFO, 5000)
  xbmcgui.Dialog().ok('www.filmeonline2013.biz', 'Sorry, Feature is not available at the moment...')
  return 0

def getTitlesData990ro():#searchString
  searchString = plugin.keyboard(heading=addon.getLocalizedString(30305))
  
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
      #addon_log(html)
      match = re.findall('<a[^>]*href=\'(.*?)\'><li[^>].*?<div[^>]id=\'rest\'>(.*?)<div[^>]id=\'auth_dat\'>.*?</div>.*?</li></a>', html)
      #addon_log(match[0][0])
      #addon_log(match[0][1])      

      return match

  except NameError, e:
    addon_log(">>>>>> ERROR:" + str(e).split("'")[1])
    # ERR could not parse site content
    movieList = []
    
  except:
    # ERR could not parse site content
    movieList = []

  return movieList


#check if video is feature or series and return the episode list if necessary
def checkVideoType(path):
    url = constants.URL_990_RO +"/"+path
    episodes = []
    try:
        request = urllib2.Request(url)
        request.add_header("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
        request.add_header('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0')
        request.add_header('Referer', "http://www.990.ro/");
        response = urllib2.urlopen(request)
        
        if response:
            html = response.read()
            #match = re.findall('<div[^>].*>.*(Sezonul.*Episodul.*).*</div>', html)
            #match = re.findall('<a[^>] class="link" href="(.*?)\">(.*?)</a>.*?|\S</div>', html)
            #episodes = match
            episodes = []
            tree = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
            content = tree.find('div', {'id': "content"})
            for div in content.findAll('div', align="left"):
                for div2 in div.findAll('div', style="position:relative; float:left; border:0px solid #000;"):
                    a = div2.find("a", href=True)
                    
                    href = a['href']
                    title = a.string
                    
                    seasonName = div2.find("div", text=re.compile("Sezonul"))
                    
                    episodes.append([seasonName, title, href])

            if len(episodes) > 0:
                videoType = constants.MOVIE_TYPE_SERIES
            else:
                videoType = constants.MOVIE_TYPE_FEATURE
                
        else:
            videoType = constants.MOVIE_TYPE_NONE

    
    except NameError, e:
      addon_log(">>>>>> ERROR:" + str(e).split("'")[1])
      videoType = constants.MOVIE_TYPE_NONE
      
    except:
      videoType = constants.MOVIE_TYPE_NONE
      
    return videoType, episodes


def grabFastUploadStream(url):

  try:
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    
  except Exception as inst:
    addon_log("ERROR ON CREATING OPENER")
    
  
  if opener:
    #try:
    
    #find first link    
    response = opener.open(url)
    source_txt = response.read()
    #addon_log(url)
    tree = BeautifulSoup(source_txt, convertEntities=BeautifulSoup.HTML_ENTITIES)
    cnt = tree.find('div', {'class': "linkviz"})
    
    a = cnt.find('a', href=re.compile('-sfast-'))# series ex. -sfast-8899.html
    if a == None:
        a = cnt.find('a', href=re.compile('-sfast.html'))# feature
    link1 = a['href']
    #addon_log(link1)
    
    #find second link
    response = opener.open("http://www.990.ro/"+link1)
    source_txt2 = response.read()
    tree2 = BeautifulSoup(source_txt2, convertEntities=BeautifulSoup.HTML_ENTITIES)
    a = tree2.find('a', href=re.compile('superweb.rol.ro'))
    link2 = a['href']#finds link with adds
    #addon_log(link2) 
    arr_link = link2.split("http://")
    if len(arr_link) > 0:
        superwebUrl = "http://" + arr_link[2]
    else:
        superwebUrl = link2
    
  
    superwebUrl = superwebUrl.replace("/1/", "/2/") #get the second link (player)
    #addon_log(superwebUrl)
    
    response = opener.open(superwebUrl)
    superwebTxt = response.read()
  
    match=re.compile('\'file\':\s*\'(http:\/\/[\w\W]+?\.\w+)\'').search(superwebTxt)
    #addon_log(match)
    if match:
      stream_url = match.group(1)
      #addon_log(stream_url)
      subtitle = grabSubtitleStream(superwebTxt)
      return stream_url, subtitle

  return None

def grabSubtitleStream(superwebTxt):
  #tree = BeautifulSoup(superwebTxt, convertEntities=BeautifulSoup.HTML_ENTITIES)
  match = re.findall('\'captions.file\':.\'(.*?)\'', superwebTxt)
  
  if len(match) > 0:
    subtitle = match[0]
    return subtitle
  else:
    return 0
    

