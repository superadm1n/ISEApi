from ISEApi.RequestHandler import Session
from ISEApi.Mixins.NodeDetails import NodeDetails
from ISEApi.Mixins.NetworkDevice import NetworkDevice

__version__ = '0.1'

class ISEApi():

    def __init__(self, ise_server, username, password, verify_ssl=False):
        self.ise_server = ise_server
        self.username = username
        self.password = password
        self.session = Session(base_url='https://{}:9060'.format(self.ise_server))
        self.session.auth = (username, password)
        self.session.verify = verify_ssl

        self.network_device = NetworkDevice(session=self.session)
        self.node_details = NodeDetails(session=self.session)


