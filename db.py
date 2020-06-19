#连接本地数据库，使用SQLAlchemy框架
from sqlalchemy import Column,String,Integer,INT,DateTime,Text,create_engine,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

Base = declarative_base() #生成ORM基类
#Create table Users ，Question：not null、forregition
#创建用户表
class Users(Base):
    __tablename__ = 'users'
    user_id = Column(INT(8),primary_key=True,nullable=False,autoincrement=True)
    user_name = Column(String(30),nullable=False)
    user_pass =Column(String(255),nullable=False)
    user_email = Column(String(255),nullable=False)
    user_date = Column(DateTime,nullable=False)
    user_level = Column(INT(8),nullable=False)
#创建主题表
class Topics(Base):
    __talblename__ = 'topics'
    topic_id = Column(INT(8),primary_key=True,nullable=False,autoincrement=True)
    topic_subject = Column(String(255),nullable=False)
    topic_date = Column(DateTime,nullable=False)
    topic_cat = Column(INT(8),nullable=False)
    topic_by = Column(INT(8),nullable=False)
#创建分类表
class Categories(Base):
    __tablename__ = 'categories'
    cat_id = Column(INT(8),primary_key=True,nullable=False,autoincrement=True)
    cat_name = Column(String(255),nullable=False,unique=True)
    cat_description = Column(String(255),nullable=False)

# #创建发布信息
class Posts(Base):
    __tablename__ = 'posts'
    post_id = Column(INT(8),primary_key=True,nullable=False,autoincrement=True)
    post_content = Column(Text,nullable=False)
    post_date = Column(DateTime,nullable=False)
    post_topic = Column(INT(8),nullable=False)
    post_by = Column(INT(8),nullable=False)


#连接数据库
def get_db():
    engine = create_engine('mysql+mysqlconnector://root:123@localhost:3306/pybbs')
    DBsession = sessionmaker(bind=engine)
    session = DBsession()
    return  session
