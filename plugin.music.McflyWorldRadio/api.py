import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import requests
import os
import sys
import shutil
import urllib2
import urllib
import re
import time
import zipfile
import ntpath
import plugintools
import socket
import sqlite3
import json
import cookielib
import base64
import fnmatch
#initialize Globals
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' 
CAPTION = 'Mcfly World Radio'


BASE_URL ="http://api.mcfly.tk/Radio"
GET_COUNTRIES_URL =  "http://api.mcfly.tk/Radio/GetList"
GET_CHANNELS_URL=  "http://api.mcfly.tk/Radio/GetStations"
SEARCH_CHANNEL_URL =   "http://api.mcfly.tk/Radio/Search/?Query="
GET_ALL_STATIONS_URL ="http://api.mcfly.tk/Radio/GetAllStations" 

#Get Addon Title
AddonTitle = "Mcfly World Radio"
Addon = xbmcaddon.Addon()
AddonId = xbmcaddon.Addon().getAddonInfo('id')
AddonPath = xbmcaddon.Addon().getAddonInfo('path')
AddonVersion = xbmcaddon.Addon().getAddonInfo('version')
DatabasePath = xbmc.translatePath('special://database')
ThumbnailsPath = xbmc.translatePath('special://thumbnails')
SkinDir = xbmc.getSkinDir()
UserDataPath = xbmc.translatePath(os.path.join('special://userdata',''))
HomePath = xbmc.translatePath(os.path.join('special://home',''))
MediaPth = xbmc.translatePath(os.path.join('special://home/media',''))
AutoexecPath = xbmc.translatePath(os.path.join(UserDataPath,'autoexec.py'));
Fanart = xbmc.translatePath(os.path.join('special://home/addons' , AddonId, 'fanart.jpg'))
Icon = xbmc.translatePath(os.path.join('special://home/addons' , AddonId,'icon.png'))
ArtPath = xbmc.translatePath(os.path.join('special://home/addons', AddonId , 'resources/art/'))
FlagsPath = xbmc.translatePath(os.path.join('special://home/addons', AddonId , 'resources/art/flags/'))
AddonDataPath = xbmc.translatePath(os.path.join(UserDataPath,'addon_data'))
PlayLists = xbmc.translatePath(os.path.join(UserDataPath,'playlists'))
AddonsPath = xbmc.translatePath(os.path.join('special://home','addons',''))
AddonCab = xbmc.translatePath(os.path.join(AddonPath,AddonId,'default.py'))
GuiSettingsXML = xbmc.translatePath(os.path.join(UserDataPath,'guisettings.xml'))
GuiFixXML = xbmc.translatePath(os.path.join(UserDataPath,'guifix.xml'))
InstallXML = xbmc.translatePath(os.path.join(UserDataPath,'install.xml'))
FavoritesXML = xbmc.translatePath(os.path.join(UserDataPath,'favourites.xml'))
SourcesXML = xbmc.translatePath(os.path.join(UserDataPath,'sources.xml'))
AdvancesSettingsXML = xbmc.translatePath(os.path.join(UserDataPath,'advancedsettings.xml'))
ProfilesXML = xbmc.translatePath(os.path.join(UserDataPath,'profiles.xml'))
RSSFeedsXML = xbmc.translatePath(os.path.join(UserDataPath,'RssFeeds.xml'))
KeyboardXML = xbmc.translatePath(os.path.join(UserDataPath,'keymaps','keyboard.xml'))
CookieJar = xbmc.translatePath(os.path.join(AddonDataPath,AddonId,'cookiejar'))
StartupXML = xbmc.translatePath(os.path.join(AddonDataPath,AddonId,'startup.xml')) 
TempXML = xbmc.translatePath(os.path.join(AddonDataPath,AddonId,'temp.xml'))
IdXML = xbmc.translatePath(os.path.join(AddonDataPath,AddonId,'id.xml'))
IdTempXML = xbmc.translatePath(os.path.join(AddonDataPath,AddonId,'idtemp.xml'))
ReasourcesPath = xbmc.translatePath(os.path.join(AddonDataPath,AddonId,'resources/'))
GuiNewXML = xbmc.translatePath(os.path.join(UserDataPath,'guinew.xml'))
GuiTemp = xbmc.translatePath(os.path.join(UserDataPath,'guitemp',''))
LogContainer = xbmc.translatePath('special://logpath')
CurrentLogPath = xbmc.translatePath(os.path.join(LogContainer,'kodi.log'))
OldLogPath = xbmc.translatePath(os.path.join(LogContainer,'kodi.old.log'))
PackagesPath = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
SKIN = xbmc.getSkinDir()
def getPlatform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'
    elif xbmc.getCondVisibility('system.platform.linux.raspberrypi'):
        return 'raspberrypi'
    elif xbmc.getCondVisibility('system.platform.linux.libreelec'):
        return 'libreelec'
    elif xbmc.getCondVisibility('system.platform.linux.openelec'):
        return 'openelec'
    elif xbmc.getCondVisibility('system.platform.darwin'):
        return 'darwin'
    else:
        return 'unknown'

def getKodiVersion():
    try:
        return xbmc.getInfoLabel("System.BuildVersion").split(' ')[0]
    except:
        return 0

Platform = getPlatform()
KodiVersion = getKodiVersion()

def hasAddon(Id):
    return xbmc.getCondVisibility('System.HasAddon(' + Id + ')')

#Get System Info...!
#xbmc.getInfoLabel

FreeSpace = xbmc.getInfoLabel('System.FreeSpace')
UsedSpace = xbmc.getInfoLabel('System.UsedSpace')
TotalSpace = xbmc.getInfoLabel('System.TotalSpace')
CpuUsage = xbmc.getInfoLabel('System.CpuUsage')
FreeMemory = xbmc.getInfoLabel('System.FreeMemory')
FriendlyName = xbmc.getInfoLabel('System.FriendlyName')
SystemTime = xbmc.getInfoLabel('System.Time')
SystemDate = xbmc.getInfoLabel('System.Date')
SystemUpTime = xbmc.getInfoLabel('System.Uptime')



#networking
IsDHCP = xbmc.getInfoLabel('Network.IsDHCP')
MacAddress = xbmc.getInfoLabel('Network.MacAddress')
IPAddress = xbmc.getInfoLabel('Network.IPAddress')

def getAddonsDbName():
    for file in os.listdir(DatabasePath):
        if fnmatch.fnmatch(file, 'Addons*.db'):
            return file;

ADDON_DB = xbmc.translatePath(os.path.join(DatabasePath,getAddonsDbName()))

