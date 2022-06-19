import base64
import random
from datetime import timedelta, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

from fastapi import Depends, HTTPException, status, File
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import insert, create_engine
from sqlalchemy.orm.session import sessionmaker, Session
from sqlalchemy.sql import func

from DB_tables import *
from models_api import *

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

engine = create_engine('sqlite:///scipher.db', echo=False, connect_args={'check_same_thread': False})

Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def send_code(email):
    msg = MIMEMultipart()
    check = random.randint(100000, 999999)  # подтверждение почты и создание пароля

    message = f'''<table style="width:100%;margin-top:46px;border-top:2px solid 
    #2086E0;background:#fff;box-shadow:0px 0px 2px #ddd;text-align:center;"> <tbody> <tr> <td 
    style="font-size:20px;font-weight:400;padding-top:120px;color:#303030;">Confirmation code</td> </tr> <tr> <td 
    style="font-size:36px;font-weight:800;color: #178BFE;">{check}</td> </tr> <tr> <td 
                    style="font-size:16px;font-weight:200;padding-top:30px;color: #303030;"> Чтобы подтвердить аккаунт введите этот код на сайтt: </td> </tr> <tr> <td style="font-size:16px;font-weight:400;color: 
                    #303030;padding-bottom:108px;border-bottom:1px solid #eee;"> <a href="/compose?To={email}">
{email}</a> 
                    </td>
                </tr>
                </tbody>
            </table>'''

    msg.attach(MIMEText(message, 'html'))
    msg["Subject"] = "[Scipher] Код подтверждения"
    server = SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login("socialpostchat@gmail.com", "8t%EzRUP")
    server.sendmail("socialpostchat@gmail.com", email, msg.as_string())
    server.quit()
    return check


def get_img(file_name: str):
    if file_name and file_name[-4::] == '.jpg':
        with open(file_name, "rb") as imageFile:
            file = base64.b64encode(imageFile.read())
            return file


def convert_to_base_user(db_user: Users):
    user = UserBaseModel(id=db_user.id,
                         username=db_user.username,
                         avatar=get_img(db_user.avatar))
    return user


def convert_to_get_user(db_user: Users):
    user = UserGetModel(id=db_user.id,
                        username=db_user.username,
                        text_color=db_user.text_color,
                        avatar=get_img(db_user.avatar),
                        background_img=get_img(db_user.background_img),
                        rating=db_user.rating)
    return user


def convert_to_compilation(db_user: Users):
    user = UserGetModel(id=db_user.id,
                        username=db_user.username,
                        text_color=db_user.text_color,
                        avatar=get_img(db_user.avatar),
                        background_img=get_img(db_user.background_img),
                        rating=db_user.rating)
    return user


def convert_to_base_tags(db_tags: List[Tags], db: Session):
    tags = []
    for db_tag in db_tags:
        db_category = get_categories(db).filter(Categories.id == db_tag.category_id).first()
        tag = TagBaseModel(id=db_tag.id,
                           title=db_tag.title,
                           text_color=db_category.text_color,
                           background_color=db_category.background_color)
        tags.append(tag)
    return tags


def convert_to_base_marks(db_marks: List[Marks], db: Session):
    marks = []
    for db_mark in db_marks:
        db_category = get_categories(db).filter(Categories.id == db_mark.category_id).first()
        mark = TagBaseModel(id=db_mark.id,
                            title=db_mark.title,
                            text_color=db_category.text_color,
                            background_color=db_category.background_color)
        marks.append(mark)
    return marks


def convert_to_base_category(db_category: Categories):
    category = CategoryBaseModel(id=db_category.id,
                                 title=db_category.title,
                                 description=db_category.description,
                                 text_color=db_category.text_color,
                                 background_color=db_category.background_color)
    return category


def convert_to_category(db_category: Categories):
    category = CategoryModel(id=db_category.id,
                             title=db_category.title,
                             description=db_category.description,
                             text_color=db_category.text_color,
                             background_color=db_category.background_color)
    return category


def convert_to_tag(db_tag: Tags, db: Session):
    db_category = get_categories(db).filter(Categories.id == db_tag.category_id).first()
    tag = TagModel(id=db_tag.id,
                   title=db_tag.title,
                   description=db_tag.description,
                   category=convert_to_base_category(db_category))
    return tag


