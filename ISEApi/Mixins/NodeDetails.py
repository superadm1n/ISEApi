

class NodeDetails:

    def __init__(self, session):
        self.session = session

    def get_all_nodes(self):
        url = '/ers/config/node'
        data = self.session.get(url)
        return data
