import os
from typing import Iterable
from pydantic import BaseModel
from googleapiclient.discovery import build


class Comment(BaseModel):
    authorDisplayName: str
    textDisplay: str
    likeCount: int


class YoutubeClient:

    def __init__(self):
        API_KEY = os.getenv("YOUTUBE_API_KEY", "AIzaSyAcQbllikpGm-4bNnXYUBY7PNTW9ZfapeQ")
        self.youtube = build("youtube", "v3", developerKey=API_KEY)

    def get_comments(self, video_id: str) -> Iterable[Comment]:
        next_page_token = None

        while True:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
                textFormat="plainText"
            )

            response = request.execute()
            for item in response["items"]:
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                yield Comment.model_validate(snippet)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break


if __name__ == "__main__":
    client = YoutubeClient()
    for i in client.get_comments("zZis75sAdPg"):
        print(i)
