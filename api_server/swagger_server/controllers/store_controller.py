from swagger_server.models.order import Order  # noqa: E501
from swagger_server import util
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

def delete_order(order_id):  # noqa: E501
    """Delete purchase order by ID

    For valid response try integer IDs with positive integer value.\\ \\ Negative or non-integer values will generate API errors # noqa: E501

    :param order_id: ID of the order that needs to be deleted
    :type order_id: int

    :rtype: None
    """
    return 'do some magic!'


def get_inventory():  # noqa: E501
    """Returns pet inventories by status

    Returns a map of status codes to quantities # noqa: E501


    :rtype: Dict[str, int]
    """
    url = connexion.request.url
    headers = connexion.request.headers
    print(headers)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    inventory = session.query(Pets.id, Pets.name, Pets.status, Tags.tag1, Tags.tag2, Photos.photo1, Photos.photo2).join(Tags).join(Photos).all()
    data_dict = {}
    for i in range(len(inventory)):
        
        data_dict.update ({
            inventory[i].id: {"name": inventory[i].name,
                              "status": inventory[i].status,
                              "tag1": inventory[i].tag1,
                              "tag2": inventory[i].tag2,
                              "photo1": inventory[i].photo1,
                              "photo2": inventory[i].photo2}
        })
    final_payload = {}
    for k,v in data_dict.items():
        if v["status"] == "available":
            final_payload.update ({
                k: v
            })
            
    print(final_payload)
    return final_payload


def get_order_by_id(order_id):  # noqa: E501
    """Find purchase order by ID

    For valid response try integer IDs with value &gt;&#x3D; 1 and &lt;&#x3D; 10.\\ \\ Other values will generated exceptions # noqa: E501

    :param order_id: ID of pet that needs to be fetched
    :type order_id: int

    :rtype: Order
    """
    return 'do some magic!'


def place_order(body):  # noqa: E501
    """Place an order for a pet

     # noqa: E501

    :param body: order placed for purchasing the pet
    :type body: dict | bytes

    :rtype: Order
    """
    if connexion.request.is_json:
        body = Order.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
