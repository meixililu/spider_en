from sqlalchemy import Column, String, create_engine,Integer,Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

base=declarative_base()
engine=create_engine("mysql+pymysql://root:Xbkj2613569!@115.29.105.123:3306/spider?charset=utf8",echo=True,pool_size=100)
# engine=create_engine("mysql+pymysql://root:Xbkj2613569!@localhost/spider?charset=utf8",echo=True,pool_size=100)
DBSession = sessionmaker(bind=engine)

class Crawl(base):

    __tablename__ = "crawl"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Text, nullable=False, index=True)
    title = Column(Text)
    source_name = Column(String(60))
    category = Column(String(60))
    film_name = Column(Text)
    text = Column(Text)
    source_url = Column(Text)
    img = Column(Text)


def isUrlExit(url):
    session = DBSession()
    query = session.query(Crawl)
    # count = query.filter(Crawl.url == url).count()
    count = query.all()
    for item in count:
        print item.url
    session.close()
    # return count > 0

def saveSpiderDBUrl(url):
    session = DBSession()
    crawl = Crawl(url=url)
    session.add(crawl)
    session.commit()
    # print crawl.id
    # session.close()
    return crawl.id