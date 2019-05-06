# -*- coding: utf-8 -*-
import numpy as np
import operator

class PageRank :
    
    @staticmethod
    def page_rank ( query  , model , collection , d =0.85 , aj=1 , Eps = 0.001 ,
                   max_iter = 20 ,  n=10 ,  k=5  ):
        
        np.random.seed(0)
        #################### building sub-graph ##################
        n_docs = model.getRanking(query)[:n]
        if ( len(n_docs) == 0 ):
            return []
        nodes = set( np.array ( n_docs )[:,0] ) 
        del n_docs 
        graph_pred = {}
        
        final_nodes = nodes.copy()
        for node in nodes :
            
            preds = set ( collection[node].getPredecessors().keys() )
            if ( len(preds) > 0 ):
                # all successors 
                final_nodes.update( preds )
                # select k predecessors and add them to the sub graph
                preds = np.array(list(preds))
                np.random.shuffle(preds)
                k_pred_set = set ( preds[:k]  )
                final_nodes.update(k_pred_set)
                # save predecessors <=> consume memory and gain execution time ( trade off !) 
                graph_pred[node] = np.array(list(k_pred_set))
                del preds
                del k_pred_set
           
        nodes = final_nodes
        ###########################################################
        
        
        ############  PAGE RANK ALGORITHM   ##############################
        
        # init 
        scores_prec = { node :  (1 / len(nodes))  for node in nodes }
        scores_current ={}
        it=0
        converg = False 
        
        while ( it < max_iter and not converg  ):
            
            for sj in scores_prec :
                sum_prod = 0
                
                #check if the node has predecessors  else score sj = (1-d) * aj
                if ( sj in graph_pred ) :
                    # select predecessors from sub-graph 
                    preds =  graph_pred[sj]
                    
                    if ( preds.shape[0] != 0 ) : 
                        
                        ###############  preparing numpy arrays for vectorization
                        si_vec , pij_vec = [] , []
                        for s in preds : 
                            si_vec.append(scores_prec[s])
                            # get successors only on sub-graphs
                            sub_sucessors = nodes.intersection( set ( collection[s].getSucessors().keys() ) )
                            # vectorize -> sum -> val / sum 
                            sub_sucessors = np.array (list(sub_sucessors))
                            pij_vec.append( collection[s].getSucessors()[sj] / 
                                            np.array( list(collection[s].getSucessors().values())).sum() )
                        
                        si_vec , pij_vec = np.array(si_vec) , np.array ( pij_vec )
                        ##############  
                        sum_prod = ( (si_vec*pij_vec).sum() )
                        
                scores_current [sj] = d * sum_prod  + (1-d) * aj
        
            factor=1.0/ np.array ( list( scores_current.values() ) ).sum() 
            scores_current = {k: round ( v*factor , 5 )  for k, v in scores_current.items() }
            print("iteration : ",it+1,"\n")
            # print ( scores_prec)
            #print ("prec :" , list( scores_prec.values()) )
            #print ( scores_current )
            #print ("curr :" , list( scores_current.values())  )
            L1 =np.abs ( np.array ( list( scores_prec.values()) )-
                        np.array ( list( scores_current.values()) ) ).sum()
            # we only need the max value to optimize memory and Time Complexity
            if ( L1 <= Eps ) :
                converg = True 
                
            print("\n L1 = ",L1)
            print("-------------------------------------")
            
            it += 1
            scores_prec = scores_current.copy()
            
            
        return sorted( scores_current.items() , key=operator.itemgetter(1) , reverse=True )
        
            
        
