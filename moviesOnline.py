import sys
import xbmc, xbmcgui
import xbmcplugin

import urllib, urllib2, re, tempfile

from glob import addon_log, addon, Downloader

from xbmcswift2 import Plugin, xbmcgui

from resources.lib import constants
from resources.lib import scraper

plugin = Plugin()



@plugin.route('/')
def show_categories():
  
  items = [{'label': addon.getLocalizedString(30303),
            #'thumbnail': category['thumb'],
            'path': plugin.url_for(
                endpoint = 'search',
                site = constants.ID_990_RO,
            )
           },
           {'label': addon.getLocalizedString(30304),
            'path': plugin.url_for(
                endpoint = 'search',
                site = constants.ID_FILMEONLINE2013_BIZ,
            )
           }]

  return plugin.finish(items)


@plugin.route('/search/<site>/')
def search(site):
  #addon_log(site)  
  movieListData = scraper.parse_video_url(site)
  if movieListData:
    items = [{
        'label': video[1],
        #'thumbnail': video['thumb'],
        #'is_playable': True,
        'path': plugin.url_for(
            endpoint='check_type',
            path=video[0]
        ),
    } for video in movieListData]
    return plugin.finish(items)
  else:
    # ERR movie not found
    return 0
        
@plugin.route('/videos/<path>/')
def check_type(path):
  videoType, episodes = scraper.checkVideoType(path)
  #addon_log(videoType)
  if videoType == 2:
    #addon_log(episodes)
    # seasonName, title, href
    items = [{
        'label': episode[0] + " - " + episode[1],
        #'thumbnail': video['thumb'],
        #'is_playable': True,
        'path': plugin.url_for(
            endpoint='play_video',
            path=episode[2]
        ),
    } for episode in episodes]
    return plugin.finish(items)
  
  elif videoType == 1:
    #play video on fastupload
    addon_log("play video")
    play_video(path)
  else:
    addon_log("ERROR")
  

@plugin.route('/play_video/<path>/')
def play_video(path):
  #addon_log(path)
  url, subtitle = scraper.grabFastUploadStream("http://www.990.ro/"+path)
  if subtitle:
    
    __addondir__    = xbmc.translatePath(addon.getAddonInfo('profile') )
    #__addondir__    = xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))
    #addon_log(__addondir__)
    #subName = __addondir__  + "\\userData\\" + "subtitle.srt"
    subName = __addondir__  + "subtitle.srt"
    #addon_log(subName)
    
    #sub = urllib.URLopener()
    #sub.retrieve(subtitle, subName)
    
    data = urllib2.urlopen(subtitle).read().decode("utf-8")
    f = open(subName, 'wb')
    f.write(data.encode('utf-8'))
    f.close()

    #xbmc.Player().setSubtitleStream(1)
  
  if xbmc.Player(xbmc.PLAYER_CORE_AUTO).isPlaying():
    xbmc.Player(xbmc.PLAYER_CORE_AUTO).stop()
    
    try: xbmc.executebuiltin("Dialog.Close(all,true)")
    except: pass
    
    xbmc.executebuiltin( "ActivateWindow(busydialog)" )
    xbmc.sleep(800)
  else:
    xbmc.executebuiltin( "ActivateWindow(busydialog)" )
    xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(url)
    if subtitle:
      xbmc.Player().setSubtitles(subName)
      xbmc.Player().showSubtitles(True)
  


if __name__ == '__main__':
    try:
        plugin.run()
    except scraper.NetworkError:
        plugin.notify(msg=_('network_error'))#NOTE: declare function "_()"
    except NotImplementedError, message:
        plugin.notify(msg=_('not_implemented'))
        log('NotImplementedError: %s' % message)
    except scraper.TerritoryError:
        plugin.notify(msg=_('not_available_in_your_country'))