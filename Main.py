from tme1.parser import Parser
from tme1.SimpleIndex import SimpleIndex
from tme2 import Weighter,IRModel
from tme3 import QueryParser , EvalMesure , evalIRmodel
from time import time
from tme4.PageRank import PageRank
import numpy as np
from tabulate import tabulate



###############################################  TME 1 ###############################################


def testBuildingCollectionSimple():
    t = time()
    docs =  Parser.buildDocCollectionSimple("data/cacm/cacm.txt")
    '''
    - IF the dictionary of the collection is small use Parser.display(docs)
      to see its content . 
    - ELSE use : Parser.store ( dict , "PATH/filename.json" ) 
    '''
    print(len(docs))
    Parser.save(docs,'OutputFiles/CollectionDictionary.json')
    print ("Build Collection Simple \nexecuting time :" , round ( time() - t , 2 ) ," seconds ."  )

def testBuildingCollectionRegex():
    t = time()
    docs =  Parser.buildDocCollectionRegex("data/cacm/cacm.txt")
    Parser.save(docs,'OutputFiles/CollectionDictionary.json') 
    print ("Build Collection using Regex \nexecuting time :" , round ( time() - t , 2 ) ," seconds ."  )
    
    
def testIndex():
    t = time()
    '''
    - Default parameters for the constructor SImpleIndex:
        --> lower=True , stemm=True , stopwords=True
    - you can change it to test other initial values !
    '''
    index1 = SimpleIndex("data/cacm/ex1.txt" , stopwords=False , stemm=True , lower=True  )
    index1.indexing()
    
    
    #params
    
    doc_test ="B"
    stem_test = "discover"
    
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

    
def testWeighter():
    t = time()
    index1 = SimpleIndex("data/cacm/ex1.txt")
    index1.indexing()
    
    doc="B"#"1"
    stem="discover" #"class"
    query ="hello world discover"  #"program algebra "
    
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
    
def testVectorialModel():
    t = time()
    index1 = SimpleIndex("data/cacm/ex1.txt")
    index1.indexing()
    m = IRModel.Vectorial ( Weighter.Ponder2( index1 ) , normalize=True )
    query = "hello world world world  line line algebra "
    print("Scores : ",m.getScores(query))
    print("Ranking : ",m.getRanking(query))
    print("\nexecuting time :" , round ( time() - t , 2 ) ," seconds ."  )

    
    
def testLangModel():
    t = time()
    index1 = SimpleIndex("data/cacm/cacmShort-good.txt")
    index1.indexing()
    query = "hello world world world  line line algebra "
    m = IRModel.ModeleLangue ( Weighter.Ponder2( index1 )  )
    print("Scores : ",m.getScores(query))
    print("Ranking : ",m.getRanking(query))
    print ("\nexecuting time :" , round ( time() - t , 2 ) ," seconds ."  )
    
    
def testOkapiBM25():
    index1 = SimpleIndex("data/cisi/cisi.txt")
    index1.indexing()
    m = IRModel.Okapi ( Weighter.Ponder2( index1 ) )
    query = "computer algebra "
    print("Scores : ",m.getScores(query))
    print("Ranking : ",m.getRanking(query))
   
    
###############################################  TME 3 ###############################################

def QueryParserTest():  
    queries = QueryParser.QueryParser.Parse("data/cisi/cisi.qry" , "data/cisi/cisi.rel" )
    Parser.save( queries ,'OutputFiles/QueryCollection.json' )
    
    
    
    
