from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
import string


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    query = request.query.decode()
    id = int(query["id"])
    label = query["label"]
    s = session()
    s.query(News.id).filter(News.id == id).update({News.label: label})
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    news = get_news("https://news.ycombinator.com/", 3)
    s = session()
    for new in news:
        if len(s.query(News.author).filter_by(author='author').all()) == 0 or len(s.query(News.title).filter_by(title='title').all()) == 0:
            s.add(
                News(
                    title=new["title"],
                    author=new["author"],
                    url=new["url"],
                    points=new["points"],
                    comments=new["comments"],
                )
            )
    s.commit()
    redirect("/news")


def clean(s):
    translator = str.maketrans('', '', string.punctuation)
    return s.translate(translator)


@route("/classify")
def classify_news():
    s = session()
    model = NaiveBayesClassifier()
    train = s.query(News).filter(News.label != None).all()
    model.fit([clean(news.title).lower() for news in train], [news.label for news in train])
    test = s.query(News).filter(News.label == None).all()
    return template(
        'news_template',
        rows=sorted(test, key=lambda news: get_l(model.predict(clean(news.title).lower()))),
    )


def get_l(label):
    if label == "never":
        return 2
    elif label == "maybe":
        return 1
    elif label == "good":
        return 0


if __name__ == "__main__":
    run(host="localhost", port=8080)