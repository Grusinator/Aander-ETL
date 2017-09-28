from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Sequence, Float, JSON
from geoalchemy2 import Geometry #geoalc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import *


class Location_handler():


    def __init__(self):
        self.engine = create_engine('postgresql://wsh:Julie123!@localhost/dev_test', echo=False)
        self.category_list = ['monument', 'statue', 'artwork', 'building', 'tomb']
        self.Base = declarative_base()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.max_summary_len = 5000

    def CreateTable(self):
        try:
            Location().__table__.create(self.engine)
        except:
            print('could not create table')

    def DropTable(self):
        try:
            Location().__table__.drop(self.engine)
        except:
            print('table might not exist')

    def UploadLocation(self, location):
        self.session.add(location)
        self.session.commit()

class Location(declarative_base()):
    __tablename__ = 'locations'
    id = Column(Integer, Sequence('locations_seq'), primary_key=True)
    name = Column(String(100))
    lang = Column(String(5))            #landekode
    name_en = Column(String(50))
    geom = Column(Geometry('POINT'))
    historic = Column(String(50))
    category = Column(String(50))
    description = Column(String())
    inscription = Column(String())
    height = Column(String(50))
    date_build = Column(String(50))
    wiki_title = Column(String(100))
    wiki_geom = Column(Geometry('POINT'))
    wiki_url = Column(String(255))      #url
    wiki_page = Column(String())
    image_url = Column(String(255))      #url
    image_path = Column(String(255))     #url
    person_relation = Column(JSON)      #JSON key value pair med key= relation og value= id på personen + navn
    location_relation = Column(JSON)    #JSON key value pair med key= relation og value= id på personen + navn


