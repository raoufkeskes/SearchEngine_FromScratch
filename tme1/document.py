class Document : 
    
    # Default constructor
    def __init__ ( self , _id ):
        # initialize 
        self.id  = _id
        self.title =""
        self.text= ""
        self.succ = dict()
        self.pred = dict()
    
    
    #Setters
    def setText(self,Text): 
        self.text = Text
    
    def setTitle(self,Title):
        self.title = Title 
        
    def addSuccessor(self,idDoc):
        if ( idDoc in self.succ  ):
            self.succ[idDoc] += 1
        else :
            self.succ[idDoc] = 1
            
    def addPredecessor(self,idDoc):
        if ( idDoc in self.pred  ):
            self.pred[idDoc] += 1
        else :
            self.pred[idDoc] = 1
    
    #Getters 
    def getId (self):
        return self.id
    
    def getText (self): 
        return self.text
    
    def getTitle (self): 
        return self.title
    
    def getSucessors(self):
        return self.succ
    
    def getPredecessors(self):
        return self.pred
    
    
    def getJsonFormat (self): 
        return { "Title" : self.title , "Text"  : self.text , "sucessors" :  self.succ , "predecessors" : self.pred  }
        
        
     