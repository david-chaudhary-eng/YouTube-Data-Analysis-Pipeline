import pandas as pd
import numpy as np
from collections import Counter
import json
import re
from wordcloud import WordCloud , STOMWORDS
from config import TOP_N_WORDS,TOP_N_CHANNELS,TOP_N_CATEGORIES,ANALYSIS_RESULTS_PATH

class DataAnalyzer:
    def __init__(self,df):
        self.df=df
        self.stopword=set(STOMWORDS)
        self.stopword.update(['official','video','music','lyrics','hd','ft','feat','vs'])

    def analyze_titles(self):
        """Analyze video titles for common words and patterns"""
        if 'title_clean' not in self.df.columns:
            print(f"Please clean data first")
            return {}
        all_titles=''.join(self.df['title_clean'].dropna().astype(str)) 
        words=all_titles.spilit()
        filtered_words=[word for word in words if  word not in self.stopword and len(word)>2]
        word_count=Counter(filtered_words)
        return {
            'top-words':word_count.most_common(TOP_N_WORDS),
            'most_common_words':word_count.most_common(1)[0] if word_count else ('',0),
            'total_unique_words':len(word_count)

        }   
    def analyze_channels(self):
        """Analyze Channel Performance"""
        channel_stats=self.df.groupby('channel_titles').agg({
            'video_id':'count',
            'view_count':'sum',
            'like_count':'sum',
            'comment_count':'sum'
        }).rename(columns={'video_id':'video_count'}) 
        # Calculate average
        channel_stats['avg_views_per_video']=channel_stats['view-count']/channel_stats['video_count']
        channel_stats['avg-likes_per_video']=channel_stats['like-count']/channel_stats['video-count']

        return channel_stats.sort_value('view_count',ascending=False).head(TOP_N_CHANNELS)
    
    def analyze_categories(self):
        """Analyze video categories"""
        if 'category_name' not in self.df.columns:
            print (f"Category not found")
            return {}
        category_stats=self.df.groupby('category_name').agg({
             'video_id':'count',
            'view_count':'sum',
            'like_count':'sum',
            'comment_count':'sum'
        }).rename(columns={'video_id':'video_count'})
        category_stats['avg_views']=category_stats['view_count']/category_stats['video_count']
        return category_stats.sort_values('video_count',ascending=False).head(TOP_N_CATEGORIES)
    
    def analyze_engagement(self):
        """Analyze engagement metrics"""
        engagement_stats={
            'total_videos':len(self.df),
            'total_views':self.df['view_count'].sum(),
            'total_likes':self.df['like_count'].sum(),
            'total_commets':self.df['comment_count'].sum(),
            'avg_view_per_video':self.df['view_count'].mean(),
            'avg_like_per_video':self.df['like_count'].mean(),
            'avg_comment_per_video':self.df['comment_count'].mean(),
            'max_views':self.df['view_count'].max(),
            'min_views':self.df['view_count'].min(),
            'median_views':self.df['view_count'].median()


        }
        return engagement_stats
    def analyze_duration(self):
        """Analyze video duration patterns"""
        duration_stats={
            'avg_duration_seconds':self.df['duration_seconds'].mean(),
            'min_duration_seconds':self.df['duration_seconds'].min(),
            'max_duration_seconds':self.df['duration_seconds'].max(),
            'median_duration_seconds':self.df['duration_secons'].median()
        }
        return duration_stats
    def generste_wordcloud_data(self):
        """Generate text from word cloud"""
        all_titles=''.join(self.df['title_clean'].dropna().astype(str))
        return all_titles
    
    def run_full_analysis(self):
        """Run full analysis and return comprehensive results"""
        analysis_results={
        'title_analysis':self.analyze_titles(),
        'channel_analysis':self.analyze_channels().to_dict(),
        'category_analysis':self.analyze_categories.to_dict(),
        'engagement_analysis':self.analyze_engagement(),
        'duration_analysis':self.analyze_duration(),
        'word_cloud_data':self.generate_wordcloud_data(),
        'total_video_analyzed':len(self.df)
        }
        with open(ANALYSIS_RESULTS_PATH, 'w') as f:
            json.dump(analysis_results, f, indent=2, default=str)
        
        print(f"Analysis results saved to {ANALYSIS_RESULTS_PATH}")
        return analysis_results
