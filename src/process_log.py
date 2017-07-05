import sys
import json
import operator
import subprocess
import re
import json


def freq(file,testFile):
    id =[]
    with open(file) as fp:
      first_line = json.loads(fp.readline())
      degree = first_line["D"]
      total = first_line["T"]
      list = []
      for line in fp:
        if(json.loads(line)['event_type'] == "purchase"):
            a=json.loads(line)['id']
            id.append(a)
    fp.close()      
    
    finalList = {}
    for i in id:  
      with open(file) as f1:
        first_line = json.loads(f1.readline())
        d = []
        for line in f1: 
            if(json.loads(line)['event_type'] == "befriend"):
                if(json.loads(line)['id1'] == i):
                    d.append(json.loads(line)['id2'])
                elif(json.loads(line)['id2'] == i):
                    d.append(json.loads(line)['id1'])        
                finalList[i] = d
    f1.close()    
    count = -1
    for i in finalList:
      amount = [0] * len(finalList)   
      count = count + 1
      matchCount = 0
      d = [] 
      for j in range(0,len(finalList[i])):
        individualAmount = [0] * len(finalList[i])   
        with open(file) as f1:
            first_line = json.loads(f1.readline())
            for line in f1:
                if(json.loads(line)['event_type'] == "purchase"):
                    if(json.loads(line)['id'] == finalList[i][j]):
                        matchCount = matchCount + 1
                        amount[count] = amount[count] + float(json.loads(line)['amount'])
                        individualAmount[j] = float(json.loads(line)['amount']) 
      mean = amount[count]/matchCount
      sd = 0.0
      for k in range(0,len(individualAmount)):
        sd = sd + (individualAmount[k]-mean)*(individualAmount[k]-mean)
      finalsd = (sd/matchCount)**(.5)  
      mean = amount[count]/matchCount
      d.append(amount[count])
      d.append(mean)
      d.append(finalsd)                      
      finalList[i] = d

    f1.close()
    findingAnamoly(finalList,testFile)


def findingAnamoly(finalList,testFile):
    f= open("flagged_purchases.json","w+")
    for i in finalList:
      with open(testFile) as f1:
        first_line = json.loads(f1.readline())
        for line in f1:
            if(json.loads(line)['event_type'] == "purchase"):   
                if(json.loads(line)['id'] == finalList[i]):
                    finalAmount = finalList[i][1] + (3 * finalList[i][2])
                    if(json.loads(line)['amount'] > finalAmount):
                        f.write(line)

    f.close()
    f1.close()                

def main():
    batch_log = open(sys.argv[1])
    stream_log = open(sys.argv[2])
    freq(sys.argv[1],sys.argv[2])

if __name__ == '__main__':
    main()
    

