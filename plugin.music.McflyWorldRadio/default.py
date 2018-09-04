import api
import helpers
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

def addDir(name,url,mode,iconimage,fanart,description):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&fanart=" + urllib.quote_plus(fanart) + "&description=" + urllib.quote_plus(description)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type="Music", infoLabels={ "Title": name, "Plot": description })
    liz.setProperty("Fanart_Image", fanart)
    if mode == 3:
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    else:
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok



def get_params():
        param = []
        paramstring = sys.argv[2]
        if len(paramstring) >= 2:
                params = sys.argv[2]
                cleanedparams = params.replace('?','')
                if (params[len(params) - 1] == '/'):
                        params = params[0:len(params) - 2]
                pairsofparams = cleanedparams.split('&')
                param = {}
                for i in range(len(pairsofparams)):
                        splitparams = {}
                        splitparams = pairsofparams[i].split('=')
                        if (len(splitparams)) == 2:
                                param[splitparams[0]] = splitparams[1]
                                
        return param
                      
params = get_params()
url = None
name = None
mode = None
iconimage = None
fanart = None
description = None

try:
        url = urllib.unquote_plus(params["url"])
except:
        pass
try:
        name = urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage = urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode = int(params["mode"])
except:
        pass
try:        
        fanart = urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description = urllib.unquote_plus(params["description"])
except:
        pass

def init():
    addDir('List By Countries','http://api.mcfly.tk',1,api.ArtPath + 'map.png','fanart.jpg','')
    addDir('Full Station list A-Z','http://api.mcfly.tk',4,api.ArtPath + 'sort.png','fanart.jpg','')          
   

if mode == None or url == None or len(url) < 1:
   init()


if mode==1:
    post_dict = {}
    response = helpers.postData(api.GET_COUNTRIES_URL,post_dict)
    link = response.replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,2,api.FlagsPath + name + '.png','fanart.jpg',description)



if mode==2:
    post_dict = {
        'CountryId':url
        }
    response = helpers.postData(api.GET_CHANNELS_URL,post_dict)
    link = response.replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,3,api.FlagsPath + name + '.png',api.FlagsPath + name + '.png',description)
 

if mode==3:
    listitem =xbmcgui.ListItem (name);
    listitem.setInfo('audio', {'Title': name})
    player = xbmc.Player()
    xbmc.Player().play(url,listitem);
    xbmc.executebuiltin('ActivateWindow(10114)');


if mode==4:
    post_dict = {}
    response = helpers.postData(api.GET_ALL_STATIONS_URL,post_dict)
    link = response.replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,3,api.FlagsPath + name + '.png',api.FlagsPath + name + '.png',description)
 


#CountryId

xbmcplugin.endOfDirectory(int(sys.argv[1]))