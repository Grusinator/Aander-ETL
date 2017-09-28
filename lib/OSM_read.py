
import overpy

from model.persons_datamodel import Person_handler, Person
from model.locations_datamodel import Location_handler, Location
from model.OSM_datamodel import OSM_handler, OSM_point

from lib.wikipedia_read import TryFindWikiPage

def TransferOSMpoint2Location():

    print("transfer data from OSM table to locations")

    osmh = OSM_handler()




    osm_query = osmh.session.query(OSM_point)#.filter(osm_point.wikipedia != None)
    print(osm_query.count())

    lh = Location_handler()

    loc_query = lh.session.query(Location)

    loc_list = [loc.name for loc in loc_query]

    i = 1

    for osm_point in osm_query:

        #if allready exists in database
        if osm_point.name == None or osm_point.name in loc_list:
            continue

        location = Location(
            name=osm_point.name,
            lang=None,  # landekode
            name_en=osm_point.name_en,
            geom=osm_point.geom,
            historic=osm_point.historic,
            category=osm_point.tourism,
            description=osm_point.descriptio,
            inscription=osm_point.inscriptio,
            height=osm_point.height,
            date_build=osm_point.date,
            wiki_title=None,
            wiki_url=None,  # url
            wiki_page=osm_point.wikipedia,
            wiki_geom=None,
            image_url=None,  # url
            image_path=None,  # url
            person_relation=None,  # JSON key value pair med key= relation og value= id på personen + navn
            location_relation=None
        )
        lh.UploadLocation(location)

        i+= 1

        print(i)


def ReadFromAPI(attributes = None,bbox = None):

    lh = Location_handler()

    loc_query = lh.session.query(Location)

    loc_list = [loc.name for loc in loc_query]



    queue_string = "node"
    if isinstance(attributes, dict):
        for key_att in attributes:
            if attributes[key_att] == None:
                queue_string += "[%s]" % (key_att)
            else:
                queue_string += "[%s=%s]"%(key_att, attributes[key_att])


    if bbox != None:
        if len(bbox) == 4:
            bbox = list(map(str, bbox))
            queue_string += "(%s)" %(','.join(bbox))

    queue_string += """;out;"""

    limits = """[timeout: 900][maxsize: 1073741824]"""


    api = overpy.Overpass()

    #queue = """node["name"~"holtorf$"](50.7,7.1,50.8,7.25);out body;"""
    #que1 = """node["historic"="memorial"];out body;"""


    #bbox = (54.35692, 7.97433, 55.82350, 9.72176)


    #node["historic" = "memorial"](54.35692, 7.97433, 55.82350, 9.72176);out body;

    #filters: http://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide

    result = api.query(queue_string)


    i = 1
    for node in result.nodes:

        location = Location()

        print(node.id)
        print(str(node.lat) + ": " + str(node.lon))
        if len(node.tags) > 0:
            if not "name" in node.tags:
                continue

            for key in node.tags:
                #print(key)

                print(node.tags[key])
                if key == "name":
                    location.name = node.tags[key]
                    # if allready exists in database
                    if location.name in loc_list:
                        continue
                elif key == "name_en":
                    location.name_en = node.tags[key]
                elif key == "historic":
                    location.historic = node.tags[key]
                elif key == "tourism":
                    location.tourism = node.tags[key]
                elif key == "descriptio":
                    location.description = node.tags[key]
                elif key == "inscriptio":
                    location.inscription = node.tags[key]
                elif key == "height":
                    location.height = node.tags[key]
                elif key == "date":
                    location.date_build = node.tags[key]

        if location.name == None:
            continue
        lh.UploadLocation(location)

        i+= 1

        print(i)


    return


def main():
    #TransferOSMpoint2Location()

    attributes = {"historic":None}
    bbox = [54.35692, 7.97433, 57.95903, 13.02223]

    ReadFromAPI(attributes=attributes, bbox=bbox)

if __name__ == "__main__":
    main()
