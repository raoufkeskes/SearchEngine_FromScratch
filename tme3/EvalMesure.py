# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:39:58 2019

@author: raoufkeskes
"""
import numpy as np

class EvalMesure :
    
    def evalQuery(self,liste,query):
        pass
    
    
class Recall(EvalMesure):
    
    def __init__( self , k=None ):
        self.rank = k
        
        
    def evalQuery(self,liste,query):
        
        
        
        if ( self.rank == None or self.rank > len(liste)  ) : 
            self.rank = len(liste)
        
        relevant_docs = set( list(query.get_relevant_doc().keys()) )
        retrieved_docs = set ( liste[:self.rank] )
        
        return ( len( retrieved_docs.intersection(relevant_docs) ) ) / len( relevant_docs )
    
class Precision(EvalMesure):
    
    def __init__( self , k=None ):
        self.rank = k
        
    def evalQuery(self,liste,query):
        
        if ( self.rank == None or self.rank > len(liste) ) : 
            self.rank = len(liste)
            
        s_liste=set(liste[:self.rank])
        s_relevant=set(list(query.get_relevant_doc().keys()))
        return (1/self.rank)*len(s_liste.intersection(s_relevant))
    
    
class F_mesure(EvalMesure):
    
    def __init__( self , k=None , Beta = 2 ):
        self.rank = k
        self.beta = Beta 
    
    def evalQuery(self,liste,query):
        
        if ( self.rank == None or self.rank > len(liste) ) : 
            self.rank = len(liste)
            
        R = Recall ( self.rank ).evalQuery(liste,query)
        P = Precision ( self.rank ).evalQuery(liste,query)
        
        if ( R == 0 or P == 0 ) :
            return 0
        
        return ( (1+self.beta**2) * (P*R) / (P*self.beta**2+R)  )
    


class avgP(EvalMesure):
    
    def __init__( self  ):
        pass
    
    def evalQuery(self,liste,query):
        relevant_dic = query.get_relevant_doc()
        
        if ( len(relevant_dic)==0 ):
            return 1
        
        S = 0
        n = len(liste)
            
        for k in range (n):
            S += ( int (liste[k] in relevant_dic) * Precision ( k+1 ).evalQuery(liste,query) ) 
        return S / len(relevant_dic)
        
    
class MAP(EvalMesure):
    
    def __init__( self ):
        pass
    
    
    def evaluate( self , m , queries ):
        queries_arr  = np.array ( queries ) 
        res = np.vectorize (lambda q : avgP().evalQuery( m.getRanking(q.getText(),scoring=False),q))(queries_arr)
        return res.mean()
        
        
    
class MRR(EvalMesure) : 
    
    def __init__( self ):
        pass
    
    
        
    def evaluate(self, m , queries ):
         
        def mrr (q,m):
            #the two lists are list of docs ID !
            expected_docs = np.array ( list(q.get_relevant_doc().keys()) )
            retrieved_docs = m.getRanking(q.getText(),scoring=False)
            for doc in (  retrieved_docs  ) : 
                detect_arr = np.nonzero ( expected_docs == doc )[0]
                if ( len(detect_arr) > 0 ) : 
                    return ( 1 / (detect_arr[0]+1) )
            return 0
        return (np.vectorize(mrr)( np.array( queries ) , m = m )).mean()
    
    
class NDCG(EvalMesure):
    
    def __init__(self,rank=None):
        # if we don t give the p as parameter we have to choose the size of retrieved_relevances
        # for each query individualy
        self.was_None = ( rank == None )
        self.p = rank
    
    
    def evaluate(self, m , queries ):
        
        def ndcg(q,m):
            expected_relevances = np.array ( list(q.get_relevant_doc().values()) )
            retrieved_relevances = q.get_relevance_for_docs( list( m.getScores( q.getText() ).keys() ) )
            
            if ( self.was_None ) :
                self.p = retrieved_relevances.shape[0]
            
            ranks = np.arange(1,self.p+1)
            max_expect_ind = min( self.p , expected_relevances.shape[0] )
            dcg_p = (retrieved_relevances[:self.p] / (np.log(ranks+1) / np.log(2)) ).sum()
            idcg_p= (expected_relevances[:self.p] / (np.log(ranks+1)[:max_expect_ind] / np.log(2)) ).sum()
            
            return dcg_p  / idcg_p
                
        return (np.vectorize(ndcg)( np.array(queries) , m = m )).mean()