from sklearn.gaussian_process import GaussianProcessClassifier
from FeatureExtractor import Extractor
import pickle

class Classifier:
    def __init__(self,loadPath=None,trainData=(["1's features","2's features"],["y","n"]),
                 extractorOptions=[True,False,True]):
        if not loadPath==None:
            self.gpc,self.ext=pickle.load(loadPath)
        elif not (trainData==(["1's features","2's features"],["y","n"]) or extractorOptions==[True,False,True]):
            self.ext=Extractor(extractorOptions)
            fetures=self.ext.features(trainData[0])
            labels=trainData[1]
            self.gpc=GaussianProcessClassifier().fit(features,labels)
        else:
            raise Exception("Either path to saved classifier or (dataset+extractor options) should be given")

    def save(self):
        fileName=input("What should the file name be for this classifier?")
        pickle.dump((self.gpc,self.ext),"./"+fileName)
        
    def predict(self,x):
        return self.gpc.predict(self.ext.features(x))

    def evaluate(self,evalData):
        predictions=self.gpc.predict(evalData[0])
        answers=evalData[1]
        tp=0
        fp=0
        fn=0
        tn=0
        for i in range(len(predictions)):
            if(predictions[i]=="y" && answers[i]=="y"):
                tp+=1
            elif(predictions[i]=="y" && answers[i]=="n"):
                fp+=1
            elif(predictions[i]=="n" && answers[i]=="y"):
                fn+=1
            else:
                tn+=1
        precision=tp/(tp+fp)
        recall=tp/(tp+fn)
        accuracy=(tp+tn)/len(predictions)
        print("precision: \t\t{0}\nrecall: \t\t{1}\naccuracy: \t\t{2}".format(precision,recall,accuracy))
        
    
