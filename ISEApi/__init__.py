import logging
# Create a custom logger
logging_off = 100
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging_off)
from ISEApi.RequestHandler import Session
from ISEApi.Mixins.NodeDetails import NodeDetails
from ISEApi.Mixins.NetworkDevice import NetworkDevice, NetworkDeviceConfig


__version__ = '0.1'


class ISEApi:

    def __init__(self, ise_server, username, password, verify_ssl=False):
        self.ise_server = ise_server
        self.username = username
        self.password = password
        self.session = Session(base_url='https://{}:9060'.format(self.ise_server))
        self.session.auth = (username, password)
        self.session.verify = verify_ssl
        if verify_ssl is False:
            import requests
            requests.packages.urllib3.disable_warnings()

        self.network_device = NetworkDevice(session=self.session)
        self.node_details = NodeDetails(session=self.session)


