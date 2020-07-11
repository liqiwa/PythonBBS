#完成主题数据的维护和更新
import datetime
from flask import Blueprint, render_template,abort,request,redirect,url_for,flash,session,g
from sqlalchemy import join,outerjoin
from pythonnewbbs import db
from pythonnewbbs.auth import login_required
from pythonnewbbs.db import Categories,Topics,Posts,Users

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
                return  render_template('blog/createtopic.html',posts = posts)
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
        return render_template('blog/createtopic.html')

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
    return render_template('blog/createcategory.html')

@bp.route('/')
def index():
    dbsession = db.get_db()
    #联合topic，category 查询 展示
    sql = """select   cc.cat_id,cc.cat_name,cc.cat_description,cc.total,tt.topic_subject,tt.topic_date
from  (
 
select t.topic_cat,t.topic_subject,t.topic_date,count(1)as row_num from topics t left join topics o on t.topic_cat = o.topic_cat where  t.topic_date <= o.topic_date group by t.topic_cat,t.topic_date,t.topic_subject
)tt ,(
select c.cat_id,c.cat_name,c.cat_description,count(1) total from categories c,topics t 
where c.cat_id = t.topic_cat group by c.cat_id,c.cat_name,c.cat_description
) cc
where tt.topic_cat = cc.cat_id and tt.row_num =1;"""
    posts = dbsession.execute(sql).fetchall()

    return render_template('blog/index.html', posts=posts)
#查询各个主题信息
@bp.route('/<int:id>/topicchat',methods = ('GET','POST'))
@login_required
def topicchat(id):

    dbsession = db.get_db()
    posts = dbsession.query(Topics.topic_id,Topics.topic_subject,Topics.topic_date,Users.user_name).join(
        Users,Topics.topic_by == Users.user_id).filter(Topics.topic_cat == id).all()


    return render_template('blog/topicchat.html',posts = posts)
#展示各个主题的回复明细
@bp.route('/<int:id>/replychat',methods = ('GET','POST'))
@login_required
def replychat(id):
    print('这个是获取到的主题ID：', id)
    if request.method =='GET':
        dbsession = db.get_db()
        posts = dbsession.query(Posts.post_id,Posts.post_content,Posts.post_date,
                            Topics.topic_subject,Users.user_name,Users.user_id).outerjoin(
        Users,Posts.post_by == Users.user_id).outerjoin(
        Topics,Posts.post_topic == Topics.topic_id).filter(Topics.topic_id == id).all()
        return render_template('blog/replychat.html',posts = posts)
    if request.method =='POST':
        #获取关于该主题的回复
        reply_content = request.form['reply_content']
        posts_date = datetime.datetime.now().replace(microsecond=0)
        posts_topic = id
        posts_by = session['user_id']
        #连接数据库插入
        dbsession = db.get_db()
        newposts = Posts(post_by = posts_by,post_date = posts_date,
                         post_content = reply_content,post_topic = id)
        dbsession.add(newposts)
        dbsession.commit()
        dbsession.close
        #添加入参，为刚才主题的博客，再次转到当前页面，及时刷新，信息可以立刻看到。
        return redirect(url_for('blog.replychat',id =id))
    return render_template('blog/replychat.html')
@bp.route('/<int:id>/replyupdate',methods = ('GET','POST'))
@login_required
def replyupdate(id):
    #展示要更新的源数据
    if  request.method =='GET':
        post_id = id
        dbsession = db.get_db()
        posts = dbsession.query(Posts).filter(Posts.post_id == id).all()
        return render_template('blog/replyupdate.html',posts = posts)
    #提交后，获取更新内容，进行更新
    if  request.method == 'POST':
        post_id = id
        post_content = request.form['post_content']
        post_date = datetime.datetime.now().replace(microsecond=0)
        dbsession = db.get_db()
        updatepost = dbsession.query(Posts).filter(
        Posts.post_id == post_id).update({Posts.post_content:post_content,Posts.post_date:post_date})
        #从要更新的内容获得上级回复主题信息，做为跳转
        post_topic = dbsession.query(Posts.post_topic).filter(Posts.post_id == post_id).first()
        dbsession.commit()
        dbsession.close
        return redirect(url_for('blog.replychat',id = post_topic[0]))

@bp.route('/<int:id>/replydelete',methods = ('GET','POST'))
@login_required
def replydelete(id):
    if  request.method =='POST':
        post_id = id
        dbsession = db.get_db()
        post_topic = dbsession.query(Posts.post_topic).filter(Posts.post_id == post_id).first()
        dbsession.query(Posts).filter(Posts.post_id == post_id).delete()
        dbsession.commit()
        dbsession.close
        return redirect(url_for('blog.replychat',id = post_topic[0]))
    return render_template('blog/replyupdate.html')
