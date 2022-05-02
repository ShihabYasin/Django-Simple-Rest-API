from django.shortcuts import render
from django.shortcuts import render, HttpResponseRedirect, Http404
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer

from .models import ItemModel
from .serializers import ItemSerializer


class JSONResponse (HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer ().render (data)
        kwargs['content_type'] = 'application/json'
        super (JSONResponse, self).__init__ (content, **kwargs)


# Create your views here.
@csrf_exempt
def ItemsView(request):
    if request.method == 'GET':
        items = ItemModel.objects.all ()
        serializer = ItemSerializer (items, many=True)
        return JsonResponse (serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser ().parse (request)
        serializer = ItemSerializer (data=data)
        if serializer.is_valid ():
            serializer.save ()
            return JSONResponse (serializer.data, status=201)
        return JSONResponse (serializer.errors, status=400)


@csrf_exempt
def ItemView(request, nm):
    try:
        item = ItemModel.objects.get (id=nm)
    except ItemModel.DoesNotExist:
        raise Http404 ('Not found')

    if request.method == 'GET':
        serializer = ItemSerializer (item)
        return JsonResponse (serializer.data)

    if request.method == 'PUT':
        data = JSONParser ().parse (request)
        serializer = ItemSerializer (item, data=data)

        if serializer.is_valid ():
            serializer.save ()
            return JsonResponse (serializer.data)
        return JsonResponse (serializer.errors, status=400)

    if request.method == "DELETE":
        item.delete ()
        return HttpResponse (status=204)