def convert_to_mark(db_mark: Marks, db: Session):
    db_category = get_categories(db).filter(Categories.id == db_mark.category_id).first()
    mark = MarkModel(id=db_mark.id,
                     title=db_mark.title,
                     description=db_mark.description,
                     category=convert_to_base_category(db_category))
    return mark


def convert_to_articles(db_articles: List[Articles], db_user: Users, db: Session, comm: str):
    articles = []
    for db_article in db_articles:
        is_read = db_article in db_user.read if db_user else False
        is_author = db_article in db_user.articles if db_user else False
        tags = convert_to_base_tags(db_article.tags, db)
        marks = convert_to_base_marks(db_article.marks, db)
        db_authors = get_users(db).join(association_table_user_articles).filter(association_table_user_articles.c.article_id == db_article.id).all()
        authors = []
        for db_author in db_authors:
            author = convert_to_base_user(db_author)
            authors.append(author)
        article = ArticleModel(id=db_article.id,
                               authors=authors,
                               title=db_article.title,
                               description=db_article.description,
                               background_color=db_article.background_color,
                               background_img=get_img(db_article.background_img),
                               text_color=db_article.text_color,
                               period_start=db_article.period_start,
                               period_end=db_article.period_end,
                               is_published=db_article.is_published,
                               is_moderated=db_article.is_moderated,
                               rating=db_article.rating,
                               views=len(db_article.viewers),
                               date_added=db_article.date_added,
                               tags=tags,
                               marks=marks,
                               is_read=is_read,
                               is_author=is_author)
        articles.append(article)

    if comm == "obj":
        return articles[0]
    elif comm == "list":
        return articles


def convert_to_comments(db_comments: List[Comments], db_user: Users, comm: str):
    comments = []
    for db_comment in db_comments:
        user_ids = [user.id for user in db_comment.likes]
        is_liked = db_user.id in user_ids if db_user else False
        is_author = db_user.id == db_comment.user_id if db_user else False

        comment = CommentModel(id=db_comment.id,
                               answer_id=db_comment.answer_id,
                               text=db_comment.text,
                               date_added=db_comment.date_added,
                               edited=db_comment.is_edited,
                               user_id=db_comment.user_id,
                               likes=len(db_comment.likes),
                               article_id=db_comment.article_id,
                               author=convert_to_base_user(db_user=db_user),
                               is_liked=is_liked,
                               is_author=is_author)

        comments.append(comment)
    if comm == "obj":
        return comments[0]
    elif comm == "list":
        return comments


def get_tags(db: Session):
    return db.query(Tags).filter(Tags.is_deleted == 0)


def get_marks(db: Session):
    return db.query(Marks).filter(Marks.is_deleted == 0)


def get_categories(db: Session):
    return db.query(Categories).filter(Categories.is_deleted == 0)


def get_comps(db: Session):
    return db.query(Compilations).filter(Compilations.is_deleted == 0)


def get_comments(db: Session):
    return db.query(Comments).filter(Comments.is_deleted == 0)


def get_news(db: Session):
    return db.query(News).filter(News.is_deleted == 0)


def get_users(db: Session):
    return db.query(Users).filter(Users.is_deleted == 0)


def get_articles(db: Session):
    return db.query(Articles).filter(Articles.is_deleted == 0).filter(Articles.is_moderated == 1).filter(
        Articles.is_published == 1)


def get_all_articles(db: Session):
    return db.query(Articles).filter(Articles.is_deleted == 0)


def get_best_users(db: Session, skip: int, limit: int):
    db_users = get_users(db=db).order_by(-Users.rating).offset(skip).limit(limit).all()
    checked = []
    for db_user in db_users:
        if db_user:
            checked.append(convert_to_get_user(db_user))
    return checked


def get_user(db: Session, user_id):
    db_user = get_users(db=db).filter(Users.id == user_id).first()
    if db_user:
        user = UserModel(id=db_user.id,
                         rating=db_user.rating,
                         is_active=db_user.is_active,
                         is_admin=db_user.is_admin,
                         first_name=db_user.first_name,
                         second_name=db_user.second_name,
                         avatar=get_img(db_user.avatar),
                         background_img=get_img(db_user.background_img),
                         username=db_user.username,
                         description=db_user.description,
                         date_of_birth=db_user.date_of_birth,
                         date_added=db_user.date_added,
                         last_activity=db_user.last_activity,
                         articles=convert_to_articles(db_user.articles, db_user, db, "list")
                         )
        return user


