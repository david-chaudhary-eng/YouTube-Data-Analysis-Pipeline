import pandas as pd
import numpy as np
from datetime import datetime
from config import *
import sys
import argparse
import os

from youtube_api import YouTubeAPI
from yt_dataProcess import DataProcessor
from yt_analyzer import DataAnalyzer

def parse_arguments():
    """Parse command line arguments"""
    parser=argparse.ArgumentParser(description='Yutube data analysis pipeline')
    parser.add_argument('--region',type=str,default=COUNTRY_CODE,
                        help='Region code for trending ideos')

    parser.add_agument('--max-results',type=int,default=MAX_RESULTS,
                       help='Maximum number of videos to fetch')

    parser.add_arguments('--use-cached',action='store-true',
                         help='use cached data instead of fetching the data from API')
    parser.add_argumments('--export',action='store-true',help='Export results to files')
    return parser.parse_args()

def main():

    args=parse_arguments()

    # Initialize components

    youtube_api=YouTubeAPI()
    processor=DataProcessor()

    if args.use-cached:
        print("Loading cached data ")
        raw_data=youtube_api.load_raw_data()

        if raw_data is None:
            print(f"No cached data found . Fetching from API  ")
            raw_data=youtube_api.get_trending_videos(args.region,args.max_results)
        else:

            print(f"fetching the trending ideos from api {args.region}")
            raw_data=youtube_api.get_trending_videos(args.region,args.max_result)

            if not raw_data:
                print(f"No data retrieved ....") 
                return 
            print(f"retrieved {len(raw_data)}")

    if args.export:
        youtube_api.save_raw_data(raw_data)

     # Get video categories 
     
        print(f"Video categories")
        categories=youtube_api.get_video_categorys(args.region)

        print(f"retrieved {len(categories)}")


        # Process data
        print(f"Processing data")
        df=processor.process_video_data(raw_data,categories)

        if df.empty:
            print(f"No data processed")
            return 
        print(f"Processed {len(df)} videos")
        print(df[['title','channel-titles','view_count','like_count']].head())

        # Clean text data

        df=processor.clean_text_data(df)

        # save processed data
        if args.export:
            processedData=processor.save_processed_data(df)
            print(f"Data saved to {PROCESSED_DATA_PATH}")
            return processedData
        # Analyze data

        print(f"Analyze data")
        analyzer=DataAnalyzer(df)
        analysis_result=analyzer.run_full_analysis()
        engagement=analysis_result['engagement_analysis']

        if args.export:
            print(f"Processed data {PROCESSED_DATA_PATH}")
            print(f"Analysis results {ANALYSIS_RESULTS_PATH}")


if __name__="__main__"
main()


