# -*- coding: cp936 -*-
"""
sparql parser
"""

def parserql(s):
    """
    parser the sparql to get
    1 the result column
    2 the condition
    @see parserPrefix
    @see parserwhere
    """
    #parser the Prefix
    s = s.lower()
    prefixdic = parserPrefix(s)
    #print prefixdic

    #print s
    s = expandPrefix(s,prefixdic)
    #print s
    
    #parser the select
    #the presentation of result in string
    resultlist = parserSelect(s)
    #print resultlist
    
    #parser the part of condition
    triples = parserWhereTriples(s)
    print triples
    
    
    #how to translate the code into result output?
    result = createsql(triples,resultlist)
    return result
    
def parserPrefix(s):
    """
    ����ǰ׺
    """
    abbrdic = {}
    lines = s.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("prefix"):
            arr = parserPrefixLine(line)
            abbrdic[arr[0]] = arr[1]
            
    return abbrdic
    
def parserPrefixLine(line):
    """
    input is a line begin with PREFIX
    case insensetive
    @param line PREFIX dc: <http://...> (start with prefix)
    @return [abbr,fullstr]
    �Ȳ��������
    """
    line = line.strip()
    if line.endswith("\n"):
        line = line[0:len(line)-1]
    if not line.startswith("prefix"):
        raise Exception("prefix line not start with prefix")
    ws1 = line.split(" ")
    ws2 = []
    for w in ws1:
        if w != "":
            ws2.append(w)
    result=[]
    result.append(ws2[1])
    result.append(ws2[2][1:len(ws2[2])-1])
    return result

def expandPrefix(s,prefixdic):
    """
    �����е���д��չ��
    ��Ҫ����<>����
    """
    for prefix in prefixdic.keys():
        #ʹ��������ʽƥ�䣬�����Լ�дһ������
        #s = s.replace(prefix,prefixdic[prefix])
        s = myreplace(s,prefix,prefixdic[prefix])
    return s

def myreplace(s,orgstr,restr):
    """
    ��s�н����滻
    """
    while s.count(orgstr) != 0:
        i = s.index(orgstr)
        j = i
        while s[j] != " ":
            j = j + 1
        s = s[0:i]+'<'+restr+ s[i+len(orgstr):j] +">"+s[j:len(s)]
    return s
            

def parserSelect(s):
    """
    parser the part between select and where
    this is the part of return related
    @param s SELECT ?name ?mbox\nWHERE
    how to ignore the big/small case
    """
    sindex = s.index('select')
    windex = s.index('where')
    s = s[sindex:windex]
    
    line = s.replace('\n',' ')
    ws1 = line.split(" ")
    ws2 = []
    for w in ws1:
        if w == "" or w == "select" or w == "where":
            continue
        ws2.append(w)
    return ws2

def parserWhereTriples(s):
    """
    #@param from WHERE to the end of the sentence
    @param the whole sentence
    @return the condition structure of the SQL
    ���ڲ�֧����дģʽ��
    һ����Ԫ������һ�����
    ��ȡÿ����Ԫ���ģʽ
    """
    s = s[s.index('{')+1:s.index('}')]
    #print s
    edges = []
    s = s.replace('\n',' ')
    index = 1
    slist = s.split(' ')
    #print slist
    i = 0
    while i < len(slist):
        triple = []
        while i < len(slist) and slist[i] != ".":
            if slist[i] == "":
                i = i + 1
                continue
            triple.append(slist[i])
            i = i + 1
        i = i + 1
        edge = {}
        if len(triple) != 3:
            continue
        edge['e'] = triple[1]
        edge['n1'] = triple[0]
        edge['n2'] = triple[2]
        edges.append(edge)

    return edges

def spreadCondition(s):
    """
    ��ʱ��֧��������ʽ
    ���ֺ�չ��
    """
    
    
def splitsentence(s,sp):
    ws = s.split(sp)
    result = []
    for w in ws:
        if w != "":
            result.append(w)
    return result

