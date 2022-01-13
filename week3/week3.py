from urllib.request import urlopen
import json,csv

# 載入資料
response = urlopen('https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json')
jsonData = response.read()
data = json.loads(jsonData)

# 整理資料
filelist = [];output = []
mainData = data['result']['results']

for i in range(len(mainData)):
    out = []
    out.append(mainData[i]['stitle'])
    out.append(mainData[i]['address'][5:8])
    out.append(mainData[i]['longitude'])
    out.append(mainData[i]['latitude'])
    filelist = mainData[i]['file'].split('https')
    out.append('https' + filelist[1])
    output.append(out)

# 輸出資料
with open('data.csv','w',encoding='utf-8',newline='') as file:
    write = csv.writer(file)
    write.writerows(output)