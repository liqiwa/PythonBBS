from flask import Flask,request,render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/signup')
def signup():
    return render_template('register.html')
@app.route('/login',methods=['POST'])
def singin():
    #插入Mysql数据库中
    request.form['username']
    return render_template('')
if __name__=='__main__':
    app.run()