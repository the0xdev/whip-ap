from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from urllib.parse import urlparse
import re

# Create your views here.
userPart = re.compile(r"")

ALPHA = "([A-Z]|[a-z])" # ALPHA = %x41-5A / %x61-7A ; A-Z / a-z
DIGIT = "\d" # DIGIT = %x30-39 ; 0-9
HEXDIG = "\x" # HEXDIG =  DIGIT / "A" / "B" / "C" / "D" / "E" / "F"

unreserved = re.compile(r"") # unreserved = ALPHA / DIGIT / "-" / "." / "_" / "~"
sub_delims = re.compile(r"") # sub-delims = "!" / "$" / "&" / "'" / "(" / ")" / "*" / "+" / "," / ";" / "="
pct_encoded = re.compile(r"%") # pct-encoded = "%" HEXDIG HEXDIG

host = re.compile(r"")
userPart = re.compile(r"[\w\-\.~]|[\!\$\&\'\(\)\*\+\,\;\=]")
acctURI = re.compile(f"{userPart}@{host}")

def webfinger(request):
    match request.method:
        case "GET":
            resource = request.GET.get('resource')
            if not resource:
                return HttpResponseBadRequest(b"no resource provided")

            parse = urlparse(resource)

            if parse.scheme != "acct":
                pass
            


            rel = request.GET.getlist('rel')

            return JsonResponse({
                "subject": resource,
                "parse": parse.path,

                "links": {
                    "rel": rel,
                }
            })
        case _:
            return HttpResponseNotAllowed(['GET'], b"bad")
