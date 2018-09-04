import xbmc
import os
import webbrowser


def browser_player(os,link):

    if os =='android':
        links = xbmc . executebuiltin ( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( ''+link+'' ) )
    else:
        links = webbrowser . open ( ''+link+'' )



link = "https://pipocaflix.com/login.php"

if xbmc . getCondVisibility ('system.platform.android'):
    os = 'android'
else:
    os = 'null'

browser_player(os,link)





