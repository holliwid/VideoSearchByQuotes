from pymongo import MongoClient
from os import listdir
from os.path import isfile, join
import json




def raw_to_prepared_data(path_text, data_video):
    onlyfiles = [f[:-4] for f in listdir(path_text) if isfile(join(path_text, f))]
    print(onlyfiles)
    data_video = [x.split('*|*') for x in open(data_video, 'r').read().split('\n')]
    res = []
    for data in data_video:
        print(data[0].replace('&#39;', "'"))
        if data[0].replace('&#39;', "'") in onlyfiles:
            name = data[0].replace('&#39;', "'")
            res.append({'name': name, 'url': data[1], 'duration': data[2], 'text': open(f'{path_text}/{name}.txt', 'r').read()})

    return res

data = (raw_to_prepared_data('prepared_text_of_video', 'url_of_videos.txt'))

for x in data:
    print(x)



def download_data_to_bs(data):
    client = MongoClient('localhost', 27017)

    db = client['Video_information']

    series_collection = db['series']

    list = []
    for x in data:
        if not series_collection.find_one({},{'name': x['name']}):
            list.append(x)
    try:
        series_collection.insert_many(list)
        series_collection.create_index({('text', 'text')})
    except:
        pass

download_data_to_bs(data)