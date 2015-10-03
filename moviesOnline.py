import sys
import xbmcgui
import xbmcplugin

import urllib, urllib2, re

from glob import addon_log, addon, Downloader

from xbmcswift2 import Plugin, xbmcgui

from resources.lib import constants
from resources.lib import scraper



#   arguments:
#0	The base URL of your add-on, e.g. 'plugin://plugin.video.myaddon/'
#1	The process handle for this add-on, as a numeric string
#2	The query string passed to your add-on, e.g. '?foo=bar&baz=quux'

plugin=sys.argv[0]
addon_handle = int(sys.argv[1])
plugin2 = Plugin()

def getParams():
  param=[]

  paramstring=sys.argv[2]

  if len(paramstring)>=2:
    params=sys.argv[2]
    cleanedparams=params.replace('?','')
    if (params[len(params)-1]=='/'):
      params=params[0:len(params)-2]
    pairsofparams=cleanedparams.split('&')
    param={}
    for i in range(len(pairsofparams)):
      splitparams={}
      splitparams=pairsofparams[i].split('=')
      if (len(splitparams))==2:
        param[splitparams[0]]=splitparams[1]
  return param


def grabFuStream(name, url):
  return None

#mode can be one of the defined sites
#@plugin.route('/search/')
def search(provider):
    searchString = plugin2.keyboard(heading=addon.getLocalizedString(30305))
    
    if searchString:
      movieList = scraper.parse_video_url(provider, searchString)     
      
      if movieList:
        #xbmcplugin.setContent(addon_handle, 'movies')
        for title in movieList:
          li = xbmcgui.ListItem(title, iconImage='DefaultVideo.png')

        #url = plugin2.url_for(
        #    'show_movie_titles',
            #path=scraper.get_search_path(search_string)
        #    path=""
        #)
        #plugin2.redirect(url)
        
def show_movie_titles(path):
  videos, next_link = scraper.get_video_titles(path)
  





params = getParams()

try:
  mode = int(params["mode"])
except:
  mode = None
  
#addon_log(plugin)
#addon_log(addon_handle)
#addon_log(mode)

if(mode == None):
  xbmcplugin.setContent(addon_handle, 'movies')
  #url = 'd:\mondeo-carbuyer.mp4'
  li = xbmcgui.ListItem(addon.getLocalizedString(30303), iconImage='DefaultVideo.png')
  xbmcplugin.addDirectoryItem(handle=addon_handle, url=plugin + "?mode=" + str(constants.ID_990_RO), listitem=li)
  
  li = xbmcgui.ListItem(addon.getLocalizedString(30304), iconImage='DefaultVideo.png')
  xbmcplugin.addDirectoryItem(handle=addon_handle, url=plugin + "?mode=" + str(constants.ID_FILMEONLINE2013_BIZ), listitem=li)
  
  xbmcplugin.endOfDirectory(addon_handle)
  
else:
  provider = mode
  search(provider)  