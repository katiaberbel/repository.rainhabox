from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from concurrent.futures import as_completed
from resources import sources
import xbmcaddon
import importlib
import urllib

addon_id = 'plugin.video.cartooncrazy'
addon = xbmcaddon.Addon(id=addon_id)

class Sites:
    def __init__(self):
        self.sources = []
        self.checkingenabled = sources.__all__
        self.sources = [src for src in self.checkingenabled if addon.getSetting(src) == 'true']
        self.links = []
        
    def search(self, term):
        pool = ThreadPoolExecutor(len(self.sources)) # 1 per source
        cleaned = ''.join([x for x in term.replace('&','and') if any([x.isalnum(), x.isspace()])])
        futures = [pool.submit(self.thread, source, urllib.quote(term)) if not any([source in s for s in ['toonova','9cartoon','kisscartooneu','kisscartoonso','kisspanda','animetoon','toonget','animewow','watchcartoonsonline','watchcartoononline','9anime']]) 
                   else pool.submit(self.thread, source, urllib.quote_plus(cleaned)) if source == '9cartoon'
                   else pool.submit(self.thread, source, urllib.quote_plus(term)) for source in self.sources]
        [self.links.extend(r.result()) for r in as_completed(futures)]
        print list(self.links)
        return self.links
        
    def thread(self, source, term):
        print '=====searching for ({}) on ({})====='.format(term,source)
        source = importlib.import_module('.'+source, package='resources.sources')
        return source.SEARCH(term)