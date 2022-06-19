from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Float, Date, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

association_table_comments_likes = Table('comment_likes', Base.metadata,
                                         Column('user_id', Integer, ForeignKey('users.id')),
                                         Column('comment_id', Integer, ForeignKey('comments.id')),
                                         Column('mark', Integer))

association_table_user_articles = Table('user_articles', Base.metadata,
                                        Column('user_id', Integer, ForeignKey('users.id')),
                                        Column('article_id', Integer, ForeignKey('articles.id')),
                                        Column('role', String))

association_table_user_news = Table('user_news', Base.metadata,
                                    Column('user_id', Integer, ForeignKey('users.id')),
                                    Column('news_id', Integer, ForeignKey('news.id')),
                                    Column('role', String))

association_table_readers = Table('articles_readers', Base.metadata,
                                  Column('user_id', Integer, ForeignKey('users.id')),
                                  Column('article_id', Integer, ForeignKey('articles.id')))

association_table_views_article = Table('articles_views', Base.metadata,
                                        Column('user_id', Integer, ForeignKey('users.id')),
                                        Column('article_id', Integer, ForeignKey('articles.id')))

association_table_rating = Table('article_rating', Base.metadata,
                                 Column('user_id', Integer, ForeignKey('users.id')),
                                 Column('article_id', Integer, ForeignKey('articles.id')),
                                 Column('rating', String))

association_table_compilations = Table('user_compilations', Base.metadata,
                                       Column('compilation_id', Integer, ForeignKey('compilations.id')),
                                       Column('article_id', Integer, ForeignKey('articles.id')))

association_table_tags = Table('article_tags', Base.metadata,
                               Column('tag_id', Integer, ForeignKey('tags.id')),
                               Column('article_id', Integer, ForeignKey('articles.id')))

association_table_marks = Table('article_marks', Base.metadata,
                                Column('mark_id', Integer, ForeignKey('marks.id')),
                                Column('article_id', Integer, ForeignKey('articles.id')))


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    username = Column(String)
    first_name = Column(String)
    second_name = Column(String)
    email = Column(String, unique=True)
    rating = Column(Integer, default=0)
    avatar = Column(String)
    background_img = Column(String)
    background_color = Column(String)
    text_color = Column(String)
    description = Column(Text)
    date_of_birth = Column(Date)
    is_active = Column(Boolean)
    is_deleted = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    last_activity = Column(DateTime)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())
    comments = relationship('Comments')
    compilations = relationship('Compilations')

    def __repr__(self):
        return f"User(id={self.id}, login={self.login}, password={self.password}, username={self.username}, " \
               f"first_name={self.first_name}, second_name={self.second_name}, email={self.email}, " \
               f"rating={self.rating}, avatar={self.avatar}, background_img={self.background_img}, " \
               f"background_color={self.background_color}, text_color={self.text_color}, description={self.description}, " \
               f"date_of_birth={self.date_of_birth}, is_active={self.is_active}, is_deleted={self.is_deleted}, " \
               f"is_admin={self.is_admin}, last_activity={self.last_activity}, date_added={self.date_added}, " \
               f"date_updated={self.date_updated}, comments={self.comments}, compilations={self.compilations})"


