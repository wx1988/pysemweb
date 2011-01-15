"""
execute the sparql query
docs.djangoproject.com/en/dev/topics/db/sql
"""
from django.db import connection,transaction
from rsparqlparser import parserql

def rquery(sen):
    """
    sen:the query sentence
    """
    #
    sqlquery = parserql(sen)
    print sqlquery
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    rows = cursor.fetchall()

    return rows
    