def check_user_email(db: Session, email: EmailStr):
    checker = get_users(db=db).filter(Users.email == email).first()
    return 0 if checker else send_code(email)


def get_users_by_username(db: Session, username: str, skip: int, limit: int):
    db_users = get_users(db=db).filter(Users.username.like(f"%{username}%")).offset(skip).limit(limit).all()
    checked = []
    for db_user in db_users:
        if db_user:
            checked.append(convert_to_get_user(db_user))
    return checked


def update_user(db: Session, user_id: int, avatar, background_img, user: UserUpdateModel):
    db_user = get_users(db=db).filter(Users.id == user_id).first()
    db_user.date_of_birth = user.date_of_birth
    db_user.description = user.description
    db_user.first_name = user.first_name
    db_user.second_name = user.second_name
    db_user.username = user.username
    db_user.text_color = user.text_color
    db_user.background_color = user.background_color
    db_user.avatar = f'static/user{db_user.id}_avatar.jpg'
    db_user.background_img = f'static/user{db_user.id}_background.jpg'
    db.commit()

    with open(db_user.avatar, 'wb') as image:
        image.write(avatar)
    with open(db_user.background_img, 'wb') as image:
        image.write(background_img)

        articles = get_all_articles(db=db).join(association_table_user_articles).filter(association_table_user_articles.c.user_id == db_user.id)
        user = UserModel(id=db_user.id,
                         rating=db_user.rating,
                         is_active=db_user.is_active,
                         is_admin=db_user.is_admin,
                         first_name=db_user.first_name,
                         second_name=db_user.second_name,
                         avatar=get_img(db_user.avatar),
                         background_img=get_img(db_user.background_img),
                         username=db_user.username,
                         description=db_user.description,
                         date_of_birth=db_user.date_of_birth,
                         date_added=db_user.date_added,
                         last_activity=db_user.last_activity,
                         articles=convert_to_articles(articles, db_user, db, "list")
                         )
        return user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db=db).filter(Users.id == user_id).first()
    db_user.is_deleted = True
    db.commit()
    return db_user


def create_user(db: Session, user: UserCreateModel):
    time = datetime.now()
    db_user = Users(email=user.email,
                    login=user.login,
                    password=get_password_hash(user.password),
                    username=user.username,
                    last_activity=time,
                    is_active=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.avatar = f'static/user{db_user.id}_avatar.jpg'
    db.commit()

    with open("static/avatar.png", "rb") as f:
        avatar = f.read()
    with open(db_user.avatar, 'wb') as image:
        image.write(avatar)
    return 200


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: EmailStr = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db_user = get_users(db).filter(Users.email == email).first()
    if db_user:
        db_user.last_activity = datetime.utcnow()
        return db_user
    raise credentials_exception


def get_current_user_base(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: EmailStr = payload.get("sub")
        db_user = get_users(db).filter(Users.email == email).first()
        if db_user:
            db_user.last_activity = datetime.utcnow()
            return db_user
    except AttributeError:
        return

def login(db: Session, email: EmailStr, password: str):
    db_user = get_users(db=db).filter(Users.email == email).first()
    if db_user and verify_password(password, db_user.password):
        db_user.is_active = True
        db.commit()
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.email}, expires_delta=access_token_expires
        )
        user = UserLoginModel(id=db_user.id,
                              username=db_user.username,
                              avatar=get_img(db_user.avatar),
                              access_token=access_token,
                              token_type="bearer"
                              )
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


def logout(db: Session, user_id: int):
    db_user = get_users(db=db).filter(Users.id == user_id).first()
    if db_user:
        db_user.is_active = False
        db.commit()
        return 0


def get_last_articles(db_user: Users, db: Session, skip: int, limit: int):
    db_articles = get_articles(db=db).order_by(-Articles.id).offset(skip).limit(limit).all()
    return convert_to_articles(db_articles, db_user, db, "list")


def get_popular_articles(db_user: Users, db: Session, skip: int, limit: int):
    time = datetime.now() - timedelta(days=7)
    db_articles = get_articles(db=db).filter(Articles.date_added >= time).order_by(Articles.rating.desc()).offset(
        skip).limit(limit).all()
    return convert_to_articles(db_articles, db_user, db, "list")


def get_read_articles_by_user(db: Session, db_user: Users, skip: int, limit: int):
    db_articles = get_articles(db=db).join(association_table_readers).filter(association_table_readers.c.user_id == db_user.id).offset(skip).limit(
        limit).all()
    return convert_to_articles(db_articles, db_user, db, "list")


