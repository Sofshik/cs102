from scraputils import get_news  # type: ignore
from sqlalchemy import Column, Integer, String, create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):  # type: ignore
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    s = session()
    news_list = get_news("https://news.ycombinator.com/newest", n_pages=1)
    for i in enumerate(news_list):
        news = News(
            title=news_list[i]["title"],
            author=news_list[i]["author"],
            url=news_list[i]["url"],
            comments=news_list[i]["comments"],
            points=news_list[i]["points"],
        )
        s.add(news)
        s.commit()
