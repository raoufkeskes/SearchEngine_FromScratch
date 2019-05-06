# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:20:50 2019

@author: raoufks
"""

import numpy as np
from tme1.TextRepresenter import PorterStemmer 


class Query(object):
   
    def __init__( self , ident , text='', relevant_doc= dict() ):
        
        self.id = ident
        self.text=text
        self.relevant_doc=dict()
        
    def get_id ( self ) : 
        return self.id
    
    def getText(self) :
        return self.text
    
    def get_relevant_doc(self ) :
        return self.relevant_doc
    
    def add_relevant_doc(self,id_doc , relevance ):
        self.relevant_doc[id_doc] = relevance
        
    def setText(self,text):
        self.text=text
        
    def set_relevant_doc(self,relevant_doc):
        self.relevant_doc=relevant_doc
    
    def get_relevance_for_docs(self , docs):
        return np.vectorize (lambda el :
            self.relevant_doc[el] if (el in self.relevant_doc) else 0
            )( np.array(docs) )
            
            
    def getJsonFormat (self): 
        return { "Text"  : self.text , "Docs" : ' '.join(self.relevant_doc) }

