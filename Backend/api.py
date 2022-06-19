from datetime import timedelta

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from pydantic import EmailStr

import crud
from crud import get_db, get_current_user, get_current_user_base
from models_api import *

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/user", response_model=UserBaseModel)
async def get_user(db_user=Depends(get_current_user)):
    return crud.convert_to_base_user(db_user)


@app.get("/users/best", response_model=List[UserGetModel])
async def get_best_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_best_users(db=db, skip=skip, limit=limit)


@app.get("/user/{user_id}", response_model=UserModel)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db=db, user_id=user_id)


@app.get("/user/{email}/email", response_model=int)
async def check_user_email(email: EmailStr, db: Session = Depends(get_db)):
    return crud.check_user_email(db=db, email=email)


@app.get("/users/{username}/search", response_model=List[UserBaseModel])
async def get_user_by_username(username: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users_by_username(db=db, username=username, skip=skip, limit=limit)


@app.patch('/user/edit', response_model=UserModel)
async def update_user(user: UserUpdateModel, db_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=db_user.id, user=user)


@app.patch('/user/delete', response_model=int)
async def delete_user(db_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=db_user.id)


@app.post("/user", response_model=int)
async def create_user(user: UserCreateModel, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.post("/user/login", response_model=UserLoginModel)
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    return crud.login(db=db, email=form_data.username, password=form_data.password)


@app.post('/user/logout', response_model=int)
async def logout(db_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.logout(db=db, user_id=db_user.id)


@app.get("/articles/last", response_model=List[ArticleModel])
async def get_last_articles(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_user = get_current_user_base(token=request.headers.get("Authorization"), db=db)
    return crud.get_last_articles(db_user=db_user, db=db, skip=skip, limit=limit)


@app.get("/articles/popular", response_model=List[ArticleModel])
async def get_popular_articles(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_user = get_current_user_base(token=request.headers.get("Authorization"), db=db)
    return crud.get_popular_articles(db_user=db_user, db=db, skip=skip, limit=limit)


@app.get("/articles/read", response_model=List[ArticleModel])
async def get_read_articles_by_user(db_user=Depends(get_current_user), skip: int = 0, limit: int = 10,
                                    db: Session = Depends(get_db)):
    return crud.get_read_articles_by_user(db=db, db_user=db_user, skip=skip, limit=limit)


@app.get("/articles/view", response_model=List[ArticleModel])
async def get_view_articles_by_user(db_user=Depends(get_current_user), skip: int = 0, limit: int = 10,
                                    db: Session = Depends(get_db)):
    return crud.get_view_articles_by_user(db=db, db_user=db_user, skip=skip, limit=limit)


@app.get("/article/{article_id}", response_model=ArticleModel)
async def get_article(request: Request, article_id: int, db: Session = Depends(get_db)):
    db_user = get_current_user_base(token=request.headers.get("Authorization"), db=db)
    return crud.get_article_by_id(db=db, article_id=article_id, db_user=db_user)


@app.get('/articles/{tag_id}/tag', response_model=List[ArticleModel])
async def get_articles_by_tag(request: Request, tag_id: int, skip: int = 0, limit: int = 10,
                              db: Session = Depends(get_db)):
    db_user = get_current_user_base(token=request.headers.get("Authorization"), db=db)
    return crud.get_articles_by_tag(db=db, tag_id=tag_id, db_user=db_user, skip=skip, limit=limit)


@app.get('/articles/{mark_id}/mark', response_model=List[ArticleModel])
async def get_articles_by_mark(request: Request, mark_id: int, skip: int = 0, limit: int = 10,
                               db: Session = Depends(get_db)):
    db_user = get_current_user_base(token=request.headers.get("Authorization"), db=db)
    return crud.get_articles_by_mark(db=db, mark_id=mark_id, db_user=db_user, skip=skip, limit=limit)


@app.get("/articles/{title}/search", response_model=List[ArticleBaseModel])
async def get_articles_by_title(title: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_articles_by_title(db=db, title=title, skip=skip, limit=limit)


@app.get("/articles/{user_id}/author", response_model=List[ArticleModel])
async def get_articles_by_user(user_id: int, skip: int = 0, limit: int = 10,
                               db: Session = Depends(get_db)):
    return crud.get_articles_by_user(db=db, user_id=user_id, skip=skip, limit=limit)


@app.patch('/article/edit', response_model=ArticleModel)
async def update_article(article: ArticleEditModel, db_user=Depends(get_current_user),
                         db: Session = Depends(get_db)):
    return crud.update_article(db, db_user=db_user, article=article)


@app.patch('/article/{article_id}/publish', response_model=ArticleModel)
async def is_published(article_id: int, db_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.publish_article(db=db, db_user=db_user, article_id=article_id)


@app.patch('/article/{article_id}/delete', response_model=int)
async def delete_article(article_id: int, db_user=Depends(get_current_user), db: Session = Depends(get_db)):
    crud.delete_article(db=db, db_user=db_user, article_id=article_id)


@app.patch("/article/{article_id}/read", response_model=ArticleModel)
async def read_article(article_id: int, db_user=Depends(get_current_user),
                       db: Session = Depends(get_db)):
    return crud.read_article(db=db, db_user=db_user, article_id=article_id)


@app.patch("/article/{article_id}/view", response_model=int)
async def create_view_of_article(article_id: int, db_user=Depends(get_current_user),
                                 db: Session = Depends(get_db)):
    return crud.create_view_of_article(db=db, user_id=db_user.id, article_id=article_id)


@app.patch("/article/{article_id}/authorship/{user_id}/role/{role}", response_model=int)
async def add_author(user_id: int, article_id: int, role: str, db_user=Depends(get_current_user),
                     db: Session = Depends(get_db)):
    return crud.add_author(db=db, user_id=user_id, db_user=db_user, article_id=article_id, role=role)


@app.patch("/article/{article_id}/rating/{rating}", response_model=int)
async def update_rating_of_article(article_id: int, rating: int, db_user=Depends(get_current_user),
                                   db: Session = Depends(get_db)):
    return crud.create_rating_article(db=db, user_id=db_user.id, article_id=article_id, rating=rating)


@app.post("/articles/search", response_model=List[ArticleModel])
async def search_articles(search: ArticleSearchModel, db: Session = Depends(get_db)):
    return crud.search_articles(db=db, search=search)


@app.post("/article/{title}", response_model=int)
async def create_article(title: str, db_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_article(db=db, db_user=db_user, title=title)


@app.get('/category/{category_id}', response_model=CategoryModel)
async def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    return crud.get_category_by_id(db=db, category_id=category_id)


@app.post("/category")
async def create_category(category: CategoryCreateModel, db_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category)


@app.get('/tags/popular', response_model=List[TagBaseModel])
async def get_popular_tags(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_popular_tags(db=db, skip=skip, limit=limit)


@app.get('/tag/{tag_id}', response_model=TagModel)
async def get_tag_by_id(tag_id: int, db: Session = Depends(get_db)):
    return crud.get_tag_by_id(db=db, tag_id=tag_id)


@app.get('/tags/{title}/search', response_model=List[TagBaseModel])
async def get_tags_by_title(title: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_tags_by_title(db=db, title=title, skip=skip, limit=limit)


@app.post("/tag")
async def create_tag(tag: TagCreateModel, db_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_tag(db=db, tag=tag)


@app.get('/marks/popular', response_model=List[TagBaseModel])
async def get_popular_marks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_popular_marks(db=db, skip=skip, limit=limit)


@app.get('/mark/{mark_id}', response_model=MarkModel)
async def get_mark_by_id(mark_id: int, db: Session = Depends(get_db)):
    return crud.get_mark_by_id(db=db, mark_id=mark_id)


@app.get('/marks/{title}/search', response_model=List[MarkBaseModel])
async def get_marks_by_title(title: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_marks_by_title(db=db, title=title, skip=skip, limit=limit)


@app.post("/mark")
async def create_mark(mark: MarkCreateModel, db_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_mark(db=db, mark=mark)


@app.get("/comments/like", response_model=List[CommentModel])
async def get_favorite_comments_by_user(db_user=Depends(get_current_user), skip: int = 0, limit: int = 10,
                                        db: Session = Depends(get_db)):
    return crud.get_favorite_comments_by_user(db=db, db_user=db_user, skip=skip, limit=limit)


@app.get("/comments/user", response_model=List[CommentModel])
async def get_comments_by_user(db_user=Depends(get_current_user), skip: int = 0, limit: int = 10,
                               db: Session = Depends(get_db)):
    return crud.get_comments_by_user(db=db, db_user=db_user, skip=skip, limit=limit)


@app.get("/comments/{article_id}/article", response_model=List[CommentModel])
async def get_comments_by_article_id(request: Request, article_id: int, skip: int = 0, limit: int = 10,
                                     db: Session = Depends(get_db)):
    db_user = get_current_user_base(token=request.headers.get("Authorization"), db=db)
    return crud.get_comments_by_article_id(db=db, article_id=article_id, db_user=db_user, skip=skip, limit=limit)


@app.patch("/comment/{comment_id}/like/{type}", response_model=CommentModel)
async def like_comment(comment_id: int, mark: int, db_user=Depends(get_current_user),
                       db: Session = Depends(get_db)):
    return crud.like_comment(db=db, db_user=db_user, comment_id=comment_id, mark=mark)


@app.patch('/comment/{comment_id}/text/{text}', response_model=CommentModel)
async def update_comment_text(comment_id: int, text: str, db_user=Depends(get_current_user),
                              db: Session = Depends(get_db)):
    return crud.update_comment_text(db=db, comment_id=comment_id, text=text)


@app.post("/comment", response_model=CommentModel)
async def create_comment(comment: CommentCreateModel, db_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_comment(db=db, db_user=db_user, comment=comment)


@app.get("/compilations/user", response_model=List[CompilationModel])
async def get_compilations_by_user(db_user=Depends(get_current_user), skip: int = 0, limit: int = 10,
                                   db: Session = Depends(get_db)):
    return crud.get_compilations_by_user(db=db, db_user=db_user, skip=skip, limit=limit)


@app.get('/compilations/article/{article_id}', response_model=List[CompilationGetModel])
async def article_is_in_compilation(article_id: int, db_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.article_is_in_compilation(db=db, user_id=db_user.id, article_id=article_id)


@app.patch('/compilation/{compilation_id}/article/{article_id}', response_model=List[CompilationGetModel])
async def save_article_in_compilation(compilation_id: int, article_id: int, db_user=Depends(get_current_user),
                                      db: Session = Depends(get_db)):
    return crud.save_article_in_compilation(db=db, compilation_id=compilation_id, user_id=db_user.id,
                                            article_id=article_id)


@app.post("/compilation", response_model=int)
async def create_compilation(compilation: CompilationCreateModel, db_user=Depends(get_current_user),
                             db: Session = Depends(get_db)):
    return crud.create_compilation(db=db, user_id=db_user.id, compilation=compilation)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
