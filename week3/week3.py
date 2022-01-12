from urllib.request import urlopen
import pandas as pd
import json

# 載入資料
response = urlopen('https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json')
jsonData = response.read()
data = json.loads(jsonData)

# 整理資料
df = pd.json_normalize(data['result']['results'])
df['address'] = df['address'].str.slice(start=5,stop=8)
df['file'] = df['file'].str.split(r'.jpg|.JPG')

pic = []
for i in range(len(df)):
    pic.append(df['file'][i][0] + '.jpg')
df['new_file'] = pic

# 整理成獨立的 DataFrame 並匯出
new_data = {'stitle':df['stitle'],'area':df['address'],'long':df['longitude'],'lat':df['latitude'],'file':df['new_file']}
df2 = pd.DataFrame(new_data)
df2.to_csv('data.csv',index=False,header=None)