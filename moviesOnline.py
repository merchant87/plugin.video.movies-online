import sys
import xbmcgui
import xbmcplugin

import urllib, urllib2, re, xbmcplugin, xbmcgui

from glob import addon_log, addon, Downloader
from dialog import inputDialog

#   arguments:
#0	The base URL of your add-on, e.g. 'plugin://plugin.video.myaddon/'
#1	The process handle for this add-on, as a numeric string
#2	The query string passed to your add-on, e.g. '?foo=bar&baz=quux'

plugin=sys.argv[0]
addon_handle = int(sys.argv[1])
#paramstring = sys.argv[2]


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






params = getParams()

try:
  mode=int(params["mode"])
except:
  mode=None
  
addon_log(mode)

#if(mode == None):
  #xbmcplugin.setContent(addon_handle, 'movies')
  
#  url = 'd:\mondeo-carbuyer.mp4'
  #li = xbmcgui.ListItem(addon.getLocalizedString(30303), iconImage='DefaultVideo.png')
  #xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
  
  #li = xbmcgui.ListItem(addon.getLocalizedString(30304), iconImage='DefaultVideo.png')
  #xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
  
  #xbmcplugin.endOfDirectory(addon_handle)
  
#else:
dialog = inputDialog()
dialog.doModal()
del dialog