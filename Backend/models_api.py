from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from fastapi import File


class UserBaseModel(BaseModel):
    id: int
    username: str
    avatar: str


class UserGetModel(UserBaseModel):
    background_img: Optional[str]
    text_color: Optional[str]
    rating: int


class TagBaseModel(BaseModel):
    id: int
    title: str
    text_color: str
    background_color: str


class MarkBaseModel(BaseModel):
    id: int
    title: str
    text_color: str
    background_color: str


class ArticleBaseModel(BaseModel):
    id: int
    title: str
    text_color: Optional[str]
    rating: int
    background_img: Optional[str]


class ArticleModel(BaseModel):
    id: int
    authors: List[UserBaseModel]
    title: str
    text: Optional[str]
    description: Optional[str]
    background_color: Optional[str]
    background_img: Optional[str]
    text_color: Optional[str]
    period_start: Optional[date]
    period_end: Optional[date]
    is_published: bool
    is_published: bool
    rating: float
    views: int
    date_added: datetime
    tags: List[TagBaseModel]
    marks: List[MarkBaseModel]
    is_read: bool
    is_author: bool


class ArticleFullModel(ArticleModel):
    text: Optional[str]


class UserModel(UserGetModel):
    is_active: bool
    is_admin: bool
    first_name: Optional[str]
    second_name: Optional[str]
    description: Optional[str]
    date_of_birth: Optional[date]
    date_added: datetime
    last_activity: datetime
    articles: List[ArticleModel]


class UserUpdateModel(BaseModel):
    username: str
    text_color: str
    background_color: Optional[str]
    description: Optional[str]
    date_of_birth: Optional[date]
    first_name: Optional[str]
    second_name: Optional[str]
    avatar: bytes = File(...)
    background_img: bytes = File(...)


class UserCreateModel(BaseModel):
    login: str
    username: str
    password: str
    email: EmailStr


class UserLoginModel(BaseModel):
    id: int
    username: str
    avatar: str
    access_token: str
    token_type: str


class ArticleEditModel(BaseModel):
    id: int
    title: str
    description: Optional[str]
    text: Optional[str]
    period_start: Optional[date]
    period_end: Optional[date]
    background_color: Optional[str]
    text_color: Optional[str]
    tags: Optional[List[int]]
    marks: Optional[List[int]]
    background_img: bytes = File(...)


class ArticleSearchModel(BaseModel):
    title: Optional[str]
    min_rating: Optional[float]
    max_rating: Optional[float]
    authors_add: Optional[List[int]]
    authors_del: Optional[List[int]]
    tags_add: Optional[List[int]]
    tags_del: Optional[List[int]]
    marks_add: Optional[List[int]]
    marks_del: Optional[List[int]]


class TagCreateModel(BaseModel):
    title: str
    description: str
    category_id: int


class MarkCreateModel(BaseModel):
    title: str
    description: str
    category_id: int


class CommentModel(BaseModel):
    id: int
    answer_id: int
    text: str
    date_added: datetime
    edited: bool
    author: UserBaseModel
    likes: int
    article_id: int
    is_liked: bool
    is_author: bool


class CompilationModel(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_public: bool
    articles: List[ArticleModel]


class CompilationGetModel(BaseModel):
    id: int
    title: str
    is_saved: bool


class CompilationCreateModel(BaseModel):
    title: str
    description: Optional[str]
    is_public: bool = True


class CategoryCreateModel(BaseModel):
    title: str
    description: str
    text_color: str
    background_color: str


class CategoryBaseModel(BaseModel):
    id: int
    title: str
    description: str
    text_color: str
    background_color: str


class CategoryModel(CategoryBaseModel):
    tags: List[TagBaseModel]
    marks: List[MarkBaseModel]


class TagModel(BaseModel):
    id: int
    title: str
    description: str
    category: CategoryBaseModel


class MarkModel(BaseModel):
    id: int
    title: str
    description: str
    category: CategoryBaseModel


class CommentBaseModel(BaseModel):
    answer_id: int
    text: str
    date_added: datetime
    deleted: bool = False
    edited: bool = False
    user_id: int
    likes: List[UserGetModel]
    article_id: int


class CommentCreateModel(BaseModel):
    origin_id: int
    answer_id: int
    text: str
    type: str
