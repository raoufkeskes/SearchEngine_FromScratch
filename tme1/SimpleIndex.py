# -*- coding: utf-8 -*-
from tme1.TextRepresenter import PorterStemmer 
from tme1.parser import Parser
import json 
import numpy as np

'''
Note :
    The TF in this project means the term counting and not the frequency because
    the counting will not affect the result of our IR Models .
    The reason is that we devide all formulas by N = len(doc) and it s
    a constant , it will not be discriminant for decisions !
'''


class SimpleIndex : 
    
    def __init__( self , filename , lower=True , stemm=True , stopwords=True  ):
        
        self.index_occ = dict()
        self.inverted_index_occ = dict()
        self.index_occ_normalized =dict()
        self.inverted_index_occ_normalized =dict()
        self.collection = dict()
        self.collection_filename = filename
        self.lower = lower 
        self.stemm = stemm
        self.stopwords = stopwords 
        
    
    def store ( self, dictionary , filename ) :
        with open( filename , 'w' ) as file:
            file.write(json.dumps (dictionary,indent=2))
            
    '''
    store : store indexes in json  files to visualize it better
    '''
    def indexing( self ,  store=True , normalize=True  ) :
        
        self.collection =  Parser.buildDocCollectionSimple(self.collection_filename)
        
        docs = self.collection
        for idDoc in docs : 
            doc = docs[idDoc]
            brute_information = doc.getText()+" "+ doc.getTitle()
            self.index_occ[idDoc] = PorterStemmer().getTextRepresentation(
                    brute_information , self.lower , self.stemm , self.stopwords )
            
            #print("**", self.index_occ[idDoc]," ",self.stopwords)
            for word in self.index_occ[idDoc] : 
                
                if ( word not in self.inverted_index_occ ) : 
                    self.inverted_index_occ[word] = {}
                self.inverted_index_occ[word][idDoc] = self.index_occ[idDoc][word]
                
                
        if ( store ) :
            self.store(self.index_occ,
                       "OutputFiles/index_occ.json")
            self.store(self.inverted_index_occ,
                       "OutputFiles/inverted_index_occ.json")
            
        
        #normalizing
        if ( normalize ) :
            self.index_occ_normalized = dict()
            self.inverted_index_occ_normalized = dict()
            for word in self.inverted_index_occ :
                factor = 1.0 / sum( self.inverted_index_occ[word].values() )
                for doc in self.inverted_index_occ[word] : 
                    normalized_occ = round(self.inverted_index_occ[word][doc]*factor,2)
                    if ( word not in self.inverted_index_occ_normalized ) :
                        self.inverted_index_occ_normalized[word] = dict()
                    self.inverted_index_occ_normalized[word][doc] =normalized_occ
                    #Same Information
                    if ( doc not in self.index_occ_normalized ) : 
                        self.index_occ_normalized[doc] = dict()
                    self.index_occ_normalized[doc][word] = normalized_occ
                    
            if ( store ) :
                self.store(self.index_occ_normalized ,
                           "OutputFiles/index_normalized.json")
                self.store(self.inverted_index_occ_normalized,
                           "OutputFiles/inverted_index_normalized.json")
        
        
        
    def getTfsForDoc(self,doc_id):
        '''
        return a dict of all document s terms with their counting
        '''
        return self.index_occ[doc_id]
        
        
    def getTfIDFsForDoc(self,doc_id):
        '''
        return a dict of all document s terms with their TF-IDF 
        '''
        tf=self.getTfsForDoc(doc_id)
        tf_idf = dict()
        for word in tf:
            tf_idf[word] = round ( tf[word] * \
                  np.log ((1+len (self.index_occ) ) /  \
                  (1+len(self.inverted_index_occ[word])) ) , 2 )
        return tf_idf
        
    def getTfsForStem(self,word):
        '''
        return a dict of all documents that contain a term with the counting 
        this one 
        '''
        t = PorterStemmer().getTermRepresentation(word , self.lower , self.stemm , self.stopwords )
        if ( t in self.inverted_index_occ ):
            return self.inverted_index_occ[t]
        else : return {}
        
    def getTfIDFsForStem(self,word):
        '''
        return TF-IDF of all documents containing a term
        '''
        res=dict() 
        t = PorterStemmer().getTermRepresentation(word , self.lower , self.stemm , self.stopwords )
        if ( t not in self.inverted_index_occ  ):
            return res
        for doc in self.inverted_index_occ[t] :
            res[doc]=self.getTfIDFsForDoc(doc)[t]
        return res 
    
    def getIDFforStem ( self, word ) :
        '''
        return the IDF value for a term
        '''
        t = PorterStemmer().getTermRepresentation(word , self.lower , self.stemm , self.stopwords )
        if ( t not in self.inverted_index_occ  ):
            return 0
        return ( round ( np.log ((1+len (self.index_occ) )/(1+len(self.inverted_index_occ[t])) ),5) )

    def getStrDoc(self,idDoc):
        '''
        return a string describing the content of a document whose
        -> ( title , text , ... ) in a json format 
        '''
        return str( self.collection[idDoc].getJsonFormat() )
    
    def getIndex(self, normalize=False ) :
        return self.index_occ if (not normalize) else self.index_occ_normalized
    
    def getInvertedIndex(self,normalize=False ):
        return ( self.inverted_index_occ if ( not normalize)  else 
                 self.inverted_index_occ_normalized ) 
        
    def getCollection(self):
        return self.collection
    

                    
        


                    
