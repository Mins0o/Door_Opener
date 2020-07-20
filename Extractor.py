import csv
import statistics

class Extractor:
    """The format of data is:
    (sound readings,labels)
    where
    sound readings is:
    [[v0_0,v0_1,...,v0_n1],...,[vm_0,...vm_nm]]
    and labels is:
    ["a","a",...,"y","y","z","z"]

    So ( [[n,...,n],[n,...,n],[n,...,n]] , ["a",...,"a"]  )
    """
    def __init__(self,options=[True,True,True,True]):
        """Options denotes which features the user is going to use"""
        self.options=options

    def amp(self,datum):
        """Returns local amplitude(stdev of three data points)
        """
        ampList=[]
        for i in range(len(datum)-2):
            ampList.append(statistics.stdev(datum[i:i+3]))
        ampList+=[0,0]
        return ampList
    
    def listIsPeak(self, datum):
        """This function is used to calculate period/frequency
        The return is a list of booleans telling if the data point is a peak(local max/min) or not
        """
        peakBoolList=[False]
        for i in range(len(datum)-2):
            peakBoolList.append((datum[i+1]>datum[i] and datum[i+1]>=datum[i+2])or((datum[i+1]<datum[i] and datum[i+1]<=datum[i+2])))
        peakBoolList+=[False]
        return peakBoolList

    def period(self, datum):
        """This function uses the listIsPeak() to measure the distance between two peaks.
        """
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
        """Maximum peak"""
        if verbose:
            print("Maximum peak",end="\t")
        med=int(statistics.median(datum))
        return max([abs(i-med) for i in datum])

    def feature2(self,datum,verbose=False):
        """Maximum Amp"""
        if verbose:
            print("Maximum Amp",end="\t")
        return max(self.amp(datum))

    def feature3(self,datum,verbose=False):
        """Maximum period(peak to inversed peak distance)"""
        if verbose:
            print("Maximum period",end="\t")
        return max(self.period(datum))

    def feature4(self,datum,verbose=False):
        """Minimum period(peak to inversed peak distance)"""
        if verbose:
            print("Minimum period",end="\t")
        return min(self.period(datum))
        
    def readTsv(self,path):
        """Read the .tsv file saved by the DoorOpener recording and return data format"""
        temp=list(csv.reader(open(path, 'r'), delimiter='\t'))
        return([[int(x) for x in line[0].split(",")] for line in temp],[line[1] for line in temp])

    def features(self,data,verbose=False):
        """ This function runs the data through all the functions above to create a pack of features.
        The features can be added, deleted or edited in this source code.
        """
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
