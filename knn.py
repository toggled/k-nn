#-------------------------------------------------------------------------------
# Name:        knn
# Purpose:
#
# Author:      andy
#
# Created:     30/01/2014
# Copyright:   (c) andy 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from __future__ import division
import math
from stemming.porter2 import stem
'''
articles = ['a','an','the']
verbs = ['am','is','are','was','were']
prep = ["aboard","about","above","across","after","against","along","amid","among","anti","around","as","at","before","behind","below",
"beneath","beside","besides","between","beyond","but","by","concerning","considering","despite","down","during","except","excepting",
"excluding","following","for","from","in","inside","into","like","minus","near","of","off","on","onto","opposite","outside",'over','past','per','plus',
'regarding','round','save','since','than','through','to','toward','towards','under','underneath','unlike','until','up','upon','versus','via','with','within','without']
'''
htofclass={}
bool_htofclass={}
doctoclass = {}

test_htofclass={}
test_bool_htofclass = {}
test_doctoclass={}
test_output={}
test_title = {} #for checking
test_firstkmap={}

numofdoc_containingw={}
numofdoc = 0
def printhtofclass(hasht,test_set=False):
    for doc,tabl in hasht.items():
        print 'doc: ',doc
        if test_set:
            #print len(test_doctoclass)
            print 'topic: ',test_doctoclass[doc]
        else:
            print 'topic: ',doctoclass[doc]
        for i,j in tabl.items():
            print i,' => ',j
        print ' --- '


def distance(vectora,vectorb):
    if len(vectora)!=len(vectorb):
        print 'dimension different'
        return
    return reduce(lambda x,y:x+y,[(i-j)**2 for (i,j) in zip(vectora,vectorb)])

def getfirstk(listoftuples,k,reverse=False):
    return sorted(listoftuples,key=lambda x:x[0],reverse=reverse)[:k]

def getstopwords(s):
    with open('stopwords.txt','r') as f:
        t=f.readlines()
        t=[i.strip().lower() for i in t if i.strip()!='']
        #print t
        list_stopw = [i for i in s if i in t]
    return list_stopw


def parsestring(s):
    ht={}
    import string
    from lxml import html
    import re


    doc = html.document_fromstring(s)


    def getWords(text):
        return re.compile('\w+').findall(text)

    text_doc = doc.text_content()
    #print text_doc
    s = text_doc.lower() # all lowercase
    s = re.sub('<[^>]*>', '', s) # removes <something> tags.
    #print s
    s = s.translate(string.maketrans("",""), string.digits)
    s = ' '.join(getWords(s)) # seperates out only words
    #print s
    #s = s.translate(string.maketrans("",""), string.punctuation)


    #s=' '.join(s.split(','))
    #s= ' '.join(s.split('.'))
    s= s.split()
    #print s
    list_stopw=getstopwords(s) #remove stopwords
    #print list_stopw
    for i in s:
        if i not in list_stopw:
            #i=stem(i) #stemming algorithm
            ht[i]=ht.get(i,0)+1
    return ht

def read_trainingset(filename='training (2).data',num_data=-1,testset=False):
    global numofdoc
    global test_htofclass
    global htofclass
    global doctoclass
    global test_title
    global test_doctoclass

    with open(filename,'r') as f:
        top = 0
        while 1:
            if num_data>0:
                if top==num_data:
                    print 'num_data'
                    break
            lines = f.readline()
            if lines == '\n':
                print 'last line'
                break

            topic = lines.strip()
            blankline = f.readline()
            story_title = f.readline()

            while 1:
                x = f.readline()

                if x == '\n':

                    break
                story_title+=x
            if testset:
                test_title[top] = story_title
            #print 'topic= ',topic, ' title = ',story_title
            #blankline = f.readline()
            story_location = f.readline()

            if story_location == '\n':
                #print 'story location null'
                f.readline()
                f.readline()
                #top+=1
                continue
            else:

                #print 'location--> ',story_location
                blankline = f.readline()
            #print topic, ' ',story_title, ' ',story_location

            #print top
            if testset:
                test_doctoclass[top] = topic
                test_topic_ht = test_htofclass.get(top,{})
            else:
                doctoclass[top]=topic
                topic_ht=htofclass.get(top,{})

            while 1:
                firstline = f.readline()
                if firstline == '\n' :
                    another = f.readline()
                    if another == '\n':
                        #print 'breaking'
                        break
                else:
                    afterparsed = parsestring(firstline)

                    #print afterparsed
                    for word,freq in afterparsed.items():
                        if testset:
                            test_topic_ht[word] = test_topic_ht.get(word,0)+freq
                        else:
                            firstinsertion = topic_ht.get(word,0)
                            topic_ht[word] = firstinsertion + freq
                            how_many_docs = numofdoc_containingw.get(word,0)

                            if not firstinsertion:
                                numofdoc_containingw[word] = how_many_docs+1


            if testset:
                test_htofclass[top] = test_topic_ht
            else:
                htofclass[top] = topic_ht
            top+=1
            print top

