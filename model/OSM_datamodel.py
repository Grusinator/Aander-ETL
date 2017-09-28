from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Sequence, Float, JSON
from geoalchemy2 import Geometry #geoalc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class OSM_handler():


    def __init__(self):
        self.engine = create_engine('postgresql://wsh:Julie123!@localhost/dev_test', echo=False)
        self.Base = declarative_base()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def CreateTable(self):
        try:
            OSM_point().__table__.create(self.engine)
        except:
            print('could not create table')

    def DropTable(self):
        try:
            OSM_point().__table__.drop(self.engine)
        except:
            print('table might not exist')


class OSM_point(declarative_base()):
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