class Comments(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    answer_id = Column(Integer, default=0)
    text = Column(Text)
    type = Column(String)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    article_id = Column(Integer, ForeignKey('articles.id'), default=0)
    news_id = Column(Integer, ForeignKey('news.id'), default=0)
    likes_count = Column(Integer, default=0)
    likes = relationship("Users", backref="comment_likes", cascade="all,delete,save-update",
                         secondary=association_table_comments_likes)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f"Comment(id={self.id}, answer_id={self.answer_id}, text={self.text}, type={self.type}, " \
               f"date_added={self.date_added}, date_updated={self.date_updated}, user_id={self.user_id}), " \
               f"article_id={self.article_id}, news_id={self.news_id}, likes_count={self.likes_count}), " \
               f"likes={self.likes}, is_deleted={self.is_deleted}" \

class Articles(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    text = Column(Text)
    period_start = Column(Date)
    period_end = Column(Date)
    background_color = Column(String)
    background_img = Column(String)
    text_color = Column(String)
    rating = Column(Float, default=0)
    is_published = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    is_moderated = Column(Boolean, default=True)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())
    comments = relationship('Comments')
    authors = relationship("Users", backref="articles", cascade="all,delete,save-update",
                           secondary=association_table_user_articles)
    readers = relationship("Users", backref="read", cascade="all,delete,save-update",
                           secondary=association_table_readers)
    viewers = relationship("Users", backref="views", cascade="all,delete,save-update",
                           secondary=association_table_views_article)
    article_rating = relationship("Users", backref="article_rating", cascade="all,delete,save-update",
                                  secondary=association_table_rating)
    tags = relationship("Tags", backref="articles", cascade="all,delete,save-update",
                        secondary=association_table_tags)
    marks = relationship("Marks", backref="articles", cascade="all,delete,save-update",
                         secondary=association_table_marks)

    def __repr__(self):
        return f"Article(id={self.id}, title={self.title}, description={self.description}, text={self.text}, " \
               f"period_start={self.period_start}, period_end={self.period_end}, background_color={self.background_color}, " \
               f"background_img={self.background_img}, text_color={self.text_color}, rating={self.rating}, " \
               f"is_published={self.is_published}, is_deleted={self.is_deleted}, is_moderated={self.is_moderated}, " \
               f"date_added={self.date_added}, date_updated={self.date_updated}, comments={self.comments}, " \
               f"authors={self.authors}, readers={self.readers}, viewers={self.viewers}, " \
               f"article_rating={self.article_rating}, tags={self.tags}, marks={self.marks})"


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(Text)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())
    comments = relationship('Comments')
    authors = relationship("Users", backref="news", cascade="all,delete,save-update",
                           secondary=association_table_user_news)

    def __repr__(self):
        return f"News(id={self.id}, title={self.title}, text={self.text}, date_added={self.date_added}, " \
               f"date_updated={self.date_updated}, comments={self.comments}, authors={self.authors})"


class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    text_color = Column(String)
    background_color = Column(String)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())
    tags = relationship('Tags')
    marks = relationship('Marks')
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f"Category(id={self.id}, title={self.title}, description={self.description}, text_color={self.text_color}, " \
               f"background_color={self.background_color}, date_added={self.date_added}, date_updated={self.date_updated}, tags={self.tags}, marks={self.marks}, is_deleted={self.is_deleted})"


class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())
    category_id = Column(Integer, ForeignKey('categories.id'))
    is_deleted = Column(Boolean, default=False)
    is_moderated = Column(Boolean, default=True)

    def __repr__(self):
        return f"Tag(id={self.id}, title={self.title}, description={self.description}, date_added={self.date_added}, date_updated={self.date_updated}, category_id={self.category_id}, is_deleted={self.is_deleted}, is_moderated={self.is_moderated})"


class Marks(Base):
    __tablename__ = "marks"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())
    category_id = Column(Integer, ForeignKey('categories.id'))
    is_deleted = Column(Boolean, default=False)
    is_moderated = Column(Boolean, default=True)

    def __repr__(self):
        return f"Mark(id={self.id}, title={self.title}, description={self.description}, date_added={self.date_added}, date_updated={self.date_updated}, category_id={self.category_id}, is_deleted={self.is_deleted}, is_moderated={self.is_moderated})"


class Compilations(Base):
    __tablename__ = "compilations"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    is_public = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    articles = relationship("Articles", backref="compilations", cascade="all,delete,save-update",
                            secondary=association_table_compilations)

    def __repr__(self):
        return f"Compilation(id={self.id}, title={self.title}, description={self.description}, is_public={self.is_public}, is_deleted={self.is_deleted}, date_added={self.date_added}, date_updated={self.date_updated}, user_id={self.user_id}, articles={self.articles})"
