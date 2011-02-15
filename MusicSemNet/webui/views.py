# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from rdfstore.models import *

def index(request):
    """
    show what type of info we have
    or
    show latest change
    or
    something interesting
    """
    nodetypes = NodeType.objects.all()
    ntarray = []
    for nt in nodetypes:
        ntarray.append(nt.uri)
    dic = {}
    dic['schemas'] = ntarray
    dic['nts'] = nodetypes
    return render_to_response('webuiindex.html',dic)

def viewinfo(request):
    """
    show data of specified schema
    according to the string next
    """
    thedata = request.GET['key']
    schemaname = NodeType.objects.filter(uri__exact = thedata)[0].desp
    schema = NodeType.objects.filter(uri__exact = thedata)[0]
    nodes = Node.objects.filter(t__exact = schema)
    dic = {}
    dic['schemaname'] = schemaname
    dic['nodes'] = nodes
    return render_to_response('webuiviewinfo.html',dic)

def viewschema(request):
    """
    schema relations
    according to the string next
    """
    
    return HttpResponse("view schema hola")
