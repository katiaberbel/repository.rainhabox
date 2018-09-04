from BeautifulSoup import BeautifulSoup
from urlparse import parse_qsl
from urllib import urlencode
import urlresolver
import xbmcplugin
import HTMLParser
import xbmcaddon
import urlparse
import requests
import xbmcgui
import urllib
import time
import json
import xbmc
import sys
import re

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)
path = 'special://home/addons/%s/' % addon_id
menu_icon = addon.getAddonInfo('icon')
fanart = addon.getAddonInfo('fanart')
icon = addon.getAddonInfo('icon')
addonname = addon.getAddonInfo('name')
base = 'https://9anime.to'
query = base+'/search?keyword=%s'
regulate = HTMLParser.HTMLParser()

def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def SOUPIFY(link):
    return BeautifulSoup(requests.get(link).content)

def MAIN_MENU():
    soup = SOUPIFY(base)

    list_item = xbmcgui.ListItem(label='Genres')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='9Anime', endpoint=base)
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='Newest')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='9Anime', endpoint=base+'/newest')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='Last Update')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='9Anime', endpoint=base+'/updated')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='Ongoing')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='9Anime', endpoint=base+'/ongoing')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='Most Watched')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='9Anime', endpoint=base+'/most-watched')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='Upcoming')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='9Anime', endpoint=base+'/upcoming')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    list_item = xbmcgui.ListItem(label='Schedule')
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='9Anime', endpoint=base+'/schedule?tz=')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_LIST(link):
    soup = SOUPIFY(link)
    shows = soup.findAll('div',{'class':'item'})
    if len(shows)>0:
        titles = ['%s (%s)'% (div.a.img['alt'], div.find('div',{'class':re.compile('^type\s')}).text) if div.find('div',{'class':re.compile('^type\s')})
                  else div.a.img['alt'] if div.a.find('img')
                  else div.a.text for div in shows]
        images = [div.find('img')['src'] for div in shows]
        links = [div.a['href'] for div in shows]
    else:
        shows = soup.findAll('div',{'class':re.compile('^item row')})
        titles = [div.find('div',{'class':'name'}).a.text for div in shows]
        images = [div.find('img',{'class':'thumb'})['src'] for div in shows]
        links = [div.find('div',{'class':'name'}).a['href'] for div in shows]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':images[i]})
        url = get_url(source='9Anime', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    GET_NEXT_PAGE(soup)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_GENRES(link):
    soup = SOUPIFY(link)
    cats = soup.find('ul',{'class':'sub'}).findAll('li')
    titles = [cat.a.text for cat in cats]
    links = [base+cat.a['href'] for cat in cats]
    
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='9Anime', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_SERVERS(link):
    soup = SOUPIFY(link)
    if 'There is no episodes for this anime, we will update asap!' in str(soup):
        dialog = xbmcgui.Dialog()
        d = dialog.ok('No Episodes','This site currently does not have any episodes/links for this series. Please check back at a later date.')
        quit()
    server_names = soup.find('div',{'id':'servers'}).findAll('label')
    server_containers = soup.findAll('div',{'class':re.compile('^server row')})
    servers = [l.text for l in server_names]
    titles = []
    links = []
    cover = soup.find('div',{'class':'cover'})['style'].replace("background-image: url('",'').replace("')",'')
    if cover == '': cover = menu_icon
    for s, server in enumerate(server_containers):
        for ep in server.findAll('li'):
            titles.append('%s (%s)'%(ep.a.text,servers[s]))
            links.append(base+ep.a['href'])
    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':cover})
        url = get_url(source='9Anime',state='play', endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_handle)

def CARTOON_SCHEDULE(link):
    soup = SOUPIFY(link)
    titles = []
    links = []
    month = soup.find('a',{'class':'current'}).text
    days = soup.find('div',{'class':'content'}).findAll('div',{'class':'day-block'})
    for day in days:
        if day.find('div',{'class':'inner'}):
            for item in day.findAll('div',{'class':'item'}):
                show = item.find('a',{'class':'name'}).text.encode('utf8').decode('ascii','ignore')
                episode = item.find('div',{'class':'release'}).text
                num_day = day.find('div',{'class':re.compile('^head')}).text
                num_day = '%s %s'%(num_day[0:2],num_day[2:])
                titles.append('%s (%s)'%(show+' '+episode,num_day))
                links.append(item.find('a',{'class':'name'})['href'])
    tz = soup.find('select',{'name':'tz'})
    if 'selected' in str(tz):
        for t in tz.findAll('option'):
            if 'selected' in str(t): 
                timezone = t.text
                break
    else: timezone = '(Default) EST'
    
    list_item = xbmcgui.ListItem(label='[COLOR yellow]%s TIMEZONE - (CLICK TO CHANGE)[/COLOR]'%timezone)
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='9Anime',endpoint=link,form='timezone')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    prev = soup.find('a',{'class':'prev'})
    list_item = xbmcgui.ListItem(label='[COLOR yellow] <<< PREVIOUS MONTH (%s)[/COLOR]'%prev.text.upper())
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='9Anime',endpoint=prev['href'])
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    list_item = xbmcgui.ListItem(label='[COLOR yellow]%s[/COLOR]'%month.upper())
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    xbmcplugin.addDirectoryItem(_handle, '', list_item, False)

    for i, link in enumerate(links):
        list_item = xbmcgui.ListItem(label=titles[i])
        list_item.setArt({'fanart':fanart,'thumb':menu_icon})
        url = get_url(source='9Anime',endpoint=link)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    next = soup.find('a',{'class':'next'})
    list_item = xbmcgui.ListItem(label='[COLOR yellow] NEXT MONTH (%s) >>>[/COLOR]'%next.text.upper())
    list_item.setArt({'fanart':fanart,'thumb':menu_icon})
    url = get_url(source='9Anime',endpoint=next['href'])
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)

