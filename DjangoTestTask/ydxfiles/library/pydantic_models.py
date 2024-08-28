from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field
import json

class Item(BaseModel):
    name: str
    file: Optional[str] = Field(None, alias='file')

class Embedded(BaseModel):
    items: List[Item]

class Owner(BaseModel):
    login: str
    display_name: str
    uid: str

class CommentIds(BaseModel):
    private_resource: str
    public_resource: str

class JsonResponse(BaseModel):
    public_key: str
    public_url: HttpUrl
    embedded: Embedded = Field(..., alias='_embedded')
    name: str
    exif: Optional[dict]
    resource_id: str
    revision: int
    created: str
    modified: str
    owner: Owner
    path: str
    comment_ids: CommentIds
    type: str
    views_count: int

