#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 14:13:00 2019

@author: 3701191
"""
from tme1.parser import Parser
from tme1.SimpleIndex import SimpleIndex
from tme2 import Weighter,IRModel
from tme3 import QueryParser , EvalMesure , evalIRmodel
from time import time
from tme4.PageRank import PageRank
import numpy as np
from tabulate import tabulate

############################################### Setting up ###########################################
##### collection
t = time()
docs =  Parser.buildDocCollectionSimple("data/cisi/cisi.txt")
'''
- IF the dictionary of the collection is small use Parser.display(docs)
  to see its content . 
- ELSE use : Parser.store ( dict , "PATH/filename.json" ) 
'''
print(len(docs))
Parser.save(docs,'OutputFiles/CollectionDictionary.json')
# queries
queries = QueryParser.QueryParser.Parse("data/cisi/cisi.qry" , "data/cisi/cisi.rel" )
Parser.save( queries ,'OutputFiles/QueryCollection.json' )

print ("Build Collection Simple  + Parse Queries \nexecuting time :" , round ( time() - t , 2 ) ," seconds ."  )
###############################################  TME 1 ###############################################

##### INDEX 
t = time()
'''
- Default parameters for the constructor SImpleIndex:
    --> lower=True , stemm=True , stopwords=True
- you can change it to test other initial values !
'''
index1 = SimpleIndex("data/cisi/cisi.txt" , stopwords=True , stemm=True , lower=True  )
index1.indexing()


#params
doc_test ="1"
stem_test = "algebra"

print ("\nstring of the doc '",doc_test,"' is : " , index1.getStrDoc(doc_test)  )
print ("\nTFs for document '",doc_test,"' ", index1.getTfsForDoc(doc_test) )
print ("\nTFIDFs for document '",doc_test,"' ", index1.getTfIDFsForDoc(doc_test) )
print ("#########################################################")

#TERM
print ("\nTFs for stem '",stem_test,"' ", index1.getTfsForStem(stem_test) )
print ("\nIDF for stem '",stem_test,"' ", index1.getIDFforStem(stem_test) )
print ("\nTFIDFs for stem '",stem_test,"' ", index1.getTfIDFsForStem(stem_test) )

print ("\nexecuting time :" , round ( time() - t , 2 ) ," seconds ."  )
print ( len(index1.index_occ_normalized) )



###############################################  TME 2 ###############################################
##### Weighters

t = time()
doc="1"
stem="class"
query ="program program program algebra algebra"

p = Weighter.Ponder1( index1 )
print("Ponder 1 :")
print( p.getWeightsForDoc(doc))
print("--------------------------")
print( p.getWeightsForQuery(query) )
print("--------------------------")
print( p.getWeightsForStem(stem) )
print("--------------------------")
print("####################################")

p = Weighter.Ponder2( index1 )
print("Ponder 2 :")
print( p.getWeightsForDoc(doc))
print("--------------------------")
print( p.getWeightsForQuery(query) )
print("--------------------------")
print( p.getWeightsForStem(stem) )
print("--------------------------")
print("####################################")
      
p = Weighter.Ponder3( index1 )
print("Ponder 3 :")
print( p.getWeightsForDoc(doc))
print("--------------------------")
print( p.getWeightsForQuery(query) )
print("--------------------------")
print( p.getWeightsForStem(stem) )
print("--------------------------")
print("####################################")
      
p = Weighter.Ponder4( index1 )
print("Ponder 4 :")
print( p.getWeightsForDoc(doc))
print("--------------------------")
print( p.getWeightsForQuery(query) )
print("--------------------------")
print( p.getWeightsForStem(stem) )
print("--------------------------")
print("####################################")
    
p = Weighter.Ponder5( index1 )
print("Ponder 5 :")
print( p.getWeightsForDoc(doc))
print("--------------------------")
print( p.getWeightsForQuery(query) )
print("--------------------------")
print( p.getWeightsForStem(stem) )
print("--------------------------")
print("####################################")

print ("\nexecuting time :" , round ( time() - t , 2 ) ," seconds ."  )


##### Models
t = time()
m = IRModel.Vectorial ( Weighter.Ponder2( index1 ) , normalize=True )
query = "hello world world world  line line algebra "
print("\nScores : ",m.getScores(query))
print("\nRanking : ",m.getRanking(query))
print("\nTOP 30 : \n",m.getRanking(query)[:30])
print("\nexecuting time :" , round ( time() - t , 2 ) ," seconds ."  )


t = time()
m = IRModel.ModeleLangue ( Weighter.Ponder2( index1 )  )
print("Scores : ",m.getScores(query))
print("Ranking : ",m.getRanking(query))
print("\nTOP 30 : \n",m.getRanking(query)[:30])
print ("\nexecuting time :" , round ( time() - t , 2 ) ," seconds ."  )


t = time()
m = IRModel.Okapi ( Weighter.Ponder2( index1 ) )
query = "computer algebra "
print("Scores : ",m.getScores(query))
print("Ranking : ",m.getRanking(query))
print("\nTOP 30 : \n",m.getRanking(query)[:30])
print("\nexecuting time :" , round ( time() - t , 2 ) ," seconds ."  )



###############################################  TME 3 ###############################################

start = time()

model ="Vectorial"
m = getattr(IRModel, model)( Weighter.Ponder2( index1 )  )

start = time()
q = "1"
query = queries[q]
k = 20 
print("testing ",model," Model !")


# display the content of the query 
# print ( Weighter.Ponder2( index1 ).getWeightsForQuery ( query.getText() ))
retrieved_docs = m.getRanking( query.getText() , scoring=False )

R = EvalMesure.Recall(k).evalQuery(    retrieved_docs , query )
P = EvalMesure.Precision(k).evalQuery( retrieved_docs , query )
F = EvalMesure.F_mesure(k).evalQuery ( retrieved_docs , query )
print( " Rappel : " , R )
print( " Precision : " , P )
print( " F_mesure : " , F )

avgP = EvalMesure.avgP().evalQuery( retrieved_docs , query )
print( " AvgP : " , avgP )


#get queries that has at least one relevant doc  to evaluate it !
ls = [queries[k] for k in queries if len(queries[k].get_relevant_doc())!=0 ]
MAP = EvalMesure.MAP().evaluate( m , ls  )
print( " MAP : " , MAP )
ls = [queries[k] for k in queries if len(queries[k].get_relevant_doc())!=0 ]
R = EvalMesure.MRR().evaluate( m , ls )
print( " Mean Reciprocal Rank : " , R )
ndcg_mean = EvalMesure.NDCG().evaluate( m , ls )
print( " NDCG : " , ndcg_mean )

end = time()
print("executing time : " , end - start )

###########  EVAL MODEL PLATFORM

start = time()
m1 = getattr(IRModel, "Vectorial")( Weighter.Ponder2( index1 ))
m2 = getattr(IRModel, "ModeleLangue")( Weighter.Ponder2( index1 )) 
m3 = getattr(IRModel, "Okapi")( Weighter.Ponder2( index1 )) 
# 5 queries 
ls = [queries[k] for k in queries if len(queries[k].get_relevant_doc())!=0 ][:10]
res = evalIRmodel.EvalIRModel.evalModels(models=[m1,m2,m3] , queries=ls )

print("\nReporting ")
print("--------------")
print("shape confirmation ", res.shape)
print("\nVectorial :")
print ( tabulate( res[0] , headers=['Precision' , 'Recall' , 'F1-score' ]  ) )
print ( "Mean :", np.mean(res[0],axis=0) , " Standard Deviation : ",np.std(res[0],axis=0))

print("\nModeleLangue :")
print ( tabulate( res[1] , headers=['Precision' , 'Recall' , 'F1-score' ]  ) )
print ( "Mean :", np.mean(res[1],axis=0) , " Standard Deviation : ",np.std(res[1],axis=0))

print("\nOkapi BM-25:")
print ( tabulate( res[2] , headers=['Precision' , 'Recall' , 'F1-score' ]  ) )
print ( "Mean :", np.mean(res[2],axis=0) , " Standard Deviation : ",np.std(res[2],axis=0))

end = time()
print("executing time : " , end - start )


# GRID SEARCH  SPLIT
start = time()    
model ="Okapi"

m = getattr(IRModel, model)( Weighter.Ponder2( index1 ))
print("testing ",model," Model !")
ls = [queries[k] for k in queries if len(queries[k].get_relevant_doc())!=0 ]
evalIRmodel.EvalIRModel.tuning_params \
( model=m , metric="MAP",method="split" , 
queries=ls , grid_param={"k1":np.arange(1.2,1.4,0.1),"b":np.arange(0.8,1.1,0.1)} , param_method=0.8 )

end = time()
print("executing time : " , end - start )


# GRID SEARCH CROSS VALIDATION
start = time()
model ="Okapi"

m = getattr(IRModel, model)( Weighter.Ponder2( index1 ))
print("testing ",model," Model !")
ls = [queries[k] for k in queries if len(queries[k].get_relevant_doc())!=0 ]
evalIRmodel.EvalIRModel.tuning_params \
( model=m , metric="NDCG",method="cross_validation" , 
queries=ls , grid_param={"k1":np.arange(1.2,1.5,0.1),"b":np.arange(0.5,0.8,0.1)} , param_method=5 )
end = time()
print("executing time : " , end - start )


# GRID SEARCH  SPLIT
start = time()    
model ="ModeleLangue"

m = getattr(IRModel, model)( Weighter.Ponder2( index1 ))
print("testing ",model," Model !")
ls = [queries[k] for k in queries if len(queries[k].get_relevant_doc())!=0 ]
evalIRmodel.EvalIRModel.tuning_params \
( model=m , metric="NDCG",method="split" , 
queries=ls , grid_param={"smooth":np.arange(0.5,1.0,0.1)} , param_method=0.8 )

end = time()
print("executing time : " , end - start )



    
    
    