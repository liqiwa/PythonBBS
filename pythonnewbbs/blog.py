#完成主题数据的维护和更新
import datetime
from flask import Blueprint, render_template,abort,request,redirect,url_for,flash,session,g
from pythonnewbbs import db
from pythonnewbbs.db import Categories,Topics,Posts

#声明蓝图
bp  =Blueprint("blog",__name__)

@bp.route('/topic',methods = ['GET','POST'])
def topic():
    #查询数据库中所有的类别，在页面选项中展示出来
        if request.method == 'GET':
            error = None
            dbsession = db.get_db()
            posts = dbsession.query(Categories).all()
            #没有创建类别需提示，锁定提交按钮为灰色，或者弹出按钮后，回到首页。
            if  len(posts) == 0:
                error = '类别为空，联系管理员添加类别'
            else:
                return  render_template('blog/topic.html',posts = posts)
            flash(error)
        if request.method == 'POST':
            error = None
            topicsubject = request.form['topic_subject']
            topiccat = request.form['topic_cat']
            topicdate = datetime.datetime.now().replace(microsecond=0)
            #获得用户信息
            if g.user is None:
                error ='请登陆后发布帖子'
            else:
                topicby = session['user_id']
                postcontent = request.form['post_content']
                postdate = datetime.datetime.now().replace(microsecond=0)
                postby = topicby
                if error is None:
                    dbsession = db.get_db()
                    newtopic = Topics(topic_subject = topicsubject,topic_date = topicdate,topic_cat = topiccat,
                                      topic_by = topicby)
                    dbsession.add(newtopic)
                    #add 后可以直接查询ID 信息
                    dbsession.flush()
                    newpost = Posts(post_content = postcontent,post_date = postdate,post_topic = newtopic.topic_id,
                                    post_by = postby)
                    dbsession.add(newpost)
                    dbsession.commit()
                    dbsession.close
                    return redirect(url_for('blog.topic'))
            flash(error)
        return render_template('blog/topic.html')

def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    dbsession = db.get_db()
    post = (
    dbsession.query(db.Topics).all()
    )

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post

@bp.route('/category',methods = ['GET','POST'])
def category():

    if request.method == 'POST':
        catname = request.form['catname']
        catdescription = request.form['catdescription']
        dbsession = db.get_db()
        camg = dbsession.query(Categories).filter(Categories.cat_name == catname).first()
        error = None
        if camg is not None:
            error='分类信息已经存在'
        if error is None:
            newCat = Categories(cat_name = catname,cat_description = catdescription)
            dbsession.add(newCat)
            dbsession.commit()
            dbsession.close

            return redirect(url_for('blog.category'))
        flash(error)
    return render_template('blog/category.html')

@bp.route('/')
def index():
    dbsession = db.get_db()
    posts = dbsession.query(db.Topics).all()
    return render_template('blog/index.html', posts=posts)