def buildbool(test_set=False):
    if test_set:
        items = test_htofclass.items()
    else:
        items = htofclass.items()
    for doc,tabl in items:
        if test_set:
            temp = test_bool_htofclass.get(doc,{})
        else:
            temp = bool_htofclass.get(doc,{})
        for i,j in tabl.items():
            if j:
                temp[i]=1
            else:
                temp[i]=0
        if test_set:
            test_bool_htofclass[doc] = temp
        else:
            bool_htofclass[doc]=temp

def printerror(writefile='random.txt'):
    global test_doctoclass
    #print test_doctoclass
    #print test_output
    with open(writefile,'w') as f:
        cnt = 0
        #print len(test_doctoclass),' ',len(test_output)
        for index,topic in test_doctoclass.items():
            if test_doctoclass[index] != test_output[index]:
                f.writelines(topic+'\n')
                f.writelines(test_title[index]+'\n')
                cnt +=1
        print 'number of misclassified: ',cnt
        #print len(test_doctoclass)
        f.writelines("misclassified: "+str(cnt)+'\n')
        f.writelines('accuracy : '+(str(100-cnt*100/len(test_doctoclass))))
        f.writelines("-------------------------------- ")


def runKNN(ham,eucl,cos,k=5):
    if ham:
        def hamming_distance(ht_a,ht_b):
           # print sorted(ht_a.keys()),' ',len(ht_a.keys())
            #print ' ----------------------- '
            #print sorted(ht_b.keys()),' ',len(ht_b.keys())
            return len(set(ht_a.keys()).symmetric_difference(set(ht_b.keys())))
        for doc,test_i in test_bool_htofclass.items():
            print 'test no: ',doc
            print 'target: ',test_doctoclass[doc]

            #for idoc,train_i in bool_htofclass.items():
                #print ' class: ', doctoclass[idoc],' ',hamming_distance(train_i,test_i)
            listoftup =[ (hamming_distance(train_i,test_i),doctoclass[idoc]) for idoc,train_i in bool_htofclass.items() ]
            #print getfirstk(listoftup,k)
            m = getfirstk(listoftup,k,reverse=True)
            t=[i[1] for i in m]
            test_firstkmap[doc] = m
            #print t
            from Counter import Counter
            c = Counter(t)
            most_common= c.most_common(1) # get most common one from k neighbours
            test_output[doc]= most_common[0][0]
            print 'classified as: ',test_output[doc]
        printerror('ham'+str(k)+'.txt')

    if eucl:
        def eucl_distance(ht_a,ht_b):
            unions = sorted(set(ht_a.keys()).union(ht_b.keys()))

            vectora= [ht_a.get(i,0) for i in unions]
            vectorb= [ht_b.get(i,0) for i in unions]
            return math.sqrt(reduce(lambda x,y:x+y,[(i-j)**2 for (i,j) in zip(vectora,vectorb)]))

        for doc,test_i in test_htofclass.items():
            #print 'test no: ',doc
            #print 'target: ',test_doctoclass[doc]

            #for idoc,train_i in bool_htofclass.items():
                #print ' class: ', doctoclass[idoc],' ',hamming_distance(train_i,test_i)
            listoftup =[ (eucl_distance(train_i,test_i),doctoclass[idoc]) for idoc,train_i in htofclass.items() ]
            #print getfirstk(listoftup,k)
            m = getfirstk(listoftup,k,reverse=True)
            t=[i[1] for i in m]

            test_firstkmap[doc] = m
            #print t
            from Counter import Counter
            c = Counter(t)
            most_common= c.most_common(1) # get most common one from k neighbours
            test_output[doc]= most_common[0][0]
            #print 'classified as: ',test_output[doc]
        printerror('eucl'+str(k)+'.txt')
    if cos:
            training_sim = {}
            def calculate_distance(test,training,idoc,testlen,traininglen):
                #intersec = set(test.keys()).intersection(set(training.keys()))
                t_vec={}
                tr_vec={}
                Wd = len(test)
                test_numofdoc = testlen

                tr_numofdoc = traininglen
                for words in test:
                    Nd_w = test.get(words)
                    TF_w= Nd_w / Wd
                    C_w = numofdoc_containingw.get(words,0)

                    if C_w>0:
                        IDF_w = 1.0 + math.log(test_numofdoc/C_w)
                    else:
                        IDF_w = 1.0
                    t_vec[words]=TF_w*IDF_w


                if not training_sim.get(idoc,0):
                    Wd = len(training)
                    #print 'wd: ',Wd
                    for words in training:
                        Nd_w = training.get(words)
                        #print 'ND-w ',Nd_w
                        TF_w= Nd_w / Wd
                        C_w = numofdoc_containingw.get(words,0)
                        if C_w>0:
                            IDF_w = 1.0 + math.log(test_numofdoc/C_w)
                        else:
                            IDF_w = 1.0
                        tr_vec[words]=TF_w*IDF_w

                    training_sim[idoc] = tr_vec
                else:
                    tr_vec = training_sim.get(idoc)

                unions = sorted(set(t_vec.keys()).union(tr_vec.keys()))
                vectora= [t_vec.get(i,0) for i in unions]
                vectorb= [tr_vec.get(i,0) for i in unions]
                #print vectora
                fun=lambda x:x**2
                sm=lambda x,y:x+y
                dotprod = reduce(sm,[i*j for (i,j) in zip(vectora,vectorb)])

                moda = reduce(sm,map(fun,vectora))
                modb = reduce(sm,map(fun,vectorb))
                if(moda*modb<0.001):
                    print 'wd ',Wd
                    print t_vec
                    print 'tits'
                    print tr_vec
                    print 'both are zero'

                return dotprod/math.sqrt(moda*modb)


            #print numofdoc_containingw.items()



            #print numofdoc
            #w = 'share'
            for doc,test_i in test_htofclass.items():
                print 'test no: ',doc
                print 'target: ',test_doctoclass[doc]

                #print test_i
                listoftup=[]
                test_len = len(test_i)
                if(test_len == 0):
                    print test_doctoclass[doc]
                    import sys
                    print test_title[doc]
                    sys.exit(1)
                for idoc,train_i in htofclass.items():
                    train_len = len(train_i)
                    if train_len:
                        dist = calculate_distance(test_i,train_i,idoc,test_len,train_len)
                    #print dist
                    listoftup.append((dist,doctoclass[idoc]))
                #print listoftup
                #print getfirstk(listoftup,k,reverse=True)
                m = getfirstk(listoftup,k,reverse=True)
                t=[i[1] for i in m]

                test_firstkmap[doc] = m
                from Counter import Counter
                c = Counter(t)
                most_common= c.most_common(1) # get most common one from k neighbours
                #print "common ",most_common
                test_output[doc]= most_common[0][0]
                print 'classified as: ',test_output[doc]
            printerror('cos'+str(k)+'.txt')

