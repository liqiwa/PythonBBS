#完成主题数据的维护和更新
from flask import Blueprint, render_template
from pythonnewbbs import db

#声明蓝图
bp  =Blueprint("blog",__name__,url_prefix="/blog")

@bp.route('/topic',methods = ['GET'])
def topic():
    return render_template('blog/topic.html')

@bp.route('/category',methods = ['GET'])
def category():
    return render_template('blog/category.html')
@bp.route('/')
def index():
    dbsession = db.get_db()
    posts = dbsession.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)
