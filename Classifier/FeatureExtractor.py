import csv
import statistics

class Extractor:
    def __init__(self,options=[True,True,True,True]):
        self.options=options

    def amp(self,datum):
        ampList=[]
        for i in range(len(datum)-2):
            ampList.append(statistics.stdev(datum[i:i+3]))
        ampList+=[0,0]
        return ampList
    
    def listIsPeak(self, datum):
        peakBoolList=[False]
        for i in range(len(datum)-2):
            peakBoolList.append((datum[i+1]>datum[i] and datum[i+1]>=datum[i+2])or((datum[i+1]<datum[i] and datum[i+1]<=datum[i+2])))
        peakBoolList+=[False]
        return peakBoolList

    def period(self, datum):
        lip=self.listIsPeak(datum)
        periods=[]
        for i in range(len(lip)):
            if lip[i]:
                j=1
                while i+j<len(lip)-1 and not lip[i+j]:
                    j+=1
                if lip[i+j]:
                    periods.append(j)
                i=i+j
        return periods
        
    def feature1(self,datum,verbose=False):
        if verbose:
            print("Maximum peak",end="\t")
        med=int(statistics.median(datum))
        return max([abs(i-med) for i in datum])

    def feature2(self,datum,verbose=False):
        if verbose:
            print("Maximum Amp",end="\t")
        return max(self.amp(datum))

    def feature3(self,datum,verbose=False):
        if verbose:
            print("Maximum period",end="\t")
        return max(self.period(datum))

    def feature4(self,datum,verbose=False):
        if verbose:
            print("Minimum period",end="\t")
        return min(self.period(datum))
        
    def tsvRead(self,path):
        temp=list(csv.reader(open(path, 'r'), delimiter='\t'))
        return([[int(x) for x in line[0].split(",")] for line in temp],[line[1] for line in temp])

    def features(self,data,verbose=False):
        featureFunList=[self.feature1,self.feature2,self.feature3,self.feature4]
        resultStack=[]
        if verbose:
            lineNum=0
        for datum in data:
            interim=[]
            if verbose:
                print("line{}: ".format(lineNum),end="")
                lineNum+=1
            for i in range(len(self.options)):
                if self.options[i]:
                    interim.append(featureFunList[i](datum,verbose))
            if verbose:
                        print()
            resultStack.append(interim)
        return resultStack

if __name__=="__main__":
    ext=Extractor()
    #print(ext.features(ext.tsvRead("D:/Workspace/09 Mechatronic/01 Door_Opener/Door_Opener/data.tsv")[0],True))
    tot=ext.tsvRead("D:/Workspace/09 Mechatronic/01 Door_Opener/Door_Opener/trainData.tsv")[0]
    a=ext.tsvRead("D:/Workspace/09 Mechatronic/01 Door_Opener/Door_Opener/trainData.tsv")[0][0]
