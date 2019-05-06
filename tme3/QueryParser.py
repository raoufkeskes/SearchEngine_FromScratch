# -*- coding: utf-8 -*-

"""
Created on Tue Mar  5 10:20:50 2019

@author: raoufks
"""

from .Query import Query
import json 


class QueryParser : 
    

    tags = ['.I' , '.W' , '.A' , '.N' ]
    @staticmethod
    def buildJSONFormat ( dictionary ) :
        temp_dict = {}
        for key in dictionary:
            temp_dict[key] = dictionary[key].getJsonFormat()
        return json.dumps( temp_dict ,  indent=2 )
    
    
    @staticmethod
    def Parse ( qryFile , relFile ) :
        
        f  = open( qryFile , 'r')
        f=f.read().splitlines()
        queries =dict()
        i=0
        while ( i< len(f) ) :
            # check if the line is not empty to explore it !
            if ( len( f[i].strip() ) > 0 ):
                
                if ( len(f[i]) >1 and f[i][0]=='.' ) :
                    # we found an id tag line 
                    if ( f[i][1] == 'I'):
                            current_tag =""
                            #delete breaklines and unecessary spaces 
                            iDquery=f[i][2:].strip()
                            new_query = Query(iDquery)
                            # point the dict element to a document object
                            queries[iDquery] = new_query
                            
                    
                        
                    elif ( f[i][1] == 'W' ):
                            current_tag  = "Text"
                    
                    
                    '''
                    -> Same Text Processing for any information tag
                    '''

                    if ( len(current_tag)!=0 ):
                        #Preprocessing
                        setter = getattr( new_query , "set"+current_tag )
                        getter = getattr( new_query , "get"+current_tag )
                        print
                        # when there is some content in the same line of the 
                        # tag else we ll get starting empty string
                        setter( f[i][2:].strip() )
                        i+=1
                        
                        # we also avoid "False Alarms"
                        # like a phrase starting with .Today ...
                        while ( i<len(f) and ( ( f[i][:2] not in QueryParser.tags ) or
                                ( f[i][:2] in QueryParser.tags and (len(f[i]) > 2) and
                                  f[i][2] != ' ') )
                              ) :
                            
                            setter( getter()+" "+f[i] )
                            i+=1
                        
                        
                        #to not skip a line 
                        i-=1
                        
                        # delete starting spaces
                        setter( getter().lstrip()  )
                        
            i+=1    
        
        
        
        
        # the file does not contain relevance values 
        default_relevance = 1
        
        f  = open( relFile  , 'r')
        for line in f :
            ls = line.split()
            
            queries[ str(int(ls[0])) ].add_relevant_doc ( str(int(ls[1])) , default_relevance )
            
        return queries 
