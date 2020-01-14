

class NetworkDevice:

    def __init__(self, session):
        self.session = session

    def all_network_devices(self):
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

    def network_device_by_id(self, id):
        url = '/ers/config/networkdevice/{}'.format(id)
        return self.session.get(url).json()

    def version_info(self):
        url = '/ers/config/networkdevice/versioninfo'
        return self.session.get(url).json()

    def update_network_device(self, id):
        raise NotImplemented('Method has not been implemented')

    def delete_network_device(self, id):
        url = '/ers/config/networkdevice/{}'.format(id)
        return self.session.delete(url)

    def add_network_device(self):
        raise NotImplemented('Method has not been implemented')

    def monitor_bulk_status(self):
        raise NotImplemented('Method has not been implemented')

    def bulk_network_device_request(self):
        raise NotImplemented('Method has not been implemented')
