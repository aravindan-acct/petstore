import connexion
import six
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from db.db import Users
from db.db import db_conn
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
import json

engine, Base = db_conn()

def create_user(body):  # noqa: E501
    """Create user

    This can only be done by the logged in user. # noqa: E501

    :param body: Created user object
    :type body: dict | bytes

    :rtype: None
    """
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    if connexion.request.is_json:
        #body = User.from_dict(connexion.request.get_json()) # noqa: E501
        body = connexion.request.get_json()

        print(dir(body))   
        print(type(body))
        username = body["username"]
        firstName = body["firstName"]
        lastName = body["lastName"]
        email = body["email"]
        password = body["password"]
        phone = body["phone"]

        # check if user exists
        i = session.query(Users).filter(Users.username == username).first()
        
        if i:
            return 'user exists', 404
        else:
            user = Users(username = username, firstName = firstName, lastName = lastName,
            email = email, password = generate_password_hash(password, method='sha256'))
            session.add(user)
            session.commit()
            return 'User Registered'


def create_users_with_array_input(body):  # noqa: E501
    """Creates list of users with given input array

     # noqa: E501

    :param body: List of user object
    :type body: list | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = [User.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def create_users_with_list_input(body):  # noqa: E501
    """Creates list of users with given input array

     # noqa: E501

    :param body: List of user object
    :type body: list | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = [User.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def delete_user(username):  # noqa: E501
    """Delete user

    This can only be done by the logged in user. # noqa: E501

    :param username: The name that needs to be deleted
    :type username: str

    :rtype: None
    """
    return 'do some magic!'


def get_user_by_name(username):  # noqa: E501
    """Get user by user name

     # noqa: E501

    :param username: The name that needs to be fetched. Use user1 for testing.
    :type username: str

    :rtype: User
    """
    path = connexion.request.path
    user_list = path.split('user/')
    user = user_list[1]
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    print(username)
    userObject = session.query(Users).filter(Users.username == username).first()
    print(userObject)
    print(userObject.get_id())
    result_dict = dict()
    if userObject:
        result_dict.update({"username": userObject.username})
        result_dict.update({"is_active": userObject.is_active})
        result_dict.update({"is_authenticated": userObject.is_authenticated})
        result_dict.update({"get_id": userObject.get_id()})
        result_dict.update({"firstName": userObject.firstName})
        result_dict.update({"lastName": userObject.lastName})
        result_dict.update({"phone": userObject.phone})
        
        return result_dict, 200
    else:
        
        return 'User does not exist', 404 


def login_user(username, password):  # noqa: E501
    """Logs user into the system

     # noqa: E501

    :param username: The user name for login
    :type username: str
    :param password: The password for login in clear text
    :type password: str

    :rtype: str
    """
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    userinfo = connexion.request.args
    username = userinfo['username']
    password = userinfo['password']
    i = session.query(Users).filter(Users.username == username).first()
    if  i:
        #check password
        if check_password_hash(i.password, password):
            
            return "password matches successfully", 200
        else:
            return "password does not match", 404
    else:
        return 'user does not exist', 404


def logout_user():  # noqa: E501
    """Logs out current logged in user session

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def update_user(body, username):  # noqa: E501
    """Updated user

    This can only be done by the logged in user. # noqa: E501

    :param body: Updated user object
    :type body: dict | bytes
    :param username: name that need to be updated
    :type username: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
