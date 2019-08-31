import os
from flask import Flask, render_template, flash, url_for, redirect, session
from forms import InstagramVideoURLDecoder
import re
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

APP_PATH = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(APP_PATH, 'templates/')

app = Flask(__name__, template_folder=TEMPLATE_PATH)
app.config['SECRET_KEY']= '900200bfec2408a479affff3e76e3208'

def get_source_html(url):
	headers = {"User-Agent": 'Chrome'}
	resp = requests.get(url, headers=headers)
	http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
	html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
	encoding = html_encoding or http_encoding
	webpage = BeautifulSoup(resp.content, 'lxml', from_encoding=encoding)
	return webpage

def find_video_tags(post_url):
	source_html = get_source_html(post_url)
	video_regex = r"\"video_url\":\"(https:\/\/[^\",\"]+)"
	videos = re.findall(video_regex, str(source_html))
	video_list = list()
	for video_url in videos:
		url = video_url.replace("\\u0026","&")
		video_list.append(url)
	return video_list


@app.route("/", methods=['GET', 'POST'])
def home():
	form = InstagramVideoURLDecoder()
	if form.validate_on_submit():
		session["video_list"] = find_video_tags(form.videoURL.data)
		session["url"] = form.videoURL.data
		form.reset()
		return redirect(url_for('video'))
	return render_template("index.html", form = form)

@app.route("/video", methods=['GET'])
def video():
	return render_template('video.html')

if __name__ == '__main__':
	app.run(Debug=True)
