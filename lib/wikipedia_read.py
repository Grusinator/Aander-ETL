import wikipedia
import os
import urllib


def TryFindWikiPage(pagename, lang, default_lang = 'en'):
    
    default_lang_list = ['dk', 'en', 'es', 'de', 'sv', 'no']

    if not isinstance(pagename, list):
        pagename = [pagename]

    if isinstance(lang, list):
        lang = lang.append(default_lang)
    else:
        lang = [lang, default_lang]

    for l in lang:
        if l in default_lang_list:
            wikipedia.set_lang(l)
        else:
            continue

        for name in pagename:
            if name is None:
                pass
            try:
                page = wikipedia.page(title=pagename)
            except:
                pass
            else:
                return page
            
    return None

def saveImageFromWikiUrl(url, filename, title):
    ext = os.path.splitext(url)[1]
    if ext in ['.jpg', '.png', '.JPG', '.PNG']:
        img_file_name = "data/images/OSM_wiki/%s%s" % (title, ext)
        image = urllib.request.URLopener()
        image.retrieve(url, img_file_name)

    return

