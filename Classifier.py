from sklearn.gaussian_process import GaussianProcessClassifier
from Extractor import Extractor
from os import listdir
from os import _exit
import pickle

class Classifier:
    def __init__(self,trainDataPath=None,
                 extractorOptions=[True,False,True],loadPath=None):
        if not loadPath==None:
            f=open(loadPath,"rb")
            self.gpc,self.ext=pickle.load(f)
            f.close()
        elif not (trainDataPath==None or extractorOptions==[True,False,True]):
            self.ext=Extractor(extractorOptions)
            data=ext.readTsv(trainDataPath)
            features=self.ext.features(data[0])
            labels=data[1]
            self.gpc=GaussianProcessClassifier().fit(features,labels)
        else:
            raise Exception("Either path to saved classifier or (dataset+extractor options) should be given")

    def save(self):
        fileName=input("What should the name of PICKLE file be for this classifier?\nex)trained\n")
        if fileName=="":
            fileName="trained"
        f=open("./data/"+fileName+".pkl",'wb')
        pickle.dump((self.gpc,self.ext),f)
        f.close()
        
    def predict(self,x):
        return self.gpc.predict(self.ext.features(x))

    def evaluate(self,evalDataPath,targetLabels=["y"]):
        data=self.ext.readTsv(evalDataPath)
        features=self.ext.features(data[0])
        predictions=self.gpc.predict(features)
        labels=data[1]
        tp=0
        fp=0
        fn=0
        tn=0
        for i in range(len(predictions)):
            if(predictions[i] in targetLabels and labels[i] in targetLabels):
                tp+=1
            elif(predictions[i] in targetLabels and not labels[i] in targetLabels):
                fp+=1
            elif(not predictions[i] in targetLabels and labels[i] in targetLabels):
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
            data=self.ext.readTsv(dataPath)
            features=self.ext.features(data[0],True)
        elif not data==None:
            features=self.ext.features(data,True)
        else:
            raise Exception("no data available")
        for i in features:
            print(i)
        
    
if __name__=="__main__":
    ext=Extractor()
    if(input("Are you here to evaluate?\n>>> ").lower()=="y"):
        itemsList=[f for f in listdir("data/") if f[-4:]==".pkl"]
        for item in range(len(itemsList)):
            print("{0}: {1}".format(item,itemsList[item]))
        clfPath=int(input("Select your classifier PICKLE file\n>>> "))
        clf=Classifier(loadPath="data/"+itemsList[clfPath])
        dataList=[f for f in listdir("data/") if f[-4:]==".tsv"]
        for datum in range(len(dataList)):
            print("{0}: {1}".format(datum,dataList[datum]))
        dataPath=int(input("Select your evaluation data\n>>> "))
        targetLabels=[l for l in input("target labels\n>>> ")]
        clf.evaluate("data/"+dataList[dataPath],targetLabels)
        _exit(0)
    opStr=input("Input your option string\nex)'fttt'\n>>> ")
    options=[]
    for l in opStr:
        if l=="t":
            options.append(True)
        else:
            options.append(False)
    itemsList=listdir("data/")
    for item in range(len(itemsList)):
        print("{0}: {1}".format(item, itemsList[item]))
    dataPath=int(input("Select your training data\n>>> "))
    clf=Classifier("data/"+itemsList[dataPath],options)
    clf.save()
