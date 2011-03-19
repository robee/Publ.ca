import cgi
import os
import uuid
import logging
from google.appengine.ext import db



class Pub(db.Model):
    pub_id = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    date_published = db.DateTimeProperty(auto_now_add=True)
    twitter_user = db.StringProperty(required=False)
    bitly_user = db.StringProperty(required=False)
    
    
    @staticmethod
    def create_pub(title_arg, author_arg, content_arg):
        
        newPub = Pub(pub_id= getUniqueId(), title=title_arg, content=content_arg, author=author_arg)
            
        newPub.put()
        return newPub
    
    @staticmethod
    def get_by_id(pub_id):
        logging.info('Models.py - pub_id: %s' % pub_id)
        return Pub.all().filter('pub_id = ', pub_id).get()
       
    @staticmethod
    def get_by_title(title):
        return Pub.all().filter('title = ', title).get()

    @staticmethod
    def get_by_author(author):
        return Pub.all().filter('author = ', author).get() 
       
       
def getUniqueId():
    """Generate 4 character hex endcoded string as
       a random identifier for offer, with collision detection"""
    pub_id = uuid.uuid4().hex[:4]
    
    existingPub = Pub.get_by_id(pub_id)
    
    if existingPub:
        generate_uuid()
    
    return pub_id