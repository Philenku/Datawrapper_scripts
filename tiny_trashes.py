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

adopt_df = pd.DataFrame()
id_list,observed,geoprivacy,lat,lng,hotspot,username,row_id,license,licence_url= [],[],[],[],[],[],[],[],[],[]
for i in reversed(range(79)):
    id_list.append(df['Post'][i]['id'])
    observed.append(df['Post'][i]['sighted'])
    geoprivacy.append(df['Post'][i]['geoprivacy'])
    lat.append(df['Post'][i]['lat'])
    lng.append(df['Post'][i]['lng'])
    hotspot.append(df['Post'][i]['hotspot'])
    username.append(df['User'][i]['username'])
    row_id.append(df['TaxonSighting'][i]['id'])
    license.append(df['DataLicense'][i]['name'])
    licence_url.append(df['DataLicense'][i]['url'])

adopt_df['id'] = id_list
adopt_df['row_id'] = row_id
adopt_df['username'] = username
adopt_df['license'] = license
adopt_df['licence_url'] =licence_url
adopt_df['lat'] = lat
adopt_df['lng'] =  lng
adopt_df['geoprivacy'] = geoprivacy
adopt_df['hotspot'] = hotspot
adopt_df['observed'] = observed
adopt_df['row_id'] = adopt_df['row_id'].astype(int)


field_df = pd.DataFrame()
trashes = []
for i in range(12):
    trashes.append([])
for i in reversed(range(79)):
    for j in range(11):
        trashes[j].append(df['Field'][i][j]['value'])
    trashes[11].append(df['Field'][i][0]['foreign_id'])
field_df['row_id'] = trashes[11]
field_df['num_bottles']=trashes[0]
field_df['plastic_lids']=trashes[1]
field_df['bottle_caps'] = trashes[2]
field_df['forks_knives_and_spoons'] = trashes[3]
field_df['plastic_straws'] = trashes[4]
field_df['food_wrappers'] = trashes[5]
field_df['cigaretter_filters'] = trashes[6]
field_df['vape_cartilages'] = trashes[7]
field_df['foam_pieces'] = trashes[8]
field_df['glass_pieces'] = trashes[9]
field_df['plastic_pieces'] = trashes[10]
field_df['row_id']=field_df['row_id'].astype(int)

final_df = adopt_df.merge(field_df,on='row_id')
final_df.sort_values(by='row_id',inplace=True)


count_df = pd.DataFrame()
columns = ["foam_pieces","glass_pieces","plastic_pieces"]
for column in columns:
    count_df[column] = pd.Series([np.sum(final_df[column].values)])

count_df = count_df.transpose()
count_df =count_df.reset_index()
arg1 = sys.argv[1]
dw = Datawrapper(access_token = arg1 )
trash_count = dw.create_chart(title = "Tiny trashes",
                chart_type= "d3-pies",
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