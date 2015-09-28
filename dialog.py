import xbmc, xbmcgui
 
#get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
ACTION_PREVIOUS_MENU = 10
 
class inputDialog(xbmcgui.Window):
  def __init__(self):
    self.strActionInfo = xbmcgui.ControlLabel(100, 120, 200, 200, '', 'font13', '0xFFFF00FF')
    self.addControl(self.strActionInfo)
    self.strActionInfo.setLabel('Push BACK to quit')
    self.strActionInfo = xbmcgui.ControlLabel(100, 300, 200, 200, '', 'font13', '0xFFFFFFFF')
    self.addControl(self.strActionInfo)
    keyboard = xbmc.Keyboard('mytext')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
      self.strActionInfo.setLabel(keyboard.getText())
    else:
      self.strActionInfo.setLabel('user canceled')
 
  def onAction(self, action):
    if action == ACTION_PREVIOUS_MENU:
      self.close()