from pymongo import MongoClient
import datetime


client = MongoClient('localhost', 27017)
db = client['Video_information']
series_collection = db['series']

def search_quote(quote):
    series_collection.create_index([('text', 'text')])
    z = series_collection.find({'$text': {'$search': f"\"{quote}\""}})
    res_list = []
    for x in z:
        qt = x['text'].find(quote)
        if qt > 100:
            start = qt - 50
        else:
            start = qt - len(quote)

        if  qt + 50 < len(x['text']):
            end = qt + 50
        else:
            end = len(x['text'])
        print(x['text'][start:end])
        print(x)
        time = str(datetime.timedelta(seconds=(int(float(x['duration']) / len(x['text']) * qt))))
        res_list.append({'name': x['name'], 'url': x['url'], 'quote': x['text'][start:end], 'time': time})

    return res_list
for x in search_quote('phone'):
    print(x)

