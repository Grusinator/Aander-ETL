import os
import urllib

from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

from lib.util_functions import TryFindWikiPage
from model.locations_datamodel import Location_handler, Location

image_folder = ""

lh = Location_handler()

Base = declarative_base()

class OSM_point(Base):
    __tablename__ = 'OSM_points'
    id = Column(Integer, Sequence('OSM_points_seq'), primary_key=True)
    geom = Column(Geometry('POINT'))
    full_id = Column(String(50))
    osm_id = Column(String(50))
    historic = Column(String(50))
    name = Column(String(50))
    tourism = Column(String(50))
    inscriptio = Column(String(50))
    material = Column(String(50))
    subject_wi = Column(String(50))
    wikidata = Column(String(50))
    start_date = Column(String(50))
    wikipedia = Column(String(50))
    name_en = Column(String(50))
    image = Column(String(50))
    descriptio = Column(String(50))
    height = Column(String(50))
    memorial = Column(String(50))
    date = Column(String(50))
    mapillary = Column(String(50))
    wikimedia_ = Column(String(50))


query = lh.session.query(OSM_point)#.filter(OSM_point.wikipedia != None)
print(query.count())




#start looking for wiki pages
lang = 'dk'
i = 0

N = query.count()
for OSM_point in query:
    try_pages = [OSM_point.name, OSM_point.name_en]
    if OSM_point.wikipedia != None:
        page_title = OSM_point.wikipedia.split(':')[1]
        lang = OSM_point.wikipedia.split(':')[0]
        try_pages.insert(0, page_title)
    
    page = TryFindWikiPage(try_pages, lang, default_lang='dk')
    
    if page == None:
        continue
    
    i += 1
    
    summary = page.summary

    if len(summary) > lh.max_summary_len:
        summary = summary[:lh.max_summary_len-1]

    wiki_img_url = None
    #read image if exists
    if len(page.images) != 0:
        for url in page.images:

            ext = os.path.splitext(url)[1]
            if ext in ['.jpg', '.png', '.JPG', '.PNG']:
                img_file_name = "data/images/OSM_wiki/%s%s" %(OSM_point.osm_id, ext)
                image=urllib.request.URLopener()
                image.retrieve(url,img_file_name)
                wiki_img_url = url
                break

    try:
        wiki_geom = "Point(%.6f %.6f)" %(page.coordinates[0],page.coordinates[1])
    except:
        wiki_geom = None

    location = Location(
        name = OSM_point.name,
        lang = lang,            #landekode
        name_en = OSM_point.name_en,
        geom = OSM_point.geom,
        historic = OSM_point.historic,
        category = OSM_point.tourism,
        description = OSM_point.descriptio,
        inscription = OSM_point.inscriptio,
        height = OSM_point.height,
        date_build = OSM_point.date,
        wiki_title = page.title,
        wiki_url = wiki_img_url,           #url
        wiki_page = summary,
        wiki_geom = wiki_geom,
        image_url = wiki_img_url,   #url 
        image_path = img_file_name, #url 
        person_relation = None,      #JSON key value pair med key= relation og value= id på personen + navn
        location_relation = None 
    )
    lh.UploadLocation(location)

    print(i)