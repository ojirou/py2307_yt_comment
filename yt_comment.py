import requests
import json
import subprocess
from googleapiclient.discovery import build
import pandas as pd
# API情報
API_KEY = ''
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(
YOUTUBE_API_SERVICE_NAME, 
YOUTUBE_API_VERSION,
developerKey=API_KEY
)
URL = 'https://www.googleapis.com/youtube/v3/'
# ここにAPI KEYを入力
# API_KEY = 'API KEYを入力'
# ここにVideo IDを入力
VIDEO_ID = ''
def print_video_comment(no, video_id, next_page_token):
  params = {
    'key': API_KEY,
    'part': 'snippet',
    'videoId': video_id,
    'order': 'relevance',
    'textFormat': 'plaintext',
    'maxResults': 100,
  }
  if next_page_token is not None:
    params['pageToken'] = next_page_token
  response = requests.get(URL + 'commentThreads', params=params)
  resource = response.json()
  for comment_info in resource['items']:
    # コメント
    text = comment_info['snippet']['topLevelComment']['snippet']['textDisplay']
    # グッド数
    like_cnt = comment_info['snippet']['topLevelComment']['snippet']['likeCount']
    # 返信数
    reply_cnt = comment_info['snippet']['totalReplyCount']
    # ユーザー名
    user_name = comment_info['snippet']['topLevelComment']['snippet']['authorDisplayName']
    # Id
    parentId = comment_info['snippet']['topLevelComment']['id']
#     print('{:0=4}\t{}\t{}\t{}\t{}'.format(no, text.replace('\r', '\n').replace('\n', ' '), like_cnt, user_name, reply_cnt))
    if reply_cnt > 0:
      cno = 1
      print_video_reply(no, cno, video_id, None, parentId)
    no = no + 1
  if 'nextPageToken' in resource:
    print_video_comment(no, video_id, resource["nextPageToken"])
def print_video_reply(no, cno, video_id, next_page_token, id):
  params = {
    'key': API_KEY,
    'part': 'snippet',
    'videoId': video_id,
    'textFormat': 'plaintext',
    'maxResults': 50,
    'parentId': id,
  }
  if next_page_token is not None:
    params['pageToken'] = next_page_token
  response = requests.get(URL + 'comments', params=params)
  resource = response.json()
  for comment_info in resource['items']:
    # コメント
    text = comment_info['snippet']['textDisplay']
    # グッド数
    like_cnt = comment_info['snippet']['likeCount']
    # ユーザー名
    user_name = comment_info['snippet']['authorDisplayName']
#     print('{:0=4}-{:0=3}\t{}\t{}\t{}'.format(no, cno, text.replace('\r', '\n').replace('\n', ' '), like_cnt, user_name))
    data.append(['{:0=4}-{:0=3}'.format(no, cno), user_name, text.replace('\r', '\n').replace('\n', ' '),like_cnt])
    cno = cno + 1
  if 'nextPageToken' in resource:
    print_video_reply(no, cno, video_id, resource["nextPageToken"], id)
# コメントを全取得する
video_id = VIDEO_ID
no = 1
data=[]
print_video_comment(no, video_id, None)
df=pd.DataFrame(data)
df.columns=['no.','name','comment','likeCount']
df.to_csv("channel_comment.csv", encoding='utf-8-sig', index=None)
subprocess.Popen(["start", "", r"C:\Users\user\python\YoutubeTwitter\channel_comment.csv"], shell=True)