# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from rdfstore.models import *
from sparqlexecute import rquery
from rsparqlparser import parserql

def index(request):
    """
    the main interface for query
    """
    dic = {}
    return render_to_response('index.html',dic)
    #return HttpResponse("2")

def showresult(request):
    """
    get post message and return the post value
    and with the box of query
    """
    sparql = request.POST['sparkqltext']

    sql = parserql(sparql)
    rows = rquery(sparql)
    
    dic = {}
    dic['thequery'] = sparql
    dic['sql'] = sql
    dic['rows'] = rows
    
    return render_to_response('result.html',dic)

    #return HttpResponse("1")
    
