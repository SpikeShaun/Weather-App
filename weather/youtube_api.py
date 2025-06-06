# -*- coding=utf-8 -*-
# @Time:7/4/2025 上午 11:28
# @Author:席灏铖
# @File:youtube_api.PY
# @Software:PyCharm


import requests

YOUTUBE_API_KEY = "AIzaSyCapth_Nbst9AyDUX8GI1fXwnnBr7xxRmA"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def search_youtube_videos(location_query, max_results=3):

    params = {
        "part": "snippet",
        "q": location_query,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY,
        "safeSearch": "strict"
    }

    try:
        response = requests.get(YOUTUBE_SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()
        videos = []

        for item in data.get("items", []):
            video = {
                "title": item["snippet"]["title"],
                "video_id": item["id"]["videoId"],
                "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
            }
            videos.append(video)

        return videos
    except requests.exceptions.RequestException as e:
        print(f"[YouTube API Error] {e}")
        return []
