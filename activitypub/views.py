from django.http import HttpResponseNotAllowed, JsonResponse

def object(request, uuid):
    match request.method:
        case "GET":
            return JsonResponse({
                "id": uuid,
            })
        case _:
            return HttpResponseNotAllowed(['GET'], b"bad")
