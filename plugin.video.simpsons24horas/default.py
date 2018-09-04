# -*- coding: utf-8 -*-
#------------------------------------------------------------
# 
#------------------------------------------------------------
# Licença: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Baseado no código do addon youtube
#------------------------------------------------------------

import os
import sys
import time
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon
from random import randint

addonID = 'plugin.video.simpsons24horas'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

addonfolder = local.getAddonInfo('path')
resfolder = addonfolder + '/resources/'

temp = randint(1,22)

addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ).decode("utf-8"), addonID)

if not os.path.exists(addon_data_dir):
	os.makedirs(addon_data_dir)

m3u =  os.path.join(addon_data_dir, "files.m3u")

file = open(""+m3u+"","w")
file.close

temp = randint(1,23)
eps = [13,22,24,22,22,25,25,25,25,23,22,21,22,22,22,21,22,22,20,23,22,22]
valor = eps[temp - 1]
svalor = int(valor)
stemp = "%02d" %(temp)
sstemp  = str(stemp)
i = 0
        
for j in range(i,svalor):
        
        file = open(""+m3u+"","a")
        igvar = "%02d" %(j+1)
        gvar = str(igvar)
        # http://vd.ec.cx/vd/dd/RC/RCServer01/videos/NRTOSHPEP"+gvar+".mp4 
        file.write("http://vd.ec.cx/vd/dd/RC/RCServer01/videos/OSMPST"+sstemp+"EP"+igvar+".mp4")
        file.write("\n")
        file.close

        
xbmc.Player().play(""+m3u+"")

