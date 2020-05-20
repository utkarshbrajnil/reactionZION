from apiclient.discovery import build
from rfc3339 import rfc3339
import pandas as pd



DEVELOPER_KEY = "api"

YOUTUBE_API_SERVICE_NAME = "youtube"

YOUTUBE_API_VERSION = "v3"


youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,  developerKey = DEVELOPER_KEY)
def search_vidid(startdate,enddate,query):


    publishedBefore = enddate
    publishedAfter = startdate

    publishedBefore = rfc3339(publishedBefore)
    publishedAfter = rfc3339(publishedAfter)

    query = query + " english news"
    req=youtube.search().list(q=query,part='snippet',type='video',publishedAfter = publishedAfter,publishedBefore = publishedBefore,maxResults=10)
    res = req.execute()
    videoid_list=[]
    for item in res['items']:
        videoid_list.append(item['id']['videoId'])
    return videoid_list

def ct_yt(vid):
    com=[]
    request = youtube.commentThreads().list(
       part="snippet",
       maxResults=100,
       order="relevance",
       textFormat="plainText",
       videoId=vid
   )
    resp = request.execute()
    for x in resp['items']:
        A=[x['snippet']['topLevelComment']['snippet']['publishedAt'],x['snippet']['topLevelComment']['snippet']['textDisplay']]
        com.append(A)
    df=pd.DataFrame(com,columns = ['unix','comments'])
    return df

def allvidcom(videoid_list):
    maindf = pd.DataFrame(columns = ['unix','comments'])
    for i in videoid_list:
        try:
            df2 = ct_yt(i)
            maindf = maindf.append(df2, ignore_index = True)
            maindf.sort_values(by=['unix'], inplace=True, ascending=False)
        except:
            continue
    return maindf
