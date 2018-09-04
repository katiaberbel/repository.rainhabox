from urlparse import parse_qsl
from urllib import urlencode
import xbmcplugin
import importlib
import xbmcaddon
import xbmcgui
import base64
import xbmc
import sys

addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)
addonname = addon.getAddonInfo('name')
path = 'special://home/addons/%s/' % addon_id
icon = addon.getAddonInfo('icon')
fanart = addon.getAddonInfo('fanart')
_url = sys.argv[0]
_handle = int(sys.argv[1])
cookie_file = xbmc.translatePath(path+'cookies.lwp')

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))
    
def MAIN_MENU():
    ninecartoon = xbmc.translatePath(path+'resources/images/9cartoon_me.png')
    bninetynine = xbmc.translatePath(path+'resources/images/b99_tv.png')
    cartooncrazy = xbmc.translatePath(path+'resources/images/cartooncrazy_net.png')
    cartoonson = xbmc.translatePath(path+'resources/images/cartoonson_com.png')
    gostream = xbmc.translatePath(path+'resources/images/gostream_is.png')
    kimcartoon = xbmc.translatePath(path+'resources/images/kimcartoon_me.png')
    kisscartooneu = xbmc.translatePath(path+'resources/images/kisscartoon_eu.png')
    kisscartoonso = xbmc.translatePath(path+'resources/images/kisscartoon_so.png')
    kisscartoonio = xbmc.translatePath(path+'resources/images/kisscartoon_io.png')
    kisspanda = xbmc.translatePath(path+'resources/images/kisspanda_net.png')
    toonova = xbmc.translatePath(path+'resources/images/toonova_net.png')
    toonget = xbmc.translatePath(path+'resources/images/toonget_net.png')
    theseriesonline = xbmc.translatePath(path+'resources/images/theseriesonline_net.png')
    watchcartoononline = xbmc.translatePath(path+'resources/images/watchcartoononline_com.png')
    watchcartoonsonline = xbmc.translatePath(path+'resources/images/watchcartoonsonline_eu.png')
    animetoon = xbmc.translatePath(path+'resources/images/animetoon.png')
    animewow = xbmc.translatePath(path+'resources/images/animewow.png')
    twentyfourseven = xbmc.translatePath(path+'resources/images/Live 24_7 Channels.png')
    requestedtitles = xbmc.translatePath(path+'resources/images/Requested Titles.png')
    universalsearch = xbmc.translatePath(path+'resources/images/Universal Search.png')
    allucsearch = xbmc.translatePath(path+'resources/images/Alluc Search.png')
    
    list_item = xbmcgui.ListItem(label='9Anime')
    list_item.setArt({'fanart':fanart,'thumb':icon})
    url = get_url(source='9Anime')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='9Cartoon')
    list_item.setArt({'fanart':fanart,'thumb':ninecartoon})
    url = get_url(source='9Cartoon')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='AnimeToon')
    list_item.setArt({'fanart':fanart,'thumb':animetoon})
    url = get_url(source='AnimeToon')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='AnimeWow')
    list_item.setArt({'fanart':fanart,'thumb':animewow})
    url = get_url(source='AnimeWow')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='B99')
    list_item.setArt({'fanart':fanart,'thumb':bninetynine})
    url = get_url(source='B99')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='CartoonCrazy')
    list_item.setArt({'fanart':fanart,'thumb':cartooncrazy})
    url = get_url(source='CartoonCrazy')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='CartoonsOn')
    list_item.setArt({'fanart':fanart,'thumb':cartoonson})
    url = get_url(source='CartoonsOn')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='GoStream')
    list_item.setArt({'fanart':fanart,'thumb':gostream})
    url = get_url(source='GoStream')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='KimCartoon')
    list_item.setArt({'fanart':fanart,'thumb':kimcartoon})
    url = get_url(source='KimCartoon')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='KissCartoon Eu')
    list_item.setArt({'fanart':fanart,'thumb':kisscartooneu})
    url = get_url(source='KissCartoonEu')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='KissCartoon So')
    list_item.setArt({'fanart':fanart,'thumb':kisscartoonso})
    url = get_url(source='KissCartoonSo')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='KissCartoon Io')
    list_item.setArt({'fanart':fanart,'thumb':kisscartoonio})
    url = get_url(source='KissCartoonIo')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='KissPanda')
    list_item.setArt({'fanart':fanart,'thumb':kisspanda})
    url = get_url(source='KissPanda')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Toonova')
    list_item.setArt({'fanart':fanart,'thumb':toonova})
    url = get_url(source='Toonova')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='Toonget')
    list_item.setArt({'fanart':fanart,'thumb':toonget})
    url = get_url(source='ToonGet')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='TheSeriesOnline')
    list_item.setArt({'fanart':fanart,'thumb':theseriesonline})
    url = get_url(source='TheSeriesOnline')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='WatchCartoonOnline')
    list_item.setArt({'fanart':fanart,'thumb':watchcartoononline})
    url = get_url(source='WatchCartoonOnline')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='WatchCartoonsOnline')
    list_item.setArt({'fanart':fanart,'thumb':watchcartoonsonline})
    url = get_url(source='WatchCartoonsOnline')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='WatchCartoons')
    list_item.setArt({'fanart':fanart,'thumb':icon})
    url = get_url(source='WatchCartoons')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)

    list_item = xbmcgui.ListItem(label='Live 24/7 Channels')
    list_item.setArt({'fanart':fanart,'thumb':twentyfourseven})
    url = get_url(source='Live247')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='Requested Titles')
    list_item.setArt({'fanart':fanart,'thumb':requestedtitles})
    url = get_url(source='RequestedTitles')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='[COLOR yellow]Universal Search[/COLOR]')
    list_item.setArt({'fanart':fanart,'thumb':universalsearch})
    url = get_url(source='Search',search='Universal')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='[COLOR yellow]Alluc Search[/COLOR]')
    list_item.setArt({'fanart':fanart,'thumb':allucsearch})
    url = get_url(source='Search',search='Alluc')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

