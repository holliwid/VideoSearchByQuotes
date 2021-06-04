
import os
from os import listdir
from os.path import isfile, join
import requests
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import isodate

import some_data

'https://stackoverflow.com/questions/15512239/python-get-all-youtube-video-urls-of-a-channel'
def get_all_video_in_channel(api_key, id_channel):

    base_video_url = 'https://www.youtube.com/watch?v='

    first_url = f'https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={id_channel}&part=snippet&part=id&order=date&maxResults=20'

    data_of_video = []
    url = first_url
    while True:
        inp = requests.get(url).text
        resp = json.loads(inp)
        print(resp)

        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                inp1 = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={i["id"]["videoId"]}&key={api_key}').text
                resp1 = json.loads(inp1)
                print(resp1,type(resp1))
                if isodate.parse_duration((resp1['items'][0]['contentDetails']['duration'])).total_seconds() < isodate.parse_duration(('PT15M')).total_seconds():
                    data_of_video.append((i['snippet']['title'], base_video_url + i['id']['videoId'], isodate.parse_duration((resp1['items'][0]['contentDetails']['duration'])).total_seconds()))

        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break


    def write_url_in_txt(path: str, data):
        f = open(path, 'w')
        for url in data:
            f.write(f'{url[0]}*|*{url[1]}*|*{url[2]}\n');
        f.close()

    write_url_in_txt('url_of_videos.txt', data_of_video)


#get_all_video_in_channel(some_data.youtube_api_key, some_data.id_channel)





def download_waw(path):
    data = open('url_of_videos.txt', 'r').read()
    data = [x.split('*|*') for x in data.split('\n')]
    print(data)

    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs',{
        'download.default_directory': r'/home/san/PycharmProjects/VideoSearch/source_of_video_wav'
    })
    driver = webdriver.Chrome(executable_path='/home/san/PycharmProjects/chromedriver', options=options)  # Optional argument, if not specified will search path.
    time.sleep(5)
    for k in range(30):
        url = data[k][1]
        print(url)
        if url not in open('existed_url_file.txt', 'r').read().split('\n'):
            try:
                driver.get('https://youtube-converter.online/')
                url_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/main/div/div/div[2]/form/input')))
                url_input.send_keys(url)
                button_download1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/main/div/div/div[2]/form/button')))
                button_download1.click()
                button_download2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div/section/div/div[5]/div/div/div[2]/div/a[4]')))
                button_download2.click()
                time.sleep(5)
                button_download3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/main/div/section/div/div[4]/div[2]/div[1]/a')))
                time.sleep(5)
                button_download3.click()
                time.sleep(5)


                def download_wait(path_to_downloads):
                    dl_wait = True
                    while dl_wait:
                        time.sleep(1)
                        dl_wait = False
                        for fname in os.listdir(path_to_downloads):
                            if fname.endswith('.crdownload'):
                                dl_wait = True
                                print('1')

                download_wait('source_of_video_wav')
                veryfied = open('existed_url_file.txt', 'a')
                veryfied.write(url+'\n')
            except:
                pass




download_waw('url_of_videos.txt')


def from_wav_to_text_IBM(apikey, path_to_source='source_of_video_wav', url='https://api.eu-gb.speech-to-text.watson.cloud.ibm.com'):
    authenticator = IAMAuthenticator(apikey)
    speech_to_text = SpeechToTextV1(authenticator=authenticator)

    speech_to_text.set_service_url(url)

    onlyfiles = [f for f in listdir(path_to_source) if isfile(join(path_to_source, f))]
    print(onlyfiles)
    for aud in onlyfiles:
        if not os.path.exists(f'prepared_text_of_video/{aud[:-3]}.txt') and aud not in open('black_list.txt', 'r').read().split('\n'):
            try:
                with open(f'source_of_video_wav/{aud}', 'rb') as audio_file:
                    response = speech_to_text.recognize(audio_file,content_type='audio/wav')
                    print(response.result)
                    result = ''
                    for x in range(len(response.result['results'])):
                        result += response.result['results'][x]['alternatives'][0]['transcript'] + ' '
                        print(result)
                    d = open(f'prepared_text_of_video/{aud[:-3]}.txt','w')
                    d.write(result)
            except:
                open('black_list.txt', 'a').write(f'{aud}\n')
    print('s')


#from_wav_to_text_IBM(some_data.IBM_PASSWORD)
