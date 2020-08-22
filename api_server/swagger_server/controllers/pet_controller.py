import connexion
import six
import json
from db.db import Pets
from db.db import Tags
from db.db import Photos
from db.db import db_conn
from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.pet import Pet  # noqa: E501
from swagger_server import util
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import re

engine, Base = db_conn()

def url_processor(url):
    url_list = url.split("pet/")
    pet_id = int(url_list[1])
    return pet_id

def add_pet(body):  # noqa: E501
    """Add a new pet to the store

     # noqa: E501

    :param body: Pet object that needs to be added to the store
    :type body: dict | bytes

    :rtype: None
    """
    body = connexion.request.form
    for k,v in body.items():
        print("{}:{}".format(k,v))
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    pet = Pets(name = body['name'], status = body['status'])
    
    tags = body['tags']
    print("Tags type is {}".format(type(tags)))
    
    if type(tags) != list:

        tags_list = tags.split(',')
        print(tags_list)
        tag1 = tags_list[0]
        tag2 = tags_list[1]
        newtag1 = tag1.strip('"[] ')
        newtag1_1 = newtag1.strip("'")
        newtag2 = tag2.strip('"[] ')
        newtag2_1 = newtag2.strip("'")
        print(newtag1)
        print(newtag2)
    
    #tags_list = re.split(r"\W+", tags)
    #tags = [ tags_list[i] for i in range(len(tags_list)) if tags_list[i]]
    #print(tags)
    
    #   pet.Tags = [Tags(tag1 = tags[0]), Tags(tag2 = tags[x1])]

    photoUrls = body['photoUrls']
    print("PhotoURL type is {}".format(type(photoUrls)))
    if type(photoUrls) != list:
        photoslist = photoUrls.split(',')
        photo1 = photoslist[0]
        photo2 = photoslist[1]
        newphoto1 = photo1.strip('"[] ')
        newphoto1_1 = newphoto1.strip("'")
        newphoto2 = photo2.strip('"[] ')
        newphoto2_1 = newphoto2.strip("'")
    #photo_list = re.split(r"\W+", photoUrls)
    #photos = [ photo_list[i] for i in range(len(photo_list)) if photo_list[i]]
    #print(photos)
    
    pet.Tags = [Tags(tag1 = newtag1_1, tag2 = newtag2_1)]
    pet.Photos = [Photos(photo1 = newphoto1_1, photo2 = newphoto2_1)]
    
    
    session.add(pet)
    session.commit()
    
    if connexion.request.is_json:
        body = Pet.from_dict(connexion.request.get_json())  # noqa: E501
    return json.dumps(body)


def delete_pet(pet_id, api_key=None):  # noqa: E501
    """Deletes a pet

     # noqa: E501

    :param pet_id: Pet id to delete
    :type pet_id: int
    :param api_key: 
    :type api_key: str

    :rtype: None
    """
    url = connexion.request.url
    pet_id = url_processor(url)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    pet_delete = session.query(Pets).get(pet_id)

    session.delete(pet_delete)
    session.commit()

    return 'Deleted Successfully'


def find_pets_by_status(status):  # noqa: E501
    """Finds Pets by status

    Multiple status values can be provided with comma separated strings # noqa: E501

    :param status: Status values that need to be considered for filter
    :type status: List[str]

    :rtype: List[Pet]
    """
    status = connexion.request.args
    result_dict = dict()
    row_list = list()
    for k,v in status.items():
        print(k)
        print(v)
        conn = engine.connect()
        Session = sessionmaker(bind=engine)
        Session.configure(bind=engine)
        session = Session()
        for id in session.query(Pets.id).filter(Pets.status == v):
            print(id[0])    
            result = session.query(Pets.name, Tags.tag1, Tags.tag2, Photos.photo1, Photos.photo2, Pets.status).join(Tags).join(Photos).filter(Tags.pet_id == id[0]).all()
            pet_key = "pet_key"+str(id[0])
            result_dict.update({pet_key: result})
    
        print(type(result_dict))
        session.close()
    return result_dict


def find_pets_by_tags(tags):  # noqa: E501
    """Finds Pets by tags

    Muliple tags can be provided with comma separated strings. Use\\ \\ tag1, tag2, tag3 for testing. # noqa: E501

    :param tags: Tags to filter by
    :type tags: List[str]

    :rtype: List[Pet]
    """
    return 'do some magic!'


def get_pet_by_id(pet_id):  # noqa: E501
    """Find pet by ID

    Returns a single pet # noqa: E501

    :param pet_id: ID of pet to return
    :type pet_id: int

    :rtype: Pet
    """
    url = connexion.request.url
    print(url)
    pet_id = url_processor(url)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    result_dict = dict()
    try:
        for id in session.query(Pets.id).filter(Pets.id == pet_id):
            result = session.query(Pets.name, Tags.tag1, Tags.tag2, Photos.photo1, Photos.photo2).join(Tags).join(Photos).filter(Pets.id == pet_id).all()
            result_dict.update({pet_id: result})
            return result_dict
    except: 
        return "Object Not Found"


