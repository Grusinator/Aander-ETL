
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Sequence, Float, JSON
from geoalchemy2 import Geometry #geoalc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import *

import json
import enum





class Person_handler():
    def __init__(self):
        self.engine = create_engine('postgresql://wsh:Julie123!@localhost/dev_test', echo=False)
        self.category_list = ['monument', 'statue', 'artwork', 'building', 'tomb']
        self.Base = declarative_base()

    def CreateTable(self):
        try:
            Person().__table__.create(self.engine) 
        except:
            print('could not create table')

    def DropTable(self):
        try:
            Person().__table__.drop(self.engine)
        except:
            print('could not create table')


class MyEnum(enum.Enum):
    Father = 1
    Mother = 2
    Sister = 3
    Brother= 4
    Son = 5
    Daughter = 6

class Person(declarative_base()):
    __tablename__ = 'persons'
    id = Column(Integer, Sequence('persons_seq'), primary_key=True)
    name = Column(String(100))
    lang = Column(String(5))            #landekode
    born_t = Column(String(50))         #dato
    born_g = Column(Geometry('POINT'))  #geolokation
    died_t = Column(String(50))         #dato
    died_g = Column(Geometry('POINT'))  #geolokation
    burried = Column(Geometry('POINT')) #geolokation
    wiki_title = Column(String(50))
    wiki_url = Column(String(50))      #url
    wiki_page = Column(String())
    image_url = Column(String(50))      #url 
    image_path = Column(String(50))     #url 
    relatives = Column(JSON)            #JSON key value pair med key= relation og value= id på personen + navn
    quotes = Column(ARRAY(String(100)))




