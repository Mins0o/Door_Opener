from sklearn.gaussian_process import GaussianProcessClassifier
from FeatureExtractor import Extractor
import pickle

class Classifier:
    def __init__(self,trainDataPath=None,
                 extractorOptions=[True,False,True],loadPath=None):
        if not loadPath==None:
            self.gpc,self.ext=pickle.load(loadPath)
        elif not (trainDataPath==None or extractorOptions==[True,False,True]):
            self.ext=Extractor(extractorOptions)
            data=ext.tsvRead(trainDataPath)
            features=self.ext.features(data[0])
            labels=data[1]
            self.gpc=GaussianProcessClassifier().fit(features,labels)
        else:
            raise Exception("Either path to saved classifier or (dataset+extractor options) should be given")

    def save(self):
        fileName=input("What should the file name be for this classifier?")
        pickle.dump((self.gpc,self.ext),"./"+fileName)
        
    def predict(self,x):
        return self.gpc.predict(self.ext.features(x))

    def evaluate(self,evalDataPath):
        data=self.ext.tsvRead(evalDataPath)
        features=self.ext.features(data[0])
        predictions=self.gpc.predict(features)
        labels=data[1]
        tp=0
        fp=0
        fn=0
        tn=0
        for i in range(len(predictions)):
            if(predictions[i]=="y" and labels[i]=="y"):
                tp+=1
            elif(predictions[i]=="y" and labels[i]=="n"):
                fp+=1
            elif(predictions[i]=="n" and labels[i]=="y"):
                fn+=1
            else:
                tn+=1
        precision=tp/(tp+fp)
        recall=tp/(tp+fn)
        accuracy=(tp+tn)/len(predictions)
        print("Total accurancies: {0}\n".format(len(predictions)))
        print("precision: \t\t{0}\nrecall: \t\t{1}\naccuracy: \t\t{2}".format(precision,recall,accuracy))
        print("confusion matrix:\nP\\R\tY\tN\nY\t{0}\t{1}\nN\t{2}\t{3}".format(tp,fp,fn,tn))

    def showFeatures(self,dataPath=None,data=None):
        if not dataPath ==None:
            data=self.ext.tsvRead(dataPath)
            features=self.ext.features(data[0],True)
        elif not data==None:
            features=self.ext.features(data,True)
        else:
            raise Exception("no data available")
        for i in features:
            print(i)
        
    
if __name__=="__main__":
    ext=Extractor()
    options=[False,True,True,False]
    clf=Classifier("D:/Workspace/09 Mechatronic/01 Door_Opener/Door_Opener/trainData.tsv",options)
