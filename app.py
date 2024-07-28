from flask import Flask, request, jsonify, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

def baixar_video(url):
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def baixar_todos_videos(url_canal):
    ydl_opts = {
        'extract_flat': 'in_playlist',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url_canal, download=False)
        urls_videos = [entrada['url'] for entrada in info['entries']]
        for url_video in urls_videos:
            baixar_video(url_video)

@app.route('/baixar', methods=['POST'])
def baixar():
    dados = request.get_json()
    url = dados['url']
    if 'channel' in url:
        baixar_todos_videos(url)
    else:
        baixar_video(url)
    return jsonify({"message": "Download iniciado"}), 200

@app.route('/')
def index():
    return send_from_directory('estatico', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
