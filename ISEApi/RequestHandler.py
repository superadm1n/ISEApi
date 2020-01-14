from requests import Session as RequestsSession


class Session(RequestsSession):

    def __init__(self, base_url):
        self.base_url = base_url
        super().__init__()

    def _set_content_type(self, request):
        """Checks for the content-type and accept headers and if they dont exists sets them to json"""
        if not request.headers.get('content-type'):
            request.headers['content-type'] = 'application/json'
        if not request.headers.get('accept'):
            request.headers['accept'] = 'application/json'

    def _prepend_base_url(self, request):
        """Takes the relative URL that was provided and prepends the base URL to it"""
        relative_url = request.url
        request.url = self.base_url + relative_url

    def prepare_request(self, request):
        """Hijack the request before it is sent to the server and update url and header"""
        self._set_content_type(request)
        self._prepend_base_url(request)
        return super().prepare_request(request)
