from QuickScrum import settings

class SubdomainURLRoutingMiddleware(object):

    # Overridden method
    # Checks the subdomain
    def process_request(self, request):
        bits = request.META['HTTP_HOST'].split('.')
        url_base_path = settings.SUBDOMAIN_URLCONFS.get('url_base_path')
        #if len(bits) == 3 and len(bits[0]) == 2:
        if bits is None: # no subdomain
            request.team = None
        elif bits[0].find(url_base_path) != -1: # no subdomain given
            request.team = None
        elif len(bits) >= 2 and bits[1].find(url_base_path) != -1: # has subdomain
            request.team = bits[0]
        return None