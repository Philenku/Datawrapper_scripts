import pandas as pd
import numpy as np
import json 
from urllib.request import urlopen
from datawrapper import Datawrapper
import sys


url = "https://anecdata.org/rest_posts/rows.json?project_id=1039"
response = urlopen(url)
data_json = json.loads(response.read())

df = pd.DataFrame(data_json['rows'])

field_df = pd.DataFrame()
trashes = [[] for i in range(len(df['Field'][0])-3) ]
trash_names = [df['Field'][0][num]['name'] for num in range(len(df['Field'][0])-3)]
for i in reversed(range(df.shape[0])):
    for j in range(len(df['Field'][0])-3):
        trashes[j].append(df['Field'][i][j]['value'])
for num in range(len(trashes)):
    field_df[trash_names[num]]=trashes[num]
field_df.fillna(0,inplace=True)
count_df = field_df.sum(axis=0).to_frame().reset_index()

arg1 = sys.argv[1]
dw = Datawrapper(access_token = arg1 )
trash_count = dw.create_chart(title = "Trash count by type",
                chart_type= "d3-bars",
                data = count_df)
if len(sys.argv)==2:
    dw.publish_chart(trash_count['id'],display=True)
    dw.display_chart(trash_count['id'])
else:
    arg2 = sys.argv[2]
    id = dw.get_charts()[int(arg2)]['id']
    dw.delete_chart(id)
    dw.publish_chart(trash_count['id'],display=True)
    dw.display_chart(trash_count['id'])