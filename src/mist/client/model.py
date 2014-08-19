import json
from mist.client.helpers import RequestsHandler


class Backend(object):
    """

    """
    def __init__(self, backend, mist_client):
        self.mist_client = mist_client
        self.info = backend
        self.title = backend['title']
        self.id = backend['id']
        self.enabled = backend['enabled']
        self.provider = backend['provider']
        self.api_token = self.mist_client.api_token

        self._machines = None

    def __str__(self):
        return "%s => %s:%s" % (self.__class__.__name__, self.title, self.id)

    def __repr__(self):
        return "%s => %s:%s" % (self.__class__.__name__, self.title, self.id)

    def request(self, *args, **kwargs):
        """
        The main purpose of this is to be a wrapper-like function to pass the api_token and all the other params to the
        requests that are being made

        :returns: An instance of RequestsHandler
        """
        return RequestsHandler(*args, api_token=self.api_token, **kwargs)

    def delete(self):
        req = self.request(self.mist_client.uri + '/backends/' + self.id)
        req.delete()
        self.mist_client.update_backends()

    def rename(self, new_name):
        payload = {
            'new_name': new_name
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri + '/backends/' + self.id, data=data)
        req.put()
        self.title = new_name
        self.mist_client.update_backends()

    def enable(self):
        payload = {
            "new_state": "1"
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri+'/backends/'+self.id, data=data)
        req.post()
        self.enabled = True
        self.mist_client.update_backends()

    def disable(self):
        payload = {
            "new_state": "0"
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri+'/backends/'+self.id, data=data)
        req.post()
        self.enabled = False
        self.mist_client.update_backends()

    @property
    def sizes(self):
        req = self.request(self.mist_client.uri+'/backends/'+self.id+'/sizes')
        sizes = req.get().json()
        return sizes

    @property
    def locations(self):
        req = self.request(self.mist_client.uri+'/backends/'+self.id+'/locations')
        locations = req.get().json()
        return locations

    @property
    def images(self):
        req = self.request(self.mist_client.uri+'/backends/'+self.id+'/images')
        images = req.get().json()
        return images

    def search_image(self, search_term):
        payload = {
            'search_term': search_term
        }
        data = json.dumps(payload)

        req = self.request(self.mist_client.uri+'/backends/'+self.id+'/images', data=data)
        images = req.get().json()
        return images

    def _list_machines(self):
        req = self.request(self.mist_client.uri+'/backends/'+self.id+'/machines')
        machines = req.get().json()

        if machines:
            for machine in machines:
                self._machines[machine['name']] = Machine(machine, self)
        else:
            self._machines = {}

    @property
    def machines(self):
        if self._machines is None:
            self._machines = {}
            self._list_machines()

        return self._machines

    def update_machines(self):
        self._machines = {}
        self._list_machines()
        return self._machines


class Machine(object):
    def __init__(self, machine, backend):
        self.backend = backend
        self.mist_client = backend.mist_client
        self.info = machine
        self.api_token = self.mist_client.api_token
        self.name = machine['name']
        self.id = machine['id']

    def __str__(self):
        return "%s => %s:%s" % (self.__class__.__name__, self.name, self.id)

    def __repr__(self):
        return "%s => %s:%s" % (self.__class__.__name__, self.name, self.id)

    def request(self, *args, **kwargs):
        """
        The main purpose of this is to be a wrapper-like function to pass the api_token and all the other params to the
        requests that are being made

        :returns: An instance of RequestsHandler
        """
        return RequestsHandler(*args, api_token=self.api_token, **kwargs)


class Key(object):
    def __init__(self, key, mist_client):
        self.mist_client = mist_client
        self.api_token = self.mist_client.api_token
        self.id = key['id']
        self.is_default = key['isDefault']
        self.info = key

    def __str__(self):
        return "%s => %s" % (self.__class__.__name__, self.id)

    def __repr__(self):
        return "%s => %s" % (self.__class__.__name__, self.id)

    def request(self, *args, **kwargs):
        """
        The main purpose of this is to be a wrapper-like function to pass the api_token and all the other params to the
        requests that are being made

        :returns: An instance of RequestsHandler
        """
        return RequestsHandler(*args, api_token=self.api_token, **kwargs)

    @property
    def private(self):
        req = self.request(self.mist_client.uri+'/keys/'+self.id+"/private")
        private = req.get().json()
        return private

    @property
    def public(self):
        req = self.request(self.mist_client.uri+'/keys/'+self.id+"/public")
        public = req.get().json()
        return public

    def rename(self, new_name):
        payload = {
            'new_id': new_name
        }
        data = json.dumps(payload)
        req = self.request(self.mist_client.uri+'/keys/'+self.id, data=data)
        req.put()
        self.id = new_name
        self.mist_client.update_keys()

    def set_default(self):
        req = self.request(self.mist_client.uri+'/keys/'+self.id)
        req.post()
        self.is_default = True
        self.mist_client.update_keys()

    def delete(self):
        req = self.request(self.mist_client.uri+'/keys/'+self.id)
        req.delete()
        self.mist_client.update_keys()