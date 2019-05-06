import operator
import numpy as np

class IRModel : 
    
    #abstract method 
    def getScores( self , query ) :
        pass
    
    def getRanking( self , query , scoring=True ) : 
        scores_couples = list(self.getScores(query).items())
        scores_couples.sort ( key=operator.itemgetter(1) , reverse=True )
        if ( scoring ):
            return scores_couples
        return [row[0] for row in scores_couples]
    
    
    
class Vectorial (IRModel):
    
    def __init__ ( self , Weighter , normalize=False ):
        self.indexer = Weighter.Indexer()
        self.weighter = Weighter
        self.normalize = normalize
        
    def getScores( self , query  ) :
        
        scores = dict()
        pertinent_docs = set()
        inverted_index = self.indexer.getInvertedIndex()
        query_dic = self.weighter.getWeightsForQuery(query)
        for word in query_dic :
            if ( word in inverted_index ) :
                pertinent_docs = pertinent_docs.union ( set( inverted_index[word].keys() ) )
            
        for doc in pertinent_docs : 
            doc_dic   = self.weighter.getWeightsForDoc(doc)
            doc_norm , query_norm , scores [doc]  = 0,0,0
            
            # vectorial product
            for word in query_dic :
                if ( word in doc_dic ) :
                    scores [doc] += (query_dic[word] * doc_dic[word])
                    query_norm   += query_dic[word]**2
                    doc_norm     += doc_dic[word]**2
                    
            # normalized ? divide by  we choose : |X| + |Y| after few tests  it works better 
            # others normalization : |X| * |Y|   ,  sqrt|X| + sqrt|Y|  ,  ......
            if ( self.normalize) :
                scores [doc] = round ( scores [doc] / (( np.sqrt(doc_norm) + np.sqrt(query_norm))) , 5 )
        return scores
    
    def set_params (self, normalize ):
            self.normalize = normalize 
    
    

class ModeleLangue(IRModel):
    
      def __init__ ( self , Weighter , smooth = 0.8  ):
        self.indexer = Weighter.Indexer()
        self.weighter = Weighter
        self.smooth = smooth
        #calculate once 
        inverted_index = self.indexer.getInvertedIndex()
        self.corpus_count_all_words = np.array(list([ np.array(list( inverted_index[word].values() )).sum() \
                                      for word in  inverted_index ])).sum()
        
      def getScores( self , query ) :
          
          scores = dict()
          pertinent_docs = set()
          inverted_index = self.indexer.getInvertedIndex()
          query_dic = self.weighter.getWeightsForQuery(query)
          for word in query_dic :
            if ( word in inverted_index ) :
                pertinent_docs = pertinent_docs.union ( set( inverted_index[word].keys() ) )
          
          
          for doc in pertinent_docs :
              doc_count_all_words = np.array ( list(self.indexer.getIndex()[doc].values()) ).sum()
              doc_tfs , corpus_tfs = list() , list()  
              for word in query_dic :
                  if ( doc in inverted_index[word] ):
                      doc_tfs.append ( inverted_index[word][doc] ) 
                  else :
                      doc_tfs.append(0)
                      
                  corpus_tfs.append ( np.array(list(inverted_index[word].values( ))).sum() )
              doc_tfs = np.array ( doc_tfs )
              corpus_tfs = np.array ( corpus_tfs  )
              terms_proba_arr = self.smooth * ( doc_tfs / doc_count_all_words ) + \
              (1-self.smooth) * ( corpus_tfs/self.corpus_count_all_words )
              
              # warning ! : if you keep proba product remove the rounding 
              scores[doc] = round ( (np.log(terms_proba_arr)).sum() , 5 ) 
              
              #scores[doc] = (terms_proba_arr).prod() 
          return scores
      
      def set_params ( self ,smooth ):
          self.smooth = smooth 
            
        
class Okapi(IRModel) : 
    
    def __init__ ( self , Weighter , k1 = 1.2 , b=0.75  ):
        self.indexer = Weighter.Indexer()
        self.weighter = Weighter
        self.k1 = k1
        self.b = b 
        
        self.avgdl = np.array([ np.array ( list( self.indexer.getIndex()[doc].values() ) ).sum()  \
        for doc in  self.indexer.getIndex() ]).sum() / len( self.indexer.getIndex())
    
    def getScores( self , query ) :
        
        scores = dict()
        pertinent_docs = set()
        # normalize to work with a real Term Frequency not the counting 
        inverted_index = self.indexer.getInvertedIndex( normalize=True )
        query_dic = self.weighter.getWeightsForQuery(query)
        for word in query_dic :
                pertinent_docs = pertinent_docs.union ( set( inverted_index[word].keys() ) )                
         
        for doc in pertinent_docs : 
            len_doc = np.array ( list(self.indexer.getIndex()[doc].values()) ).sum()
            scores[doc] = 0 
            for word in query_dic : 
                if (  doc in inverted_index[word] ) :
                   tf_qi =  inverted_index[word][doc]
                   idf_qi = np.log ( ( len( self.indexer.getIndex()) +len(inverted_index[word])+ 0.5)/
                                    ( len(inverted_index[word]) + 0.5 ) )
                   
                   scores[doc]+= idf_qi * ( tf_qi * (self.k1+1) ) / ( tf_qi + self.k1 *( 1 - self.b + self.b \
                                 * len_doc / self.avgdl ) ) 
        
        return scores 
    
    
    def set_params (self, k1 , b ):
            self.k1 = k1
            self.b = b