def get_view_articles_by_user(db: Session, db_user: Users, skip: int, limit: int):
    db_articles = get_articles(db=db).join(association_table_views_article).filter(association_table_views_article.c.user_id == db_user.id).offset(
        skip).limit(limit).all()
    return convert_to_articles(db_articles, db_user, db, "list")


def get_article_by_id(db: Session, article_id: int, db_user: Users):
    db_article = get_articles(db=db).filter(Articles.id == article_id).first()
    return convert_to_articles([db_article], db_user, db, "obj")


def get_articles_by_tag(tag_id: int, db: Session, db_user: Users, skip: int, limit: int):
    db_articles = get_articles(db=db).join(association_table_tags).filter(association_table_tags.c.tag_id == tag_id).offset(skip).limit(limit).all()
    return convert_to_articles(db_articles, db_user, db, "list")


def get_articles_by_mark(mark_id: int, db: Session, db_user: Users, skip: int, limit: int):
    db_articles = get_articles(db=db).join(association_table_marks).filter(association_table_marks.c.mark_id == mark_id).offset(skip).limit(
        limit).all()
    return convert_to_articles(db_articles, db_user, db, "list")


def get_articles_by_title(db: Session, title: str, skip: int, limit: int):
    db_articles = get_articles(db=db).filter(Articles.title.like(f"%{title}%")).offset(skip).limit(limit).all()
    return db_articles


def get_articles_by_user(db: Session, user_id: int, skip: int, limit: int):
    db_articles = get_articles(db=db).join(association_table_user_articles).filter(association_table_user_articles.c.user_id == user_id).offset(skip).limit(
        limit).all()
    db_user = get_users(db=db).filter(Users.id == user_id).first()
    return convert_to_articles(db_articles, db_user, db, "list")


def update_article(db: Session, article: ArticleEditModel, db_user: Users):
    db_article = get_all_articles(db=db).filter(Articles.id == article.id).first()
    db_article.title = article.title
    db_article.description = article.description
    db_article.text = article.text
    db_article.period_start = article.period_start
    db_article.period_end = article.period_end
    db_article.background_color = article.background_color
    db_article.text_color = article.text_color

    db_article.background_img = f'static/article{db_article.id}_background.jpg'
    with open(db_article.background_img, 'wb') as image:
        image.write(article.background_img)

    db_article.tags = []
    for tag_id in article.tags:
        db_tag = get_tags(db).filter(Tags.id == tag_id).first()
        if db_tag:
            db_article.tags.append(db_tag)

    db_article.marks = []
    for mark_id in article.marks:
        db_mark = get_marks(db).filter(Marks.id == mark_id).first()
        if db_mark:
            db_article.marks.append(db_mark)
    db.commit()

    return convert_to_articles([db_article], db_user, db, "obj")


def publish_article(db: Session, db_user: Users, article_id: int):
    db_article = get_all_articles(db).filter(Articles.id == article_id).first()
    db_article.is_published = True
    db.commit()
    return convert_to_articles([db_article], db_user, db, "obj")


def delete_article(db: Session, db_user: Users, article_id: int):
    db_article = get_all_articles(db).filter(Articles.id == article_id).first()
    db_article.is_published = True
    db.commit()
    return convert_to_articles([db_article], db_user, db, "obj")


def read_article(db: Session, db_user: Users, article_id: int):
    db_article = get_articles(db).filter(Articles.id == article_id).first()
    if db_article in db_user.read:
        db_user.read.remove(db_article)
    else:
        db_user.read.append(db_article)
    db.commit()
    return convert_to_articles([db_article], db_user, db, "obj")


def view_article(db: Session, db_user: Users, article_id: int):
    db_article = get_articles(db).filter(Articles.id == article_id).first()
    db_user.views.append(db_article)
    db.commit()
    return 200


def add_author(db: Session, user_id: int, article_id: int, role: str):
    db.query(association_table_user_articles).filter(association_table_user_articles.c.user_id == user_id).filter(
        association_table_user_articles.c.article_id == article_id).delete()
    stmt = (
        insert(association_table_user_articles).
            values(user_id=user_id, article_id=article_id, role=role)
    )
    db.execute(stmt)
    db.commit()
    return 200


