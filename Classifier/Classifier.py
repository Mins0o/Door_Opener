from sklearn.gaussian_process import GaussianProcessClassifier
import pickle

class Classifier:
    def __init__(self,loadClf=None,featureData=None):
        if not loadClf==None:
            self.gpc=pickle.load(loadClf)
        elif not featureData==None:
            self.gpc=GaussianProcessClassifier().fit(featureData)
        else:
            raise Exception("Either save classifier path or dataset should be given")

    
    
