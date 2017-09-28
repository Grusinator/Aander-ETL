import urllib
import os



from model.persons_datamodel import Person_handler, Person
from model.locations_datamodel import Location_handler, Location
from model.OSM_datamodel import OSM_handler, OSM_point

from lib.OSM_read import TransferOSMpoint2Location

from lib.g_vision_api_labels import detect_labels

from lib.wikipedia_read import TryFindWikiPage
from lib.tf_style_transfer import styletransferOnImage, save_image, save_image_sbs, load_image, save_image_sbs2


def LocationsAddWikiPage():

    print("transfer wiki info to locations")

    lh = Location_handler()


    query = lh.session.query(Location)#.filter(OSM_point.wikipedia != None)
    print(query.count())

    # start looking for wiki pages
    lang = 'dk'
    i = 0

    N = query.count()

    for location in query:


        #if allready has page then skip
        if location.wiki_title != None or location.wiki_page == "false":
            continue

        #construct list of names that we will try to find on wiki
        try_pages = [location.name]

        if location.name_en != None:
            try_pages.append(OSM_point.name_en)

        if location.wiki_page != None:
            page_title = location.wiki_page.split(':')[1]
            lang = location.wiki_page.split(':')[0]
            try_pages.insert(0, page_title)

        page = TryFindWikiPage(try_pages, lang, default_lang='dk')

        #if none found skip
        if page == None:
            location.wiki_page = "false"
            lh.session.commit()
            continue

        i += 1

        if i > 10:
            break

        try:
            print(page.category)
        except:
            pass


        max_summary_len = 5000
        summary = page.summary
        #truncate summary to 5000
        if len(summary) > max_summary_len:
            summary = summary[:max_summary_len - 1]

        wiki_img_url = None
        img_file_name = None
        # read image if exists
        if len(page.images) != 0:
            for url in page.images:

                #if type of image is not .svg, take the first
                ext = os.path.splitext(url)[1]
                if ext in ['.jpg', '.png', '.JPG', '.PNG']:
                    img_file_name = "data/images/OSM_wiki/%s%s" % (page.title, ext)
                    image = urllib.request.URLopener()
                    image.retrieve(url, img_file_name)
                    wiki_img_url = url
                    break

        try:
            wiki_geom = "Point(%.6f %.6f)" % (page.coordinates[0], page.coordinates[1])
        except:
            wiki_geom = None


        location.wiki_title = page.title
        location.wiki_url = page.url
        location.wiki_page = summary
        location.wiki_geom = wiki_geom
        location.image_url = wiki_img_url
        location.image_path = img_file_name

        lh.session.commit()


        print(i)


def location_image_labeling():

    print("loading attributes from images using google api")

    lh = Location_handler()


    query = lh.session.query(Location).filter(Location.image_path != None)
    print(query.count())


    monument_list = ['landmark', 'sculpture', 'monument', 'statue', 'fountain', 'ancient history','tourist attraction', 'memorial', 'stone carving', 'rock']

    construction_list = ['building', 'estate', 'mansion', 'fortification', 'castle', 'tower']

    person_list = ['human','person', 'gentleman', 'lady', 'portrait']


    i = 0

    N = query.count()

    for location in query:



        labels = detect_labels(location.image_path,disp = True)

        if any([l in monument_list for l in labels]):
            category = 'monument'

        elif any([l in construction_list for l in labels]):
            category = 'construction'

        elif any([l in person_list for l in labels]):
            category = 'person'
        else:
            category = 'not found'

        print(category)
        location.category = category


    lh.session.commit()

def styleTransfer():
    print("style transfer...")
    lh = Location_handler()

    mixed_path = 'data/images/style_mixed/'
    style_path = 'data/images/location_style/'

    query = lh.session.query(Location).filter(Location.image_path != None)#and_(Location.image_path != None, Location.category == 'monument'))
    for location in query:
        if location.image_path is None:
            continue

        try:
            #create style stransfer image
            style_image, style_src_img_path = styletransferOnImage(location.image_path)



        except BaseException as e:
            print('Style transfer failed: ' + str(e) + "\n... img.path: "+ location.image_path)


        if style_image is None:
            continue
        #basename of image
        loc_basename = os.path.basename(location.image_path)

        #only style image path
        style_path_full = os.path.join(style_path, loc_basename)

        #save image
        save_image(style_image, style_path_full)

        #save mixed path
        save_image_sbs2(
            os.path.join(mixed_path, loc_basename),
            location.image_path,
            style_path_full,
            style_src_img_path
            )


def main():
    #TransferOSMpoint2Location()
    #LocationsAddWikiPage()
    #location_image_labeling()
    styleTransfer()

if __name__ == "__main__":
    main()