def create_rating_article(db: Session, user_id: int, article_id: int, rating: int):
    db.query(association_table_rating).filter(association_table_rating.c.user_id == user_id).delete()
    stmt = (
        insert(association_table_rating).
            values(user_id=user_id, article_id=article_id, rating=rating)
    )
    db.execute(stmt)
    db_article = get_articles(db).filter(Articles.id == article_id).first()
    rating = db.query(func.avg(association_table_rating.c.rating)).filter(
        association_table_rating.c.article_id == article_id).scalar()
    db_article.rating = rating
    db.commit()
    return rating


def create_article(db: Session, db_user: Users, title: str):
    db_article = Articles(title=title,
                          is_published=False)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    add_author(db=db, user_id=db_user.id, article_id=db_article.id, role="creator")
    return db_article.id


def search_articles(db: Session, db_user: Users, search: ArticleSearchModel):
    db_articles = db.query(Articles).filter(Articles.is_deleted == 0).filter(Articles.is_moderated == 1)
    db_articles = db_articles.filter(Articles.is_published == 1)

    if search.title:
        db_articles = db_articles.filter(Articles.title.like(f"%{search.title}%"))

    if search.max_rating != 0:
        db_articles = db_articles.filter(Articles.rating <= search.max_rating)

    if search.min_rating != 0:
        db_articles = db_articles.filter(Articles.rating >= search.min_rating)

    if search.authors_add is not None:
        for user_id in search.authorship_add:
            db_articles = db_articles.join(association_table_user_articles).filter(association_table_user_articles.c.user_id == user_id)

    if search.authors_del is not None:
        for user_id in search.authorship_del:
            db_articles = db_articles.join(association_table_user_articles).filter(association_table_user_articles.c.user_id != user_id)

    if search.tags_add is not None:
        for tag_id in search.tags_add:
            db_articles = db_articles.join(association_table_tags).filter(association_table_tags.c.tag_id == tag_id)

    if search.tags_del is not None:
        for tag_id in search.tags_del:
            db_articles = db_articles.join(association_table_tags).filter(association_table_tags.c.tag_id != tag_id)

    if search.marks_add is not None:
        for mark_id in search.marks_add:
            db_articles = db_articles.join(association_table_marks).filter(association_table_marks.c.mark_id == mark_id)

    if search.marks_del is not None:
        for mark_id in search.marks_del:
            db_articles = db_articles.join(association_table_marks).filter(association_table_marks.c.mark_id != mark_id)

    return convert_to_articles(db_articles.all(), db_user)


def get_category_by_id(db: Session, category_id: int):
    db_category = get_categories(db).filter(Categories.id == category_id).first()
    return convert_to_category(db_category)


def create_category(db: Session, category: CategoryCreateModel):
    db_category = Categories(title=category.title,
                             description=category.description,
                             text_color=category.text_color,
                             background_color=category.background_color)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return convert_to_category(db_category)


def get_popular_tags(db: Session, skip: int, limit: int):
    db_tags = get_tags(db).order_by(func.random()).offset(skip).limit(limit).all()
    return convert_to_base_tags(db_tags, db)


def get_tag_by_id(db: Session, tag_id: int):
    db_tag = get_tags(db).filter(Tags.id == tag_id).first()
    return convert_to_tag(db_tag, db)


def get_tags_by_title(db: Session, title: str, skip: int, limit: int):
    db_tags = get_tags(db).filter(Tags.title.like(f"%{title}%")).offset(skip).limit(limit).all()
    return convert_to_base_tags(db_tags, db)


def create_tag(db: Session, tag: TagCreateModel):
    db_tag = Tags(title=tag.title,
                  description=tag.description,
                  category_id=tag.category_id)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return convert_to_tag(db_tag, db)


def get_popular_marks(db: Session, skip: int, limit: int):
    db_marks = get_marks(db).order_by(func.random()).offset(skip).limit(limit).all()
    return convert_to_base_marks(db_marks, db)


def get_mark_by_id(db: Session, mark_id: int):
    db_mark = get_marks(db).filter(Marks.id == mark_id).first()
    return convert_to_mark(db_mark, db)


def get_marks_by_title(db: Session, title: str, skip: int, limit: int):
    db_marks = get_marks(db).filter(Tags.title.like(f"%{title}%")).offset(skip).limit(limit).all()
    return convert_to_base_marks(db_marks, db)


