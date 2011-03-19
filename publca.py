#!/usr/bin/env python

import sys
import os
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import util
from google.appengine.api import mail

from constants import *
from models import Pub

# This hack is here because we want to accept HTML but not javascript content.  Fix for this coming soon.
def CheckRequest(inFunction):
    """Checks for Javascript injection """
    def outFunction(*args,**kwargs):
         
        webAppRequest = args[0] # the first argument in get/post is self - This should work - There is probably a better way to do this.
        arguments = webAppRequest.request.arguments()
        
        for argument in arguments:
            argValue = webAppRequest.request.get(argument)
            
            # Check if trying to access someone elses offers - FIX THIS
           
                
            if '<script' in argValue or '< script' in argValue:
                 
               webAppRequest.redirect('/')
               return
                
        return inFunction(*args,**kwargs)
    
    return outFunction

class HomeHandler(webapp.RequestHandler):
    def get(self):
        logging.info('Cookies: %s - self.request.cookies')
        content_template_values = {
                
        }
        
        self.response.out.write(
            RenderPage('index.html', content_template_values)
        )

class PubHandler(webapp.RequestHandler):
    def get(self, pub_id):
        
        pub = Pub.get_by_id(pub_id)
        
        if pub:
        
            content_template_values = {
                'title':pub.title,
                'author':pub.author,
                'content':pub.content,
                'date':pub.date_published.date().isoformat()
            }
       
        else:
            content_template_values = {
                   'title': 'Sorry No Publication Here',
                   'author':'No one',
                   'content':'Try Something else',
                   'date':'Never'
            }
        self.response.out.write(
            RenderPage('text.html', content_template_values)
        )

  
            
class FavHandler(webapp.RequestHandler):
    def get(self):
        pass    


class CreateHandler(webapp.RequestHandler):
    
    @CheckRequest
    def post(self):
        
        title = self.request.get('title_form')
        author = self.request.get('author_form')
        content = self.request.get('content_form')
        email = self.request.get('email_form')
        
        
        if title == '':
            title = 'Untitled'
        
        if author == '':
            author = 'Anonymous'
        
        if content == '':
            content = 'Nothing To Say'
        
        content = "<br/>".join(content.split("\n"))
        new_pub = Pub.create_pub(title, author, content)
        
        
        if email:
            mail.send_mail(sender="Publca <mr.rossrobinson@gmail.com>",
                      to=email,
                      subject='Publca - %s'% new_pub.title ,
                      body= 'publ.ca/%s'% new_pub.pub_id )
        
        self.redirect('/%s'% new_pub.pub_id )
       
       
class LandingHandler(webapp.RequestHandler):
    def get(self):
        
        self.response.out.write(RenderPage('landing.html', {}))
 
# Helpers
# NOTE: this is overkill and will be more useful when we have constants that need to be added to each page
def RenderPage(template_file_name, content_template_values):
    """This re-renders the full page with the specified template."""
    
    main_path = os.path.join('templates/%s' % template_file_name)
    
    content_template_values.update(willetJS = WILLET_JS)
    content_template_values.update(willetOfferId = WILLET_OFFER_ID)
    willetOfferId = 'bbf81b0b8114d7e9'
    
    # Add constant things to content_template_values
    return template.render(main_path, content_template_values)



appRoute = webapp.WSGIApplication( [    ('/favicon.ico', FavHandler),
                                        ('/create', CreateHandler),
                                        ('/write', HomeHandler),
                                        ('/', LandingHandler), 
                                        (r'/(.*)', PubHandler)
                                     ],debug=True)
										
def main():
    run_wsgi_app(appRoute)

if __name__ == '__main__':
    main()
