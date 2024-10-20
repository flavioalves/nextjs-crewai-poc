from pydantic import BaseModel
from typing import List

class NamedURL(BaseModel):
    name: str
    url: str

class PositionInfo(BaseModel):
    company: str
    position: str
    name: str
    blog_articles_urls: List[str]
    youtube_interviews_urls: List[NamedURL]
    
    
class PositionInfoList(BaseModel):
    positions: List[PositionInfo]    