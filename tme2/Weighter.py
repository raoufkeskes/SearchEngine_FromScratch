import numpy as np
from tme1.TextRepresenter import PorterStemmer 
from collections import Counter

class Weighter(object):
   
    def __init__( self , indexer ):
        '''
        Constructor
        '''
        self.indexer = indexer
        
    # abstract method
    def getWeightsForDoc ( self , idDoc ) : 
        pass
    
    # common method for all Ponderations
    def getWeightsForStem(self , stem ) :
        
        docs = self.indexer.getTfsForStem(stem)
        return { doc : round(self.getWeightsForDoc(doc)[ PorterStemmer().\
                             getTermRepresentation(stem , self.indexer.lower\
                             , self.indexer.stemm , self.indexer.stopwords )],5)  \
                             for doc in docs  }
    
    # abstract method
    def getWeightsForQuery(self , query ) :
        pass
    
    def Indexer(self):
        return self.indexer
    
class Ponder1 ( Weighter ):
    
    def getWeightsForDoc ( self , idDoc ) : 
        return self.indexer.getTfsForDoc(idDoc)
    
    
    
    def getWeightsForQuery( self , query ) :
        query_words = list(set(PorterStemmer().getQueryRepresentation ( query , self.indexer )))
        values = [1] * len(query_words)
        return dict(zip(query_words, values))
   

class Ponder2 ( Weighter ):
    
    def getWeightsForDoc ( self,idDoc ) : 
        return self.indexer.getTfsForDoc(idDoc)
    
    
    def getWeightsForQuery( self , query ) :
        return dict(Counter(PorterStemmer().getQueryRepresentation( query , self.indexer )))
                    
                    
class Ponder3 ( Weighter ):
    
    def getWeightsForDoc ( self,idDoc ) : 
        return self.indexer.getTfsForDoc(idDoc)
    
    def getWeightsForQuery( self , query ) :
        query_words = list(set(PorterStemmer().getQueryRepresentation ( query , self.indexer )))
        return { word : self.indexer.getIDFforStem(word) for word in query_words }
    
    
class Ponder4 ( Weighter ):    
    
    def getWeightsForDoc ( self,idDoc ) : 
        words_tfs = self.indexer.getTfsForDoc(idDoc) 
        return { word : round (1+ np.log ( words_tfs[word] ),5)  for word in words_tfs } 
    
    def getWeightsForQuery( self , query ) :
        query_words = list(set(PorterStemmer().getQueryRepresentation ( query , self.indexer )))
        return { word : self.indexer.getIDFforStem(word) for word in query_words } 
        
class Ponder5 ( Weighter ):    
    
    def getWeightsForDoc ( self,idDoc ) : 
        words_tf = self.indexer.getTfsForDoc(idDoc) 
        return { word : round( (1+ np.log (words_tf[word]))*self.indexer.getIDFforStem(word),5 ) \
                for word in words_tf } 
    
    def getWeightsForQuery( self , query ) :
        words_tf = dict(Counter(PorterStemmer().getQueryRepresentation( query , self.indexer )))
        print("***" , words_tf)
        return { word : round((1+ np.log (words_tf[word]))*self.indexer.getIDFforStem(word),5) \
                for word in words_tf }         
        
      
          