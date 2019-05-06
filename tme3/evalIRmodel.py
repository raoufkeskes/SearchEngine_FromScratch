# -*- coding: utf-8 -*-



import numpy as np 
from tme3 import EvalMesure


class EvalIRModel :
    
    
    @staticmethod
    def evalModels ( models  , queries , kk=None ):
        if ( kk==None ) : 
            kk = len(queries)
        ls = []   
        for m in models :
            ls2 = []
            for query in queries :
                retrieved_docs = m.getRanking( query.getText() , scoring=False )
                R = EvalMesure.Recall(kk).evalQuery(    retrieved_docs , query )
                P = EvalMesure.Precision(kk).evalQuery( retrieved_docs , query )
                F = EvalMesure.F_mesure(kk).evalQuery ( retrieved_docs , query )
                ls2.append([R,P,F])
            ls.append(ls2)
        return np.array(ls) 
    
    
    @staticmethod    
    def tuning_params ( model , queries , grid_param  , metric="MAP",method="split", param_method=0.8 ) : 
        
        '''
        grid parameters is a dictionary 
        
        '''
        # get numpy of all possibilities 
        possibilities = np.array(np.meshgrid(*list(grid_param.values()) )).T.reshape(-1,len(grid_param))
        #model 
        m = model
        best_score = -1
        best_d = {}
        params = grid_param.keys()
        print("GRID MATRIX : ",possibilities)
        # select the corresponding method
        if ( method =="split" ):
            print("training split : ")
            train_queries = queries [:int(param_method*len(queries))]
            test_queries  = queries [int(param_method*len(queries)):]
            
            for values in possibilities :
                print("values iteration :",values)
                d = dict (zip(params,values))
                model.set_params ( **d )
                score = getattr(EvalMesure,metric)().evaluate( m , train_queries  )
                if ( score > best_score ):
                    best_score = score
                    best_d = d
                    
            
            print(" best_score : ",best_score," best_param : ", best_d )
            print("testing ... ")
            model.set_params ( **best_d)
            print("Test result ...", getattr(EvalMesure,metric)().evaluate( m , test_queries  ))
            
                
        elif ( method =="cross_validation" ):

            K_folds = np.array_split(np.array(queries),param_method)
            final_score = 0
            final_params = []
            
            for k in range ( param_method ):
                print("iteration ",k)
                print ("training ...." )
                test_queries =  K_folds[k]
                train_queries = np.concatenate(K_folds[:k]+K_folds[k+1:]).ravel().tolist()
                best_score = -1
                best_d = {}
                # train 
                for values in possibilities :
                    d = dict (zip(params,values))
                    model.set_params ( **d )
                    score = getattr(EvalMesure,metric)().evaluate( m , train_queries  )
                    if ( score > best_score ):
                        best_score = score
                        best_d = d
                           
                #test
                print(" best_score : ",best_score," best_param : ", best_d )
                print("testing ... ")
                model.set_params ( **best_d)
                s = getattr(EvalMesure,metric)().evaluate( m , test_queries  )
                print("Test result ...",s)
                
                final_score += s 
                final_params.append(best_d)
                print("---------------------------------------")
            
            print("final mean score :",final_score/param_method)
            print("final ",param_method," best params :\n",final_params )
            
            
        
            
                
                
                    
                
            
                    
                
                
        
            
            
                
            
                

            