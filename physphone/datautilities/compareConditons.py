import numpy as np
import statsmodels.api as sm

def averageArray(data):
    total=0
    count=0
    for item in data:
        total=total+item
        count=count+1
    return float(total)/float(count)
def extractHF(data):
    filtered=[]    
    for index in range(0,len(data)):
        total=0.0
        count=0.0
        for point in range(-2,2):
            fullIndex=index+point;
            if (fullIndex >= 0 and fullIndex < len(data)):
                total=total+data[fullIndex]
                count=count+1
        lfpower=total/count
        filtered.append(abs(data[index]-lfpower))
    return filtered
def extractLF(data):
    filtered=[]    
    for index in range(0,len(data)):
        total=0.0
        count=0.0
        for point in range(-2,2):
            fullIndex=index+point;
            if (fullIndex >= 0 and fullIndex < len(data)):
                total=total+data[fullIndex]
                count=count+1
        lfpower=total/count
        filtered.append(lfpower)
    return filtered
def getData():
    fileName=raw_input()
    datafile=open(fileName,'r')
    theData=datafile.readlines()
    lastLine=theData[len(theData)-1]
    datafile.close()
    val=[]
    xacc=[]
    yacc=[]
    zacc=[]
    for line in theData:
        splitup=line.split(",")
        val.append(float(splitup[1]))
        xacc.append(float(splitup[2]))
        yacc.append(float(splitup[3]))
        zacc.append(float(splitup[4]))
        if (line == lastLine):
            break
    print("If the data includes a baseline, enter the last baseline sample, otherwise press enter")
    baseChoice=raw_input()
    if len(baseChoice) >= 1:
        tc=int(baseChoice)
        baseMean=averageArray(val[1:tc])
        xMean=averageArray(xacc[1:tc])
        yMean=averageArray(yacc[1:tc])
        zMean=averageArray(zacc[1:tc])
        newVal=[]
        newX=[]
        newY=[]
        newZ=[]
        for item in range(tc,len(val)):
            newVal.append(val[item]-baseMean)
            newX.append(xacc[item]-xMean)
            newY.append(yacc[item]-yMean)
            newZ.append(zacc[item]-zMean)
        return [newVal,newX,newY,newZ]
    else:
        return [val,xacc,yacc,zacc]
    
print("Enter data series 1, then DONE")
data1=getData()
print("Enter data series 2, then DONE")
data2=getData()


hf1=extractHF(data1[0])
hf2=extractHF(data2[0])
lf1=extractLF(data1[0])
lf2=extractLF(data2[0])
alldata=[]
allhf=[]
allx=[]
ally=[]
allz=[]
datatype=[]
constant=[]
for item in range(0,len(data1[0])):
    alldata.append(data1[0][item])
    allhf.append(hf1[item])
    allx.append(data1[1][item])
    ally.append(data1[2][item])
    allz.append(data1[3][item])
    constant.append(1);
    datatype.append(1)
for item in range(0,len(data2)):
    alldata.append(data2[0][item])
    allhf.append(hf2[item])
    allx.append(data2[1][item])
    ally.append(data2[2][item])
    allz.append(data2[3][item])
    constant.append(1)
    datatype.append(2)

predictors=np.transpose(np.asarray([alldata,allhf,allx,ally,allz,constant]))
est = sm.OLS(datatype, predictors)
est.data.xnames=['Measured value','HF power','X acc','Y acc','Z acc','constant']

est = est.fit()
if (est.pvalues[0] < 0.05):
    print("Red light value appears to differ between conditions (p< 0.05) , correcting for HF power and movement")
else:
    print("Red light value does not appear to differ between conditions (p>= 0.05) , correcting for HF power and movement")
print("Statistics details:")
print(est.summary())
outFile=open("processedData.csv",'w')
outFile.write("data-1,data-2,hf power-1,hf power-2,lowpass filter-1,lowpass filter-2\n")
for item in range(0,min(len(data1[0]),len(data2[0]))):
    outFile.write(str(data1[0][item])+","+str(data2[0][item])+","+str(hf1[item])+","+str(hf2[item])+","+str(lf1[item])+","+str(lf2[item])+"\n")
outFile.flush()
outFile.close()
raw_input()

        
