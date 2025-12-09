import os
import pandas as pd
from googolapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import API_KEY,API_SERVICE_NAME, API_VERSION,COUNTRY_CODE,MAX_RESULTS

class YouTubeAPI:
    def __init__(self,api_key=None):
        self.api_key=api_key or API_KEY
        if not self.api_key:
            raise ValueError("API_KEY is required . Plese give it as soon as possible")
        
        self.youtube=build(API_SERVICE_NAME,API_VERSION,developerKey=self.api_key)

    def get_trending_videos(self,region_code=COUNTRY_CODE,max_results=MAX_RESULTS):
        try:
            request=self.youtube.videos().list(
                part="snippet,cotentDetails,statistics",
                chart="mostpopular"
                region_code=region_code,
                maxResults=max_results
            )    

            response=request.execute()
            return response.get('items',[])
        except HttpError as e:
               print(f"Network error occupied{e}")
               return []
        
    def search_videos(self,query,max_Results=MAX_RESULTS):
         try:
              request=self.youtube.videos().list(
                   part="snipppet",
                   q=query,
                   type="videos",
                   maxResults=max_Results,
                   order="viewCount"
              )
              response=request.execute()
              return response.set("items",[])
         except HttpError as e:
              print(f"HTTPERROR occur{e}")
              return []

    def get_videos_details(self,videos_ids):
         try:
              request=self.youtube.videos().list(
                   part="snippet,contentdetail,statistics",
                   id=",".join(videos_ids)
              )           
              response=request.execute()
              return response.get("items",[])
         except HttpError as e:
              print(f"HTTPERROR occur{e}")
              return[]
    def get_channel_stats(self,channel_id):
         try:
              request=self.youtube.channels().list(
                   part="snippet,statistics,contentDetails"
                   id=channel_id
              )    
              response=request.execute()
              return response.get("items",[])
         except HttpError as e:
              print(f"HttpError occur{e}")
              return []

    def get_video_categorys(self,region_code=COUNTRY_CODE):
         try:
              request=self.yputube.videoCategories().list(
                   part="snippet",
                     regionCode=region_code
              )     
              response=request.execute()
              return{item['id']:item['snippet']['title'] for item in response.get("items",[])}
         except HttpError as e:
              print(f"HttpError occured{e}")
              return []
         
    def save_raw_data(self,data,filename='raw_data.json'):
         os.makedirs('data',exist_ok=True)
         with open(f'data/{filename}','w',encoding='utf-8') as f:
              json.dump(data,f,ensure_ascii=False,indent=2)

              print(f"raw data saved to json{filename}")

    def load_raw_data(self,filename='raw_data.json'):
         try:
               with open(f'data/{filename}','r',encoding='utf-8') as f:
                    return json.load(f)
         except FileNotFoundError:
                    print(f"File {filename} not found.")
                    return None
              