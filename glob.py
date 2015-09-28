import xbmc, xbmcgui, xbmcaddon
import urllib, urllib2
import os, stat

addon = xbmcaddon.Addon('plugin.video.movies-online')

def addon_log(string):
  DEBUG = addon.getSetting('debug')
  ADDON_VERSION = addon.getAddonInfo('version')
  if DEBUG == 'true':
    if isinstance(string, unicode):
      string = string.encode('utf-8')
    xbmc.log("[plugin.video.movies-online-%s]: %s" %(ADDON_VERSION, string))
    
def Downloader(url,dest,description,heading):
  dp = xbmcgui.DialogProgress()
  dp.create(heading,description,url)
  dp.update(0)

  urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,dp))

def message(title, message):
  dialog = xbmcgui.Dialog()
  dialog.ok(title, message)