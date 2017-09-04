import urllib2
import time
print("Enter the maximum length of the recording (in seconds). This determines how much memory will be allocated.")
recLength=int(raw_input())
sampLength=recLength*4
dbuffer=[]
tbuffer=[]
xbuffer=[]
ybuffer=[]
zbuffer=[]
sampleSet=False
firstSample=0
for i in range(0,sampLength):
    dbuffer.append(-1000)
    tbuffer.append(0)
    xbuffer.append(0)
    ybuffer.append(0)
    zbuffer.append(0)
lastWrite=0
writeSeconds=10
print("Enter the stream id")
streamID=raw_input()
print("OK. Press enter to start recording")
print("Starting recording")
while True:
    req = urllib2.urlopen('http://biostream-1024.appspot.com/get?stream='+streamID)
    data=req.read()
    data=data.split("\n")[1] #get rid of human-readable segment
    data=data.split(",")
    if not sampleSet:
        firstSample=int(data[2])
        sampleSet=True
        print("Synced with biostream")
    dbuffer[int(data[2])-firstSample]=float(data[1])
    tbuffer[int(data[2])-firstSample]=int(data[0])
    xbuffer[int(data[2])-firstSample]=float(data[3])
    ybuffer[int(data[2])-firstSample]=float(data[4])
    zbuffer[int(data[2])-firstSample]=float(data[5])
    print("Packet: "+data[2], "+value: "+data[1])
    if (time.time() >= lastWrite+writeSeconds):
        lastWrite=time.time()
        outFile=open("log.csv",'w')
        lastGood=0
        lgx=0
        lgy=0
        lgz=0
        for i in range(0,len(dbuffer)):
            if (dbuffer[i] != -1000):
                outFile.write(str(tbuffer[i])+","+str(dbuffer[i])+","+str(xbuffer[i])+","+str(ybuffer[i])+","+str(zbuffer[i])+"\n")
                lastGood=dbuffer[i]
                lgx=xbuffer[i]
                lgy=ybuffer[i]
                lgz=zbuffer[i]
            else:
                outFile.write(str(tbuffer[i])+","+str(lastGood)+","+str(lgx)+","+str(lgy)+","+str(lgz)+"\n")
        outFile.flush()
        outFile.close()
        
    

    
    
