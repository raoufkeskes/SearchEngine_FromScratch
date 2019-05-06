import json
import re 
from tme1.document import Document

class Parser : 
    
    # static attribules
    tags = [".I",".T",".B",".A",".K",".W",".X"]
       
    
    '''
    - transform a dictionary to a json object for outputs purpose
      such as printing , files , ... 
      
    '''
    def buildJSONFormat ( dictionary ) :
        temp_dict = {}
        for key in dictionary:
            temp_dict[key] = dictionary[key].getJsonFormat()
        return json.dumps( temp_dict ,  indent=2 )
        
  
    '''
    show the collection dic on the console 
    '''
    @staticmethod
    def display(dictionary) :
        print ( Parser.buildJSONFormat(dictionary) )
    
    '''
    store the collection dic on a file 
    '''
    @staticmethod
    def save( dictionary , filename ) :
        with open( filename , 'w' ) as file:
            file.write(Parser.buildJSONFormat(dictionary))
        
    @staticmethod
    def buildDocCollectionSimple ( collection_file , store=None , console=False ) :
        
        f  = open( collection_file , 'r')
        f=f.read().splitlines()
        docs=dict()
        i=0

        while ( i< len(f) ) :
            
            
            # check if the line is not empty to explore it !
            if ( len( f[i].strip() ) > 0 ):
                
                #Case doc 1461 Cisi line= <blabla> .I 1461 text
                for tt in Parser.tags : 
                    start = f[i].find(tt+" ")
                    if ( start != -1 ):
                        f[i] = f[i][start:]
                        break
                
                
                if ( len(f[i]) >1 and f[i][0]=='.' ) :
                    current_tag =""
                    # we found an id tag line 
                    if ( f[i][1] == 'I'):
                            #delete breaklines and unecessary spaces 
                            iDdoc=f[i][2:].strip()
                            #new document object created
                            if ( iDdoc not in docs ) :
                                # point the dict element to a document object
                                docs[iDdoc] = Document(iDdoc)
                            
                            current_doc = docs[iDdoc]
                            
                    elif ( f[i][1] == 'T' ):
                        current_tag  = "Title"
                    
                    # keywords kan improve the system to see results 
                    # or f[i][1] =="K"
                    elif ( f[i][1] == 'W'  ):
                            current_tag  = "Text"
                    elif ( f[i][1] == 'X' ):
                        current_tag  = "X"
                                 

                    if ( len(current_tag)!=0 ):
                        
                        if ( current_tag != 'X'  ):
                            '''
                            -> Same Text Processing for any information tag expect X tag
                            '''
                            #Preprocessing
                            setter = getattr( current_doc , "set"+current_tag )
                            getter = getattr( current_doc , "get"+current_tag )
                            # when there is some content in the same line of the 
                            # tag else we ll get starting empty string Ex .T blabla
                            setter( f[i][2:].strip() )
                        
                        i+=1
                        
                        # we also avoid "False Alarms"
                        # like a phrase starting with .Today ...
                        while ( i<len(f) and len(f[i])>0 and ( ( f[i][:2] not in Parser.tags ) or
                                ( f[i][:2] in Parser.tags and (len(f[i]) > 2) and
                                  f[i][2] != ' ') )
                              ) :
                            if ( current_tag == "X" ) : 
                                id_found = f[i].lstrip().split()[0] 
                                current_doc.addSuccessor ( id_found )
                                if ( id_found not in docs ) :
                                    docs[id_found] = Document(id_found)
                                    
                                docs[id_found].addPredecessor( iDdoc )
                            
                            else : 
                                setter( getter()+" "+f[i] )
                                
                            i+=1
                        
                        
                        #to not skip a line 
                        i-=1
                        if ( current_tag != "X"  ):
                            # delete starting spaces
                            setter( getter().strip()  )
            i+=1    
             
        if ( console == True ) :
            Parser.display ( docs )
        if ( store !=  None ) :
            Parser.save ( docs , store  )
            
        
        return docs
    
    '''
    TME 1 : function to retrieve id , title and text of document with regex
            just for fun !
    '''
    def buildDocCollectionRegex( collection_file , store=None , console=False ) :
        with open( collection_file , 'r') as file:
            data = file.read().replace('\n', ' ')
            data = data.split('.I ')[1:]
            docs = { }
            
            for doc_str in data :
                
                res = re.split("\s+(\.T|\.B|\.A|\.K|\.W|\.X)+\s+",doc_str.strip())
                
                #id_doc
                docs[ res[0] ] = Document( res[0] )

                i = 1
                while ( i < len(res)  ) :
                    # Title 
                    if( res[i] == ".T" ) :
                        i += 1
                        docs[ res[0] ].setTitle( res[i] )
                    # Text
                    elif ( res[i] == ".W" ):
                        i += 1
                        docs[ res[0] ].setText( res[i] )
                    
                    # Graph PageRank
                    elif ( res[i] == ".X" ):
                        i += 1
                        #step 3
                        nodes = res[i].split()[::3]
                        # soccessors and predecessors pass
                        for n in nodes :
                            docs[ res[0] ].addSuccessor( n )
                            if ( n.isdigit()) :
                                if ( n not in docs ):
                                    docs[n] = Document(n)
                                docs[ n ].addPredecessor ( res[0] )
            

                        
                        
                    i += 1
                    
                    
            if ( console == True ) :
                Parser.display ( docs )
            if ( store !=  None ) :
                Parser.save ( docs , store  )
                
            
                
            return docs
    

        

