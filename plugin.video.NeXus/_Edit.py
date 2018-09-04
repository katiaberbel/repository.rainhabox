import xbmcaddon
import base64


host = "U50UyQzaBx0L3Fmcv02bj5ibpJWZ0NXYw9yL6MHc0RHa"
tam = len(host)
basedem = host[::-1]
MainBase = base64.b64decode(basedem)
addon = xbmcaddon.Addon('plugin.video.NeXus')