def SCHEDULE_FORM(link):
    soup = SOUPIFY(link)
    tzs = soup.find('select',{'name':'tz'}).findAll('option')
    links = ['%s/schedule?tz=%s'%(base,o['value']) for o in tzs]
    zones = [o.text for o in tzs]
    dialog = xbmcgui.Dialog()
    ret = dialog.select('Choose a Timezone', zones)
    if ret > -1: CARTOON_SCHEDULE(links[ret])
    else: quit()

def GET_NEXT_PAGE(soup):
    pagination = soup.find('div',{'class':'paging'})
    if pagination is not None:
        next_page_span = pagination.find('span',{'class':'mr5'})
        if next_page_span is not None:
            try:
                next_page = base+'/'+pagination.findAll('a')[1]['href']
                list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
                list_item.setArt({'fanart':fanart,'thumb':menu_icon})
                url = get_url(source='9Anime', endpoint=next_page)
                xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
            except:
                pass

def PLAY_VIDEO(link):
    page_content = requests.get(link).content
    j_obj = json.loads(extract_9anime(link, page_content))
    print str(j_obj)
    if len(j_obj['params']) > 0:
        grab = json.loads(requests.get(j_obj['grabber'],params=urllib.urlencode(j_obj['params'])).content)
        titles = []
        links = []
        for link in grab['data']:
            titles.append(link['label'])
            links.append(link['file'])
        if len(links) > 1:
            dialog = xbmcgui.Dialog()
            ret = dialog.select('Choose a Stream', titles)
            if ret > -1:
                play_link = links[ret]
                title = titles[ret]
            else: quit()
        else:
            play_link = links[0]
            title = ''
    else:
        t = urllib.unquote(j_obj['target'])
        if t.startswith('//'): t = 'http:'+t
        print 'unquoted t : '+t
        if 'mycloud' in t:
            self_hosted = requests.get(t).content
            t_file = re.compile("""sources:\s*\[\{["']file["']:["'](.+?)["']\}\]""").findall(self_hosted)[0]
            if t_file.startswith('//'): play_link = 'http:'+t_file
            else: play_link = t
            play_link += '|User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36&Referer=%s' % t
        else: play_link = t
        title = ''
    print 'play_link before urlresolver : '+play_link
    if urlresolver.HostedMediaFile(play_link).valid_url():
        try:
            play_link = urlresolver.HostedMediaFile(play_link).resolve()
        except:
            play_link = play_link
    print 'play_link after urlresolver : '+play_link
    li = xbmcgui.ListItem(title)
    li.setPath(play_link)
    xbmc.Player().play(play_link, li, False)

def extract_9anime(url, page_content):
    episode_id = url.rsplit('/', 1)[1]
    url_info = urlparse.urlparse(url)
    domain = url_info.netloc
    scheme = url_info.scheme

    url_base = "%s://%s" % (scheme, domain)

    ts_value = re.compile(ur"<body.*data-ts\s*=['\"](\d+)['\"]").findall(page_content)[0]
    extra_param = get_extra_url_parameter(episode_id, 0, ts_value)

    url = "%s/ajax/episode/info?ts=%s&_=%d&id=%s&update=0" % (url_base, ts_value, extra_param, episode_id)
    time.sleep(0.3)
    return requests.get(url).content

def get_extra_url_parameter(id, update, ts):
    DD = 'gIXCaNh'
    params = [('id', str(id)), ('update', str(update)), ('ts', str(ts))]

    o = _s(DD)
    for i in params:
        o += _s(_a(DD + i[0], i[1]))

    return o

def _s(t):
    i = 0
    for (e, c) in enumerate(t):
        i += ord(c) * e
    return i

def _a(t, e):
    n = 0
    for i in range(max(len(t), len(e))):
        n += ord(e[i]) if i < len(e) else 0
        n += ord(t[i]) if i < len(t) else 0
    return format(n, 'x')  # convert n to hex string

def SEARCH(title):
    try:
        links = []
        soup = SOUPIFY(query % title)
        shows = soup.findAll('div',{'class':'item'})
        if len(shows)>0:
            titles = ['%s (%s) [COLOR blue]9ANIME[/COLOR]'% (div.a.img['alt'], div.find('div',{'class':re.compile('^type\s')}).text) if div.find('div',{'class':re.compile('^type\s')})
                      else div.a.img['alt']+' [COLOR blue]9ANIME[/COLOR]' if div.a.find('img')
                      else div.a.text+' [COLOR blue]9ANIME[/COLOR]' for div in shows]
            images = [div.find('img')['src'] for div in shows]
            links = [div.a['href'] for div in shows]
        else:
            shows = soup.findAll('div',{'class':re.compile('^item row')})
            titles = [div.find('div',{'class':'name'}).a.text+' [COLOR blue]9ANIME[/COLOR]' for div in shows]
            images = [div.find('img',{'class':'thumb'})['src'] for div in shows]
            links = [div.find('div',{'class':'name'}).a['href'] for div in shows]
    
        return zip(titles, images, links)
    except:
        link = []
        return links
        
def router(paramstring):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    if params:
        link = params.get('endpoint')
        play = params.get('state')
        form = params.get('form')
        if link == base: CARTOON_GENRES(base)
        elif not form is None: SCHEDULE_FORM(link)
        elif not play is None: PLAY_VIDEO(link)
        elif '/watch/' in link: CARTOON_SERVERS(link)
        elif '/schedule?' in link: CARTOON_SCHEDULE(link)
        elif not link is None: CARTOON_LIST(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        MAIN_MENU()

if __name__ == '__main__':
    router(sys.argv[2][1:])