from ISEApi import logger
from json import dumps
from random import randint

class NetworkDevice:

    def __init__(self, session):
        self.session = session

    def all_devices(self):
        url = '/ers/config/networkdevice'
        while True:
            data = self.session.get(url)
            for entry in data.json()['SearchResult']['resources']:
                yield entry

            # if the href key does not exist there are no more results
            try:
                _ = data.json()['SearchResult']['nextPage']['href']
            except KeyError:
                break
            # update the relative url to use based on the url listed in the next page href key
            url = '/' + '/'.join(data.json()['SearchResult']['nextPage']['href'].split('/')[3:])

    def device_by_id(self, id):
        url = '/ers/config/networkdevice/{}'.format(id)
        return self.session.get(url).json()

    def version_info(self):
        url = '/ers/config/networkdevice/versioninfo'
        return self.session.get(url).json()

    def update_device(self, id):
        raise NotImplemented('Method has not been implemented')

    def delete_device(self, id):
        url = '/ers/config/networkdevice/{}'.format(id)
        resp = self.session.delete(url)
        if resp.status_code == 204:
            return True
        else:
            logger.error(resp.text)
            return False

    def add_device(self, device_configuration):
        url = '/ers/config/networkdevice'
        resp = self.session.post(url=url, data=device_configuration)
        if resp.status_code == 201:
            return True
        else:
            logger.error(resp.text)
            return False

    def monitor_bulk_status(self):
        raise NotImplemented('Method has not been implemented')

    def bulk_device_request(self):
        raise NotImplemented('Method has not been implemented')


def subsection(view):
    """tags method in network device config class to represent sub sections of the NetworkDevice config"""
    view.subsection = True
    return view


class NetworkDeviceConfig:
    """Object to abstract the generation of a JSON string that is used to
    submit to the API for creating a network device"""
    def __init__(self, name, description, radius_secret, snmp_secret, snmp_polling_interval,
                 tacacs_secret, ip_address, snmp_version='TWO_C'):

        num_digits = 20
        self.id = randint(10 ** (num_digits - 1), (10 ** num_digits) - 1)
        self.name = name
        self.description = description
        self.radius_secret = radius_secret
        self.snmp_secret = snmp_secret
        self.snmp_version = snmp_version
        self.snmp_polling_interval = snmp_polling_interval
        self.tacacs_secret = tacacs_secret
        self.ip_address = ip_address

    @classmethod
    def _subsection_methods(cls):
        """Detects the classes methods that are decorated with the on_init decorator and returns
        them"""
        methods = []
        for name, method in cls.__dict__.items():
            if hasattr(method, "subsection"):
                methods.append(method)
        return methods

    @subsection
    def _authentication_section(self):
        return {'authenticationSettings':
                    {'radiusSharedSecret': self.radius_secret}
                }

    @subsection
    def _snmp_settings(self):
        return {'snmpsettings': {'version': self.snmp_version,
                                 'roCommunity': self.snmp_secret,
                                 'pollingInterval': 28800,
                                 'linkTrapQuery': 'true',
                                 'macTrapQuery': 'true',
                                 'originatingPolicyServicesNode': 'Auto'
                                 }
                }

    @subsection
    def _tacacs_settings(self):
        return {'tacacsSettings':
                    {'sharedSecret': self.tacacs_secret, 'connectModeOptions': 'OFF'}
                }

    @subsection
    def _ip_settings(self):
        return {'NetworkDeviceIPList':
                    [
                        {'ipaddress': self.ip_address, 'mask': 32}
                    ]
                }

    @property
    def json_string(self):
        string = {'NetworkDevice':
                      {'id': self.id, 'name': self.name, 'description': self.description,
                       "NetworkDeviceGroupList": ["Location#All Locations",
                                                  "Device Type#All Device Types#IOS_Devices"]
                       }
                  }

        for method in self._subsection_methods():
            string['NetworkDevice'].update(method(self))

        return dumps(string)