def createsql(conditions,queryitems):
    #print "condition and queryitems"
    #print conditions
    #print queryitems
    """
    @conditions the triples
    @
    Ŀǰ֧�ֲ�ѯģʽ��
    select [��ѯģʽ] where {[��֪/δ֪����/�ַ���ֵ ��֪ν�� ��֪/δ֪����/�ַ���ֵ.]}
    ��ѯģʽ := ���ַ�
    ν��Ҳ������ͨ���
    select�е���֪���Ա�����where��������
    """
    sqlstr = ""
    #the condition part
    #how to translate them into sql pattern
    #get a list of triples
    #conditions = parserWhere(s[s.index('{')+1:s.rindex('}')])

    selectstr = "SELECT "
    fromstr = " FROM "
    wherestr = " WHERE "

    #from
    for i in range(len(conditions)):
        fromstr = fromstr + "rdfstore_node AS Node"+str(i)+str(1)+",rdfstore_node AS Node"+str(i)+str(2)+",rdfstore_edge AS Edge"+str(i)+","
    fromstr = fromstr[0:len(fromstr)-1]

    #where
    #first get all type of info to be processed
    #const value
    #resource
    #tmp variable ?name
    #edge type:not only constant value supported
    dicunknow = {}
    express = []
    for i in range(len(conditions)):
        #n1
        if conditions[i]['n1'].startswith('?'):
            tmps = conditions[i]['n1']
            if not dicunknow.has_key(tmps):
                dicunknow[tmps] = []
            dicunknow[tmps].append("Node"+str(i)+str(1))
        elif conditions[i]['n1'].startswith('<'):
            tmps = conditions[i]['n1']
            express.append("Node"+str(i)+str(1)+".value == '"+tmps[1:len(tmps)-1]+"'")
        else:
            tmps = conditions[i]['n1']
            express.append("Node"+str(i)+str(1)+".value == '"+tmps[0:len(tmps)]+"'")

        #n2
        if conditions[i]['n2'].startswith('?'):
            tmps = conditions[i]['n2']
            if not dicunknow.has_key(tmps):
                dicunknow[tmps] = []
            dicunknow[tmps].append("Node"+str(i)+str(2))
        elif conditions[i]['n2'].startswith('<'):
            tmps = conditions[i]['n2']
            express.append("Node"+str(i)+str(2)+".value == '"+tmps[1:len(tmps)-1]+"'")
        else:
            tmps = conditions[i]['n2']
            express.append("Node"+str(i)+str(2)+".value == '"+tmps[0:len(tmps)]+"'")

        #edge
        if conditions[i]['e'].startswith("?"):
            #to nothing?
            k = 1
        elif conditions[i]['e'].startswith('<'):
            tmps = conditions[i]['e']
            tmps = "Edge"+str(i)+".t_id in " + "(SELECT id FROM rdfstore_edgetype WHERE uri='"+tmps[1:len(tmps)-1]+"')"
            tmps1 = "Node"+str(i)+str(1)+".id == Edge"+str(i)+".node1_id"
            tmps2 = "Node"+str(i)+str(2)+".id == Edge"+str(i)+".node2_id"
            express.append(tmps)
            express.append(tmps1)
            express.append(tmps2)
            
    #print express
    #print dicunknow
    #Cn2 combination
    for unknowitem in dicunknow.keys():
        unknowlist = dicunknow[unknowitem]
        for i in range(1,len(unknowlist)):
            tmps = ""
            tmps = unknowlist[i]+".value == " +unknowlist[i-1]+".value"
            express.append(tmps)

    #print express
    for exp in express:
        wherestr = wherestr + "(" + exp + ")"+" and "
    wherestr = wherestr[0:len(wherestr)-4]
        
    #select
    for queryitem in queryitems:
        for i in range(len(conditions)):
            if queryitem == conditions[i]['e']:
                raise Exception("Not Support Now")
                #selectstr = selectstr + "Edge"+str(i)+".
            elif queryitem == conditions[i]['n1']:
                selectstr = selectstr + "Node"+str(i)+str(1)+".value,"
            elif queryitem == conditions[i]['n2']:
                selectstr = selectstr + "Node"+str(i)+str(2)+".value,"
            else:
                #do nothing
                i = 1
    selectstr = selectstr[0:len(selectstr)-1]+" "

    sqlstr = selectstr + fromstr + wherestr
    #print sqlstr
    
    return sqlstr
    
    """
    ת������
    """
    
    """
    parser the sentence of where
    #startwith { and endwith }
    #split with '.'
    #what does ';' means triple pattern
    #','��ʾ������ͬ��ν��
    #Filter regrex(?name,"Smith")
    #this is the biggest part
    #�ƺ�����ǿ���
    """
    #ͨ����ͬ���ʾ�����ϵ
    #����ӳ�䵽rdb�ռ��أ�
    
    """
    { ?x foaf:name ?name .    ?x foaf:mbox ?mbox }
    ͨ��name�����Կ���֪��
    name�����нڵ������
    x���ǽڵ������
    ��x���뵱ǰ��δ֪�м����ṹ
    
    ����ʵ�������ӽṹ������ӳ�䵽gql��䣿
    """

def testmyreplace():
    s = "?x foaf:name ?name"
    
    print myreplace(s,"foaf:","ss")

def test1():
    sparql="""select ?title where {<http://book/book1> <http://title> ?title . }"""
#    sparql = "SELECT ?name where {<http://www.com/record/111/> <http://record/> ?name .}"
    print parserql(sparql)

def test2():
    sparql = "PREFIX foaf: <http://aa/>\nSELECT ?name ?mbox where {?x foaf:name ?name . ?x foaf:mbox ?mbox .}"
    print parserql(sparql)
    
    """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT ?x ?name
    WHERE {?x foaf:name ?name }
    """
def test3():
    sparql = "select ?name where {<http://meaqi.com/Record/1> <http://purl.org/dc/elements/1.1/title> ?name .}"
    print parserql(sparql)

def test4():
    sparql = "select ?name ?x where {?x <http://purl.org/dc/elements/1.1/title> ?name .}"
    print parserql(sparql)
    
if __name__ == "__main__":
    test1()
    test4()
    test3()
    test1()
    test2()
    #testmyreplace()
