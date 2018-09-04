import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys
from resources.lib import dom_parser
from resources.lib import dom_parser2

AddonTitle        = "Kidz"
addon_id          = 'plugin.video.kidz'
fanarts           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon              = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
dialog            = xbmcgui.Dialog()

def MAIN_MENU():

    url = 'http://www.b99.tv'
    response = open_url(url)

    links = dom_parser2.parse_dom(response, 'li', {'class': re.compile('menu-item.+?')})
    for i in links[1:][:-4]:
        a = re.compile('<a href="(.+?)">(.+?)</a>').findall(i.content)
        for url,title in a:
            addDir(title,url,1,icon,fanarts)

def GET_LISTS(url):

    response = open_url(url)
    links = dom_parser2.parse_dom(response, 'article', {'class': re.compile('post-.+?')})

    if links:
        for i in links:
            url2      = dom_parser2.parse_dom(i.content, 'a', req='href')[0][0]['href']
            title       = dom_parser2.parse_dom(i.content, 'img', req='src')[0][0]['alt']
            iconimage = dom_parser2.parse_dom(i.content, 'img', req='alt')[0][0]['src']
            old = title
            title = dom_parser2.replaceHTMLCodes(title)
            if 'series' in url: addDir(title,url2,1,iconimage,fanarts)
            elif 'studios' in url: addDir(title,url2,1,iconimage,fanarts)
            else: addLink(title,url2,900,iconimage,fanarts)

    try:
        np = dom_parser2.parse_dom(response, 'link', {'rel': 'next'})[0][0]['href']
        addDir('[COLOR blue]Next Page -->[/COLOR]',np,1,icon,fanarts)
    except: pass

def PLAY_LINK(name,url,iconimage):

    response = open_url(url)

    i = dom_parser2.parse_dom(response, 'video', {'class': 'wp-video-shortcode'})[0]
    url = dom_parser2.parse_dom(i.content, 'a', req='href')[0][0]['href']
    
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    xbmc.Player ().play(url, liz, False)

def open_url(url):

    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
    response = urllib2.urlopen(req, timeout = 10)
    link=response.read()
    response.close()
    return link

def get_params():
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
    
def addDir(name,url,mode,iconimage,fanart,description=''):

    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setProperty( "fanart_Image", fanart )
    liz.setProperty( "icon_Image", iconimage )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name, url, mode, iconimage, fanart, description=''):

    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setProperty( "fanart_Image", fanart )
    liz.setProperty( "icon_Image", iconimage )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None; fanart=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass
 
if mode==None or url==None or len(url)<1: MAIN_MENU()

elif mode==1:GET_LISTS(url)
elif mode==900:PLAY_LINK(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