def create_mark(db: Session, mark: MarkCreateModel):
    db_mark = Marks(title=mark.title,
                    description=mark.description,
                    category_id=mark.category_id)
    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)
    return convert_to_mark(db_mark, db)


def get_favorite_comments_by_user(db: Session, db_user: Users, skip: int, limit: int):
    db_comments = get_comments(db=db).join(association_table_comments_likes).filter(association_table_comments_likes.c.user_id == db_user.id).offset(
        skip).limit(
        limit).all()
    return convert_to_comments(db_comments=db_comments, db_user=db_user, comm="list")


def get_comments_by_user_id(db: Session, db_user: Users, skip: int, limit: int):
    db_comments = get_comments(db=db).filter(Comments.user_id == db_user.id).offset(skip).limit(
        limit).all()
    return convert_to_comments(db_comments=db_comments, db_user=db_user, comm="list")


def get_comments_by_article_id(db: Session, article_id: int, db_user: Users, skip: int, limit: int):
    db_comments = get_comments(db=db).filter(Comments.article_id == article_id).offset(skip).limit(
        limit).all()
    return convert_to_comments(db_comments=db_comments, db_user=db_user, comm="list")


def like_comment(db: Session, comment_id: int, db_user: Users, mark: int):
    db.query(association_table_comments_likes).filter(association_table_comments_likes.c.user_id == db_user.id).delete()
    comm = (
        insert(association_table_comments_likes).
            values(user_id=db_user.id, comment_id=comment_id, mark=mark)
    )
    db.execute(comm)
    db_comment = get_comments(db=db).filter(Comments.id == comment_id).first()
    likes_count = db.query(func.sum(association_table_comments_likes.c.mark)).filter(
        association_table_comments_likes.c.comment_id == comment_id).scalar()
    db_comment.likes_count = likes_count
    db.commit()
    return convert_to_comments(db_comments=[db_comment], db_user=db_user, comm="obj")


def update_comment_text(db: Session, comment_id: int, text: str, db_user: Users):
    db_comment = get_comments(db=db).filter(Comments.id == comment_id).first()
    db_comment.text = text
    db.commit()
    return convert_to_comments(db_comments=[db_comment], db_user=db_user, comm="obj")


def create_comment(db: Session, db_user: Users, comment: CommentCreateModel):
    if comment.type == "news":
        db_comment = Comments(news=comment.origin_id,
                              answer_id=comment.answer_id,
                              text=comment.text,
                              user_id=db_user.id,
                              type=comment.type)
    elif comment.type == "article":
        db_comment = Comments(article_id=comment.origin_id,
                              answer_id=comment.answer_id,
                              text=comment.text,
                              user_id=db_user.id,
                              type=comment.type)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return convert_to_comments(db_comments=[db_comment], db_user=db_user, comm="obj")


def get_compilations_by_user(db: Session, db_user: Users, skip: int, limit: int):
    db_comps = get_comps(db=db).filter(Compilations.user_id == db_user.id).offset(skip).limit(limit).all()
    comps = []
    for db_comp in db_comps:
        comp = CompilationModel(id=db_comp.id,
                                title=db_comp.title,
                                description=db_comp.description,
                                is_public=db_comp.is_public,
                                articles=convert_to_articles(db_comp.articles, db_user, db, "list"))
        comps.append(comp)
    return comps


def article_is_in_compilation(db: Session, user_id: int, article_id: int):
    db_article = get_articles(db=db).filter(Articles.id == article_id).first()
    db_user = get_users(db=db).filter(Users.id == user_id).first()
    comps = []
    for compilation in db_user.compilations:
        comp = CompilationGetModel(id=compilation.id,
                                   title=compilation.title,
                                   is_saved=db_article in compilation.articles)
        comps.append(comp)
    return comps


def save_article_in_compilation(db: Session, compilation_id: int, user_id: int, article_id: int):
    db_article = get_articles(db=db).filter(Articles.id == article_id).first()
    db_comp = get_comps(db=db).filter(Compilations.id == compilation_id).first()
    db_comp.articles.append(db_article)
    db.commit()
    return article_is_in_compilation(db=db, user_id=user_id, article_id=article_id)


def create_compilation(db: Session, user_id: int, compilation: CompilationCreateModel):
    db_compilation = Compilations(title=compilation.title,
                                  description=compilation.description,
                                  is_public=compilation.is_public,
                                  user_id=user_id)
    db.add(db_compilation)
    db.commit()
    db.refresh(db_compilation)
    return 200
