#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#使用微软REST API 进行语音识别
# HTTP请求:
#       POST speech/recognition/conversation/cognitiveservices/v1?language=en-US&format=detailed HTTP/1.1
#       Accept: application/json;text/xml
#       Content-Type: audio/wav; codec="audio/pcm"; samplerate=16000
#       Ocp-Apim-Subscription-Key: YOUR_SUBSCRIPTION_KEY
#       Host: westus.stt.speech.microsoft.com
#       Transfer-Encoding: chunked
#       Expect: 100-continue

import requests
import configparser
import json
import io
import os
from scipy.signal import resample
import scipy.io.wavfile as wav

cf = configparser.ConfigParser()
cf.read('configAPI.ini')
key = cf.get('api','key')
url = cf.get('api','url')

def read_in_chunks(file_object, chunk_size = 1024):
        while True:
                data = file_object.read(chunk_size)
                if not data:
                        break
                yield data

def speech_result(file_name):
        print("wav start ------------------------------")
        (rate,sig) = wav.read(file_name)
        wavout = io.BytesIO()
        wav.write(wavout,rate,sig)
        print("wva end --------------------------------")
		
        headers = {'Ocp-Apim-Subscription-Key': key,
               'Content-type': 'audio/wav; codec=audio/pcm; samplerate=16000'}
        query_params = {'language': 'en-US'}

        response = requests.post(url, params=query_params,headers=headers,data=wavout)
        #print text
        response = json.loads(response.text)
        if response['RecognitionStatus'] == 'Success':
                recognized_text = response['DisplayText']
                print(recognized_text)
                return recognized_text
        else:
                print('Did not understand command')
                exit()


if __name__ == '__main__':
        speech_result("output.wav");