def update_pet(body):  # noqa: E501
    """Update an existing pet

     # noqa: E501

    :param body: Pet object that needs to be added to the store
    :type body: dict | bytes

    :rtype: None
    """
    url = connexion.request.url
    body = connexion.request.form
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    payload = {}
    for k,v in body.items():
        payload.update({k : v})
    

    print("payload is {}".format(payload))
    pet_id = payload["id"]
    for id in session.query(Pets.id).filter(Pets.id == pet_id): 
        #result = session.query(Pets.name, Tags.tag1, Tags.tag2, Photos.photo1, Photos.photo2).join(Tags).join(Photos).filter(Tags.pet_id == id[0]).all()
        result = session.query(Pets, Tags, Photos).filter(Pets.id == pet_id ).filter(Tags.pet_id == pet_id).filter(Photos.pet_id == pet_id).all()
        print("size of result object is {}".format(result))
        print("size of result object is {}".format(len(result)))    
        print(result[0].Pets.name)
           
        if "name" in payload:
            result[0].Pets.name = payload["name"]
        if "status" in payload:
            result[0].Pets.status = payload["status"]
        
        
        #pet = Pets(name = body['name'], status = body['status'])
        #pet.Tags = [Tags(tag1 = newtag1_1, tag2 = newtag2_1)]
        #pet.Photos = [Photos(photo1 = newphoto1_1, photo2 = newphoto2_1)]

        if "tags" in payload:
            newtag = payload["tags"].strip('"[] ')

            tags_list = payload["tags"].split(',')
            print(len(tags_list))
            if len(tags_list) != 0:
                newtag_list=list()
                for i in range(len(tags_list)):
                    element_append=tags_list[i].strip('"[] ')
                    element_append_1 = element_append.strip("'")
                    newtag_list.append(element_append_1)
                print("newtag_list is {}".format(newtag_list))
            if len(newtag_list) == 1:    
                tag_sql_query = "[Tags(tag1 ="+newtag_list[0]+")]"
                #pet.Tags = tag_sql_query
                #session.add(tag)
                result[0].Tags.tag1 = newtag_list[0]
            else:
                tag_sql_query = "[Tags(tag1 ="+newtag_list[0]+", tag2 = "+newtag_list[1]+")]"
                #pet.Tags = tag_sql_query
                #session.add(tag)
                result[0].Tags.tag1 = newtag_list[0]
                result[0].Tags.tag2 = newtag_list[1]
        if "photoUrls" in payload:
            newphoto = payload["photoUrls"].strip('"[] ')
            photoslist = newphoto.split(',')
            
            newphoto.strip("'")
            print(newphoto)
            if len(photoslist) != 0:
                newphotoslist = list()
                for i in range(len(photoslist)):
                    photo_element_append = photoslist[i].strip('["] ')
                    photo_element_append_1 = photo_element_append.strip("'")
                    newphotoslist.append(photo_element_append_1)
                    
                print("photoslist is {}".format(newphotoslist))
            if len(newphotoslist) == 1:
                photos_sql_query="[Photos(photo1 ="+newphotoslist[0]+")]"
                #pet.Photos = photos_sql_query
                #session.add(photos)
                result[2].Photos.photo1 = newphotoslist[0]
            else:
                photos_sql_query="[Photos(photo1 ="+newphotoslist[0]+", photo2 = "+newphotoslist[1]+")]"
                #pet.Photos = photos_sql_query
                #session.add(photos)
                print(newphotoslist[0])
                print(newphotoslist[1])
                result[0].Photos.photo1 = newphotoslist[0]
                result[0].Photos.photo2 = newphotoslist[1]
                print("Data updated")
        try:
            session.commit()
            return 'Transaction Successful', 200
        except:

            return 'Transaction Unsuccessful', 404
        
    return 'do some magic'

def update_pet_with_form(pet_id, name=None, status=None):  # noqa: E501
    """Updates a pet in the store with form data

     # noqa: E501

    :param pet_id: ID of pet that needs to be updated
    :type pet_id: int
    :param name: 
    :type name: str
    :param status: 
    :type status: str

    :rtype: None
    """
    return 'do some magic!'


def upload_file(pet_id, body=None):  # noqa: E501
    """uploads an image

     # noqa: E501

    :param pet_id: ID of pet to update
    :type pet_id: int
    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponse
    """
    if connexion.request.is_json:
        body = Object.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
