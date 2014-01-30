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
import math
def distance(vectora,vectorb):
    if len(vectora)!=len(vectorb):
        print 'dimension different'
        return
    return reduce(lambda x,y:x+y,[(i-j)**2 for (i,j) in zip(vectora,vectorb)])

def main():
    a=[(3,'A'),(5,'B'),(2,'C'),(5,'D')]
    k=3
    print sorted(a,key=lambda x:x[0])[:k]
    a=[1,1,1,1.2]
    b=[2,3,3,4.2]
    print distance(a,b)

if __name__ == '__main__':
    main()
