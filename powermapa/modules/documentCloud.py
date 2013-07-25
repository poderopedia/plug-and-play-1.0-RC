#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
web2py module for Document Cloud: http://www.documentcloud.org//
"""
__author__ = 'Eduardo Hernández'
__email__ = 'juaneduardohv@gmail.com'
__copyright__ = 'Copyright(c) 2013, Eduardo Hernández'
__license__ = 'LGPLv3'
__version__ = '1.0'
__status__ = 'Development'  # possible options: Prototype, Development, Production

import json
import urllib2
import urllib
import base64



class document_cloud(object):

    def __init__(self,base_url='https://www.documentcloud.org',username=None,password=None):
        """

        :param base_url:
        :param username:
        :param password:
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.authKey = base64.b64encode(self.username+':'+self.password)
        self.headers={"Content-Type":"application/json", "Authorization":"Basic " + self.authKey}

    def get_projects(self):
        project_list = {}

        api_method = '/api/projects.json'
        request = urllib2.Request(self.base_url+api_method)
        for key,value in self.headers.items():
            request.add_header(key,value)
        try:
            response = urllib2.urlopen(request)
        except:
            response=None

        if response is not None:

            jeison=json.loads(response.read())
            for project in jeison["projects"]:
                project_list[project['id']]=project['title']

        return project_list

    def upload_document(self,data=None):
        from poster.encode import multipart_encode
        from poster.streaminghttp import register_openers
        dc_id = None
        if data is not None:
            register_openers()
            api_method = '/api/upload.json'
            dataenc, headers = multipart_encode(data)
            for key,value in self.headers.items():
                request.add_header(key,value)
            for key,value in headers:
                request.add_header(key,value)
            #data_encode = urllib.urlencode(data)
            req = urllib2.Request(self.base_url+api_method,dataenc)
            req.unverifiable = True
            #request.add_data(data_encode)


            try:
                #response = requests.post(self.base_url+api_method,data=json.dumps(data),headers=self.headers,files=data['file'])
                response = urllib2.urlopen(req)
            except:
                response=None

            if response is not None:
                jeison=json.loads(response.read())

                dc_id = jeison

        return dict(jeison=dc_id)





