import json

name = list()
name = list()
token = list()
opttype = list()
size = list()
date = list()

with open('print_job.json') as f:
  data = json.load(f)
  for job in data['print_job']:
    name.append(job['name'])
    token.append(job['access_token'])
    opttype.append(job['type'])
    size.append(job['size'])
    date.append(job['date'])
		
print(name)
