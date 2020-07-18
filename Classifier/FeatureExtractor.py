import csv

class Extractor:
    def __init__(self,options):
        self.options=options

    
    def feature1(self,datum,verbose=False):
        if verbose:
            print("")
        

    def feature2(self,datum):

    def feature3(self,datum):
        

    def features(self,data):
        featureFunList=[self.feature1,self.feature2,self.feature3]
        resultStack=[]
        for datum in data:
            interim=[]
            for i in len(self.options):
                if self.options[i]:
                    interim.append(featureFunList[i]())
            resultStack.append(interim)
        return resultStack
    
        
