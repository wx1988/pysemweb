from google.appengine.ext import db

class NodeType(db.Model):
    name = db.StringProperty()
    uri = db.LinkProperty()

class EdgeType(db.Model):
    name = db.StringProperty()
    uri = db.LinkProperty()
    node1type = db.ReferenceProperty(NodeType,collection_name="n1")
    node2type = db.ReferenceProperty(NodeType,collection_name="n2")    

class Node(db.Model):
    t = db.ReferenceProperty(NodeType)
    value = db.StringProperty()

class Edge(db.Model):
    t = db.ReferenceProperty(EdgeType)
    node1 = db.ReferenceProperty(Node,collection_name="n1")
    node2 = db.ReferenceProperty(Node,collection_name="n2")