params = dict(parse_qsl(sys.argv[2][1:]))
if not params: MAIN_MENU()
source = params.get('source')
settings = params.get('action')
link = params.get('link')
if source:
    Site = importlib.import_module('.'+source.lower(), package='resources.sources')
    Site.router(sys.argv[2][1:])
elif settings:
    if not link:
        import xbmcvfs
        dialog = xbmcgui.Dialog()
        if xbmcvfs.exists(cookie_file):
            xbmcvfs.delete(cookie_file)
            status = xbmcvfs.exists(cookie_file)
            if not status:
                d = dialog.ok('Cookie File Deleted','Existing cookie file successfully deleted. Image issues should now be resolved.')
            else:
                d = dialog.ok('Deletion Unsuccessful','Existing cookie file was not deleted.')
        else:
            d = dialog.ok('No File', 'No cookie file currently exists. The add-on will automatically create it when needed.')
    else:
        osWin = xbmc.getCondVisibility('system.platform.windows')
        osOsx = xbmc.getCondVisibility('system.platform.osx')
        osLinux = xbmc.getCondVisibility('system.platform.linux')
        osAndroid = xbmc.getCondVisibility('System.Platform.Android')

        if osOsx:    
            # ___ Open the url with the default web browser
            xbmc.executebuiltin("System.Exec(open "+link+")")
        elif osWin:
            # ___ Open the url with the default web browser
            xbmc.executebuiltin("System.Exec(cmd.exe /c start "+link+")")
        elif osLinux and not osAndroid:
            # ___ Need the xdk-utils package
            xbmc.executebuiltin("System.Exec(xdg-open "+link+")") 
        elif osAndroid:
            # ___ Open media with standard android web browser
            xbmc.executebuiltin("StartAndroidActivity(com.android.browser,android.intent.action.VIEW,,"+link+")")
            # ___ Open media with Mozilla Firefox
            xbmc.executebuiltin("StartAndroidActivity(org.mozilla.firefox,android.intent.action.VIEW,,"+link+")")                    
            # ___ Open media with Chrome
            xbmc.executebuiltin("StartAndroidActivity(com.android.chrome,,,"+link+")") 