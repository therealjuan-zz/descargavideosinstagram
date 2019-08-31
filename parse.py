import re
import requests
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

data = 'https://google.com/#resource'
data2 = 'https://www.instagram.com/p/B1rwA69H6ii/?utm_source=ig_web_button_share_sheet'
data2 = 'https://www.instagram.com/p/B1v_kF8h1z_/?utm_source=ig_web_copy_link'
data2 = 'https://www.instagram.com/p/B1v0FxDInwn/'
data2 = 'https://www.instagram.com/p/B1v_kF8h1z_/?utm_source=ig_web_copy_link'

def validate_url(data):
	url_regex = r'''(^(http|https):\/\/www\.instagram\.com\/p\/.*)'''
	regex = re.compile(url_regex)
	return regex.match(data)

def get_source_html(url):
	headers = {"User-Agent": 'Chrome'}
	resp = requests.get(url, headers=headers)
	http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
	html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
	encoding = html_encoding or http_encoding
	webpage = BeautifulSoup(resp.content, 'lxml', from_encoding=encoding)
	return webpage

def find_video_tags(post_url):
	valid_url = validate_url(post_url)
	if valid_url:
		source_html = get_source_html(valid_url.group())
		video_regex = r"\"video_url\":\"(https:\/\/[^\",\"]+)"
		videos = re.findall(video_regex, str(source_html))
		video_list = list()
		for video_url in videos:
			url = video_url.replace("\\u0026","&")
			video_list.append(url)
		return video_list


video_list = find_video_tags(data2)

print(video_list)