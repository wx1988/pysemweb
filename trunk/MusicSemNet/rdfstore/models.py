from django.db import models

# Create your models here.
class NodeType(models.Model):
    isvalue = models.BooleanField()
    desp = models.TextField()
    comment = models.TextField()
    uri = models.URLField(verify_exists=False)

    def __unicode__(self):
        return self.uri

class EdgeType(models.Model):
    desp = models.TextField()
    comment = models.TextField()
    uri = models.URLField(verify_exists=False)
    node1type = models.ForeignKey(NodeType,related_name='nt1')
    node2type = models.ForeignKey(NodeType,related_name='nt2')

    def __unicode__(self):
        return self.uri+"__"+str(self.node1type)+"__"+str(self.node2type)

class Node(models.Model):
    t = models.ForeignKey(NodeType)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return self.value

class Edge(models.Model):
    """
    how to over write the save() method to have a check machnism
    """
    t = models.ForeignKey(EdgeType)
    node1 = models.ForeignKey(Node,related_name='n1')
    node2 = models.ForeignKey(Node,related_name='n2')

    def __unicode__(self):
        return self.node1.__unicode__() + "_" + self.t.__unicode__()+"_"+self.node2.__unicode__()


