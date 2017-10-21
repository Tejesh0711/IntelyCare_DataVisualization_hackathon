import pandas as pd
import json

df = pd.read_csv('hk_svcreq_location_details.csv')
df.sort_values('caredate', inplace=True)
df = df.dropna(axis=0, how='any')
df = df.iloc[int(len(df)  * 0.35):]
df = df[(df.clat.map(str).values != 'null') &
		(df.plat.map(str).values != 'null') &
		(df.clong.map(str).values != 'null') &
		(df.plong.map(str).values != 'null')]
print(df)

df.to_csv('output.csv')

alldict = {}
alldict['type'] = 'FeatureCollection'
alldict['features'] = []


for index, row in df.iterrows():
	curdict = {}
	curdict['type'] = 'Feature'
	curdict['properties'] = {}
	for col in df.columns.values:
		curdict['properties'][col] = row[col]
	curdict['geometry'] = {'type': 'LineString', 'coordinates': [[row['plong'], row['plat']], [row['clong'], row['clat']]]}
	alldict['features'] += [curdict]

with open('output.json', 'w') as out:
	out.write(json.dumps(alldict))