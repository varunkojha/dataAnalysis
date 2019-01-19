import pandas as pd
import simplejson as json

text = open("doc_energy.txt", "r").read()
json_text = json.loads(text)
print(type(json_text))

with open('data.json', 'w') as outfile:  
    json.dump(json_text, outfile)

df = pd.read_json("data.json")
df.to_excel('output.xls', index=False)
