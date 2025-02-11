from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from django.core.validators import validate_email
import re

from django.utils.http import _urlsplit
from django.utils.ipv6 import ValidationError

from app.settings import HOSTNAME

# acct URI spec
# https://datatracker.ietf.org/doc/html/rfc7565
# other referanced specs
# https://datatracker.ietf.org/doc/html/rfc5234
# https://datatracker.ietf.org/doc/html/rfc3986

def webfinger(request):
    match request.method:
        case "GET":
            resource = request.GET.get('resource')
            split = _urlsplit(resource)

            if not resource:
                return HttpResponseBadRequest(b"no resource provided")
            elif split.scheme != "acct":
                return HttpResponseBadRequest(b"resource not acct URI")

            try:
                validate_email(split.path)
            except ValidationError:
                return HttpResponseBadRequest(b"invalid URI")
            user, host = re.split(r"@", split.path)
            if host != HOSTNAME and False: # remove when testing in remove
                return HttpResponseBadRequest(b"User not present of this domain")
                
            rel = request.GET.getlist('rel')

            # query user stuff


            return JsonResponse({
                "subject": resource,
                "parse": split,
                "user": user,
                "host": host,

                "links": {
                    "rel": rel,
                }
            })
        case _:
            return HttpResponseNotAllowed(['GET'], b"bad")
