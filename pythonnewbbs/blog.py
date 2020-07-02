#完成主题数据的维护和更新
from flask import Blueprint, render_template,abort,request,redirect,url_for,flash
from pythonnewbbs import db
from pythonnewbbs.db import Categories,Topics,Posts

#声明蓝图
bp  =Blueprint("blog",__name__)

@bp.route('/topic',methods = ['GET','POST'])
def topic():
    #查询数据库中所有的类别，在页面选项中展示出来
        if request.method == 'GET':
            dbsession = db.get_db()
            posts = dbsession.query(Categories.cat_name).all()
        return  render_template('blog/topic.html',posts = posts)
        if request.method == 'POST':
            # topicsubject = request.form['topic_subject']
            # topiccat = request.form['topic_cat']
            # topicdate =
            # topby = request.form['']
            # postcontent = request.form['post_content']
            #

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