def getfirst(k,reverse=False):
        from Counter import Counter
        for doc,test_i in test_htofclass.items():
            temp = test_firstkmap[doc]
            print 'target: ',test_doctoclass[doc]
            #print temp
            t = [j for i,j in getfirstk(temp,k,reverse)]
            #temp =
            c = Counter(t)
            most_common= c.most_common(1) # get most common one from k neighbours
           # print "common ",most_common
            test_output[doc]= most_common[0][0]
            print 'classified as: ',test_output[doc]
        printerror('cos'+str(k)+'.txt')

def main():
    a=[(3,'A'),(5,'B'),(2,'C'),(5,'D'),(0,'AA')]
    k=3
    #init_htbles()
    #print len(htofclass)
   # print getfirstk(a,k)
    #a=[1,1,1,1.2]
    #b=[2,3,3,4.2]
    #print distance(a,b)
    #parsestring('')

    #read_trainingset(filename='abc.txt',num_data=25)
    #read_trainingset(filename = 'abc_test.txt',testset= True,num_data=10)

    read_trainingset(num_data=200)
    #print 'reading test set'
    read_trainingset('test.data',testset=True,num_data=50)
    #printhtofclass(test_htofclass,True)
    #printhtofclass(htofclass)
    #read_trainingset()
    #buildbool()

    #buildbool(True)
    #runKNN(ham=True,eucl=False,cos=False)
    #runKNN(ham=False,eucl=True,cos=False)

    runKNN(ham=False,eucl=False,cos=True)
    getfirst(1,reverse=True)
    getfirst(3,reverse=True)
    #printhtofclass(bool_htofclass)
    #printhtofclass(test_bool_htofclass,True)
if __name__ == '__main__':
    main()