def Test_Recall_Precision_Fmesure():
    start = time()
    
    
    q = "15"
    model ="ModeleLangue"
    
    collection = "cisi"
    index1 = SimpleIndex("data/"+collection+"/"+collection+".txt" )
    index1.indexing()
    queries = QueryParser.QueryParser.Parse("data/"+collection+"/"+collection+".qry",
                                            "data/"+collection+"/"+collection+".rel" )
    query = queries[q]
    
    
    # display the content of the query 
    # print ( Weighter.Ponder2( index1 ).getWeightsForQuery ( query.getText() ))
    
    print("testing ",model," Model !")
    print("collection : ",collection )
    m = getattr(IRModel, model)( Weighter.Ponder2( index1 )  )
    retrieved_docs = m.getRanking( query.getText() , scoring=False )
    print(retrieved_docs[:10])
    R = EvalMesure.Recall().evalQuery(    retrieved_docs , query )
    P = EvalMesure.Precision().evalQuery( retrieved_docs , query )
    F = EvalMesure.F_mesure().evalQuery ( retrieved_docs , query )
    print( " Rappel : " , R )
    print( " Precision : " , P )
    print( " F_mesure : " , F )
    
    
    end = time()
    print("executing time : " , end - start )
    
    
def Test_avgP():
    start = time()
    
    collection = "cisi"
    q = "1"
    model ="Vectorial"
    
    index1 = SimpleIndex("data/"+collection+"/"+collection+".txt")
    index1.indexing()
    queries = QueryParser.QueryParser.Parse("data/"+collection+"/"+collection+".qry",
                                            "data/"+collection+"/"+collection+".rel" )
    query = queries[q]
    # display the content of the query 
    # print ( Weighter.Ponder2( index1 ).getWeightsForQuery ( query.getText() ))
    
    print("testing ",model," Model !")
    print("collection : ",collection )
    m = getattr(IRModel, model)( Weighter.Ponder2( index1 )  )
    retrieved_docs = m.getRanking( query.getText() , scoring=False )
    avgP = EvalMesure.avgP().evalQuery( retrieved_docs , query )
    print( " AvgP : " , avgP )
    
    end = time()
    print("executing time : " , end - start )
    
    
    
def testMAP():
    start = time()
    
    collection = "cisi"
    model ="Okapi"
    
    index1 = SimpleIndex("data/"+collection+"/"+collection+".txt")
    index1.indexing()
    queries = QueryParser.QueryParser.Parse("data/"+collection+"/"+collection+".qry",
                                            "data/"+collection+"/"+collection+".rel" )
    m = getattr(IRModel, model)( Weighter.Ponder2( index1 )  )
    print("testing ",model," Model !")
    print("collection : ",collection )
    #get queries that has at least one relevant doc  to evaluate it !
    ls = [queries[k] for k in queries if len(queries[k].get_relevant_doc())!=0 ]
            
    MAP = EvalMesure.MAP().evaluate( m , ls  )
    print( " MAP : " , MAP )
    
    end = time()
    print("executing time : " , end - start )
    
    
def TestReciprocalRank():
    start = time()
    
    collection = "cisi"
    model ="Vectorial"

    index1 = SimpleIndex("data/"+collection+"/"+collection+".txt" )
    index1.indexing()
    queries = QueryParser.QueryParser.Parse("data/"+collection+"/"+collection+".qry",
                                            "data/"+collection+"/"+collection+".rel" )
    m = getattr(IRModel, model)( Weighter.Ponder2( index1 ) )
    print("testing ",model," Model !")
    print("collection : ",collection )
    ls = [queries[k] for k in queries if len(queries[k].get_relevant_doc())!=0 ]
    R = EvalMesure.MRR().evaluate( m , ls )
    print( " Mean Reciprocal Rank : " , R )
    
    end = time()
    print("executing time : " , end - start )

    
def Test_NDCG_mean():
    start = time()
    
    collection = "cisi"
    model ="Vectorial"

    index1 = SimpleIndex("data/"+collection+"/"+collection+".txt")
    index1.indexing()
    queries = QueryParser.QueryParser.Parse("data/"+collection+"/"+collection+".qry",
                                            "data/"+collection+"/"+collection+".rel" )
    m = getattr(IRModel, model)( Weighter.Ponder2( index1 ))
    print("testing ",model," Model !")
    print("collection : ",collection )
    ls = [queries[k] for k in queries if len(queries[k].get_relevant_doc())!=0 ]
    ndcg_mean = EvalMesure.NDCG().evaluate( m , ls )
    print( " NDCG : " , ndcg_mean )
    
    end = time()
    print("executing time : " , end - start )

