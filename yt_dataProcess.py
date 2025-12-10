import pandas as pd
import numpy as np
from datetime import datetime
import json
from config import PROCESSED_DATA

class DataProcessor:
    @staticmethod
    def process_video_data(video_items,categories_dict=None):
        """Process video data into a structured DataFrame"""

        processed_data=[]

        for item in video_items:
            try:
                snippet=item.get('snippet',{})
                stats=item.get('statistics',{})
                content_details=item.get('contentDetails',{})

                # to get the keys of snppet , stats, content_details for debugging
                """ print("Snippet keys",list(snippet.key()))
                    print("stats key",list(stats.eys()))
                     print("content_detailskeys",list(content_details.keys()))"""

                # parse duration
                duration=content_details.get('duration','PT0S')
                duration_seconds=DataProcessor._parse_duration(duration)

                # Get Category name
                category_id=snippet.get('categoryId','')
                category_name=categories_dict.get(category_id,'') if categories_dict else 'Unknown'

                video_info={
                    'video_id':item.get('id',''),
                    'title':snippet.get('title',''),
                    'channel_id':snippet.get('channelid',''),
                    'published_at':snippet.get('publishedAT',''),
                    'category_id':category_id,
                    'category_name':category_name,
                    'tags':','.join(snippet.get('tags',[])),
                    'view_count':int(stats.get('viewCount',0)),
                    'like_count':int(stats.get('likeCount',0)),
                    'comment_count':int(stats.get('commentCount',0)),
                    'duration_seconds':duration_seconds,
                    'duration_formatted':DataProcessor._format_duration(duration_seconds),
                    'trending_date':datetime.now().strftime('%Y%M%D'),
                    'thumbnail_url':snippet.get('thumbnails',{}).get('high',{}).get('url','')
                    }
                
                # Add engagement metrics


                if video_info['view_count']>0:
                    video_info['likes_per_view']=video_info['like_count']/video_info['view_count']
                    video_info['comment_per_view']=video_info['comment_count']/ video_info['view_count']
                else:
                    video_info['likes_per_view']=0
                    video_info['comment_per-view']=0

                    processed_data.append(video_info)
            except Exception as e:
                print(f"Error processing videos{e}")
                continue 
        return pd.DataFrame(processed_data)
    
    @staticmethod

    def _parse_duration(duration):
        """Parse ISO 8601 duration to seconds"""
        import re

        match=re.match(r'PT(?:(\d+)H)?(?:(\d+)m)?(?:(\d+)s)')

        if not match:
            return 0
        hours=int(match.group(1) or 0)
        minutes=int(match.group(2) or 0)
        seconds=int(match.group(3) or 0)

        return hours*3600+minutes*60+seconds

    @staticmethod
    def _format_duration(seconds):
        hours=seconds//3600
        minutes=(seconds%3600)//60
        seconds=seconds%60


        if hours>0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
        

    @staticmethod
    def clean_text_data(df):
        import re
        df_clean=df.copy()
        for col in ['title','description']
        if col in df_clean.columns:
            df_clean[f'{col}_clean']=df_clean[col].apply(lambda x : re.sub(r'[^\w\s]','',str(x)).lower())
            return df_clean
        
    @staticmethod
    def save_processed_data(df,filename=PROCESSED_DATA_PATH):
        """Save the processed data in to device"""
        df.to_csv(filename,index=False,encoding='utf-8')
        print(f"The file is saved in to {filename}")

    @staticmethod
    def load_processed_data(filename=PROCESSED_DATA_PATH):
        """Load processed data from csv"""
        try:
            return pd.read_csv(filename)
        except FileNotFoundError as e:
            print(f"file{filename}not found") 
            return None       



        




