'''

Copyright (C) 2017 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2017 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from sregistry.logger import bot
from sregistry.auth import read_client_secrets
from sregistry.main import ApiConnection
import json
import sys
import os

from .auth import authorize
from .pull import pull
from .push import push
from .delete import remove
from .query import *

class Client(ApiConnection):

    def __init__(self, secrets=None, base=None, **kwargs):
 
        super(ApiConnection, self).__init__(**kwargs)
        self.base = base
        self.update_secrets()
        self.update_headers()
        self.update_base() 

    def update_base(self):
        if self.base is not None:
            if not self.base.endswith('api'):
                self.base = '%s/api' %self.base.strip('/')


    def read_response(self,response, field="detail"):
        '''attempt to read the detail provided by the response. If none, 
        default to using the reason'''

        try:
            message = json.loads(response._content.decode('utf-8'))[field]
        except:
            message = response.reason
        return message


    def update_secrets(self):
        '''update secrets will take a secrets credential file
        either located at .sregistry or the environment variable
        SREGISTRY_CLIENT_SECRETS and update the current client 
        secrets as well as the associated API base.
        '''
        self.secrets = read_client_secrets()
        if self.secrets is not None:
            if "base" in self.secrets:
                self.base = self.secrets['base']
                self.update_base()

    def __str__(self):
        return "sregistry.client.%s" %(self.base)
    

Client.authorize = authorize
Client.ls = ls
Client.remove = remove
Client.pull = pull
Client.push = push
Client.search = search
Client.collection_search = collection_search
Client.container_search = container_search
Client.label_search = label_search