def TuningParams_TrainTestSplitTest():
    start = time()
    
    collection = "cisi"
    model ="Okapi"

    index1 = SimpleIndex("data/"+collection+"/"+collection+".txt")
    index1.indexing()
    queries = QueryParser.QueryParser.Parse("data/"+collection+"/"+collection+".qry",
                                            "data/"+collection+"/"+collection+".rel" )
    m = getattr(IRModel, model)( Weighter.Ponder2( index1 ))
    print("testing ",model," Model !")
    print("collection : ",collection )
    ls = [queries[k] for k in queries if len(queries[k].get_relevant_doc())!=0 ]
    evalIRmodel.EvalIRModel.tuning_params \
    ( model=m , metric="MAP",method="split" , 
    queries=ls , grid_param={"k1":np.arange(0.8,2.0,0.1),"b":np.arange(0.8,1.1,0.1)} , param_method=0.8 )
    
    end = time()
    print("executing time : " , end - start )
    
def TuningParams_CrossValidationTest():
    start = time()
    
    collection = "cisi"
    model ="Okapi"

    index1 = SimpleIndex("data/"+collection+"/"+collection+".txt")
    index1.indexing()
    queries = QueryParser.QueryParser.Parse("data/"+collection+"/"+collection+".qry",
                                            "data/"+collection+"/"+collection+".rel" )
    m = getattr(IRModel, model)( Weighter.Ponder2( index1 ))
    print("testing ",model," Model !")
    print("collection : ",collection )
    ls = [queries[k] for k in queries if len(queries[k].get_relevant_doc())!=0 ]
    evalIRmodel.EvalIRModel.tuning_params \
    ( model=m , metric="MAP",method="cross_validation" , 
    queries=ls , grid_param={"k1":np.arange(1.2,1.4,0.1),"b":np.arange(0.8,1.1,0.1)} , param_method=5 )
    end = time()
    print("executing time : " , end - start )
    
    
def evalModelsTest(  ) : 
    start = time()
    
    collection = "cisi"

    index1 = SimpleIndex("data/"+collection+"/"+collection+".txt")
    index1.indexing()
    queries = QueryParser.QueryParser.Parse("data/"+collection+"/"+collection+".qry",
                                            "data/"+collection+"/"+collection+".rel" )
    m1 = getattr(IRModel, "Vectorial")( Weighter.Ponder2( index1 ))
    m2 = getattr(IRModel, "ModeleLangue")( Weighter.Ponder2( index1 )) 
    m3 = getattr(IRModel, "Okapi")( Weighter.Ponder2( index1 )) 
    print("collection : ",collection )
    # 5 queries 
    ls = [queries[k] for k in queries if len(queries[k].get_relevant_doc())!=0 ][:15]
    res = evalIRmodel.EvalIRModel.evalModels(models=[m1,m2,m3] , queries=ls  )
    
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
    

##########################  tme 4 ####################################"
    
def Exo1PagerankTest():
    index1 = SimpleIndex("data/cacm/ex1.txt")
    index1.indexing()
    m = IRModel.Vectorial ( Weighter.Ponder2( index1 ) )
    q = "hello hello worlds"
    PageRank.page_rank ( q , m , index1.getCollection()  )
    
def FullPageRank():
    
    start = time()
    index1 = SimpleIndex("data/cacm/cacm.txt")
    index1.indexing()
    m = IRModel.Vectorial ( Weighter.Ponder2( index1 ) )
    q = "computer coding Algebraic"
    
    '''
    default parameters :
        d =0.85 , aj=1 , Eps = 0.001 , max_iter = 20 ,  n=10 ,  k=5
    '''
    res = PageRank.page_rank ( q , m , index1.getCollection() , Eps=1e-7 )
    print(res)
    
    end = time()
    print("executing time : " , end - start )
    
    
if __name__ == '__main__':
    Exo1PagerankTest()