#coding:utf-8
from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory
from app import app
from .forms import LoginForm,RegisterForm,EditForm,SellBookForm,RetrieveForm,PasswordForm
from app import db, models,login_manager
from flask_mail import Mail,Message
from flask_login import login_user,logout_user,login_required,current_user
from app.token import generate_confirmation_token, confirm_token
import datetime
from werkzeug import secure_filename
import os

app.config.update(
    MAIL_SERVER='smtp.sina.com.cn',
    MAIL_PROT=25,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME="shuju_regist@sina.com",
    MAIL_PASSWORD="cht1995516",
    MAIL_DEBUG=True
)
UPLOAD_FOLDER = r'D:/anaconda/envs/flask/start/app/static'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))

@app.route('/')
@app.route('/home')
def index():
    user = { 'nickname': 'Miguel' }
    posts = [
        { 
            'author': { 'nickname': 'John' }, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': { 'nickname': 'Susan' }, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("home.html", title='Home', user=user, posts=posts)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    try:
        if form.validate_on_submit():
            user = models.User.query.filter_by(email=str(form.email.data)).first_or_404()
            if user.activate:
                if user.password == form.password.data:
                    login_user(user, True)
                    return redirect(str(user.email))
                else:
                    flash(u"密码错误")
            else:
                flash(u"您的账号还未验证，请先到您的邮箱验证账户后再登录")
                return redirect(url_for('login'))
    except:
        flag = False
        flash(u"账号不存在")
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    mail = Mail(app)
    form = RegisterForm()
    try:
        if form.validate_on_submit():
            user = models.User(name=form.name.data, password=form.password.data, email=form.email.data,
                               job=form.job.data)
            db.session.add(user)
            db.session.commit()
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url, user_name=user.name)
            subject = u"请确认您的邮箱"
            msg = Message(subject=subject, recipients=[user.email], html=html, sender='shuju_regist@sina.com')
            msg.body = u'研炬'
            mail.send(msg)
            login_user(user)
            flash(u'我们已经向您的邮箱发送了验证邮件，请验证后登录。')
            return redirect('/login')
    except:
        flash(u"抱歉，这个邮箱已经注册，请用您的邮箱找回密码。")
        return redirect(url_for('retrieve'))
    return render_template('register.html',
                           title='Sign In',
                           form=form)


@app.route('/retrieve', methods= ['GET', 'POST'])
def retrieve():
    mail = Mail(app)
    form = RetrieveForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first_or_404()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('retrieve_email', token=token, _external=True)
        html = render_template('retrieve_email.html', confirm_url=confirm_url, user_name=user.name)
        subject = u"重置密码"
        msg = Message(subject=subject, recipients=[user.email], html=html, sender='shuju_regist@sina.com')
        msg.body = u'研炬'
        login_user(user)
        mail.send(msg)
        user.retrieve = False
        db.session.add(user)
        db.session.commit()
        flash(u'我们已经向你的邮箱发送了验证邮件。')
        return redirect('/login')
    return render_template('retrieve.html', title='retrieve', form=form)


@app.route('/Success')
def Sucess():
    return "Sucess"


@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = models.User.query.filter_by(email=email).first_or_404()
    if user.activate:
        flash(u'已确认您的邮箱，欢迎登录研矩。', )
        return redirect(url_for('login'))
    else:
        user.activate = True
        db.session.add(user)
        db.session.commit()
        flash(u'已经确认过您的邮箱，谢谢!')
        return redirect(url_for('login'))


@app.route('/retrieve/<token>', methods=['GET', 'POST'])
def retrieve_email(token):
    try:
        email = confirm_token(token)
    except:
        flash(u'验证链接无效或已超时.')
        return redirect(url_for('retrieve'))
    form = PasswordForm()
    user = models.User.query.filter_by(email=email).first_or_404()
    if user.retrieve:
        return redirect(url_for('login'))
    user.retrieve = True
    db.session.add(user)
    db.session.commit()
    if form.validate_on_submit():
        user.password = form.password.data
        return redirect(url_for('login'))
    return render_template("retrieve_password.html", form=form)


@app.route('/<user_email>')
@login_required
def user(user_email):
    user_login = models.User.query.filter_by(email=user_email).first_or_404()

    if user_login is None:
        flash('User' + user_email + 'not found.')
        return redirect(url_for('index'))
    books = [{'owner': user_login, 'title': 'Test book #1'}, {'owner': user_login, 'title': 'Test book #2'}]
    return render_template('user.html', user=user_login, books=books)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.about_me.data = current_user.about_me
    return render_template('edit.html', form=form)


@app.route('/sell/book', methods=['GET', 'POST'])
@login_required
def sell():
    form = SellBookForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            dir = os.path.abspath('app')
            dir = os.path.join(dir, 'static')
            dir = os.path.join(dir, str(current_user.name))
            if os.path.exists(dir):
                dir = os.path.join(dir, 'sell_book')
                if os.path.exists(dir):
                    book = models.Book(title=form.title.data, info=form.info.data, user_id=current_user.id)
                else:
                    os.mkdir(dir)
                    book = models.Book(title=form.title.data, info=form.info.data, user_id=current_user.id)
            else:
                os.mkdir(dir)
                dir = os.path.join(dir, 'sell_book')
                os.mkdir(dir)
                book = models.Book(title=form.title.data, info=form.info.data, user_id=current_user.id)
            db.session.add(book)
            db.session.commit()
            filename = str(book.id)+str(os.path.splitext(file.filename)[-1])
            filename = secure_filename(filename)
            dir = os.path.join(dir, filename)
            im.save(dir)
            relative_path = os.path.join(current_user.name, 'sell_book')
            relative_path = os.path.join(relative_path, filename)
            relative_path = os.path.join('../static', relative_path)
            book.url = relative_path
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('uploaded_file', filename=filename, dir=str(book.url))+'\\')  # 跳转到预览页面
        return '<p> 你上传了不允许的文件类型 </p>'
    return render_template('sell.html', form=form)


@app.route('/uploaded_file/<filename>')
@login_required
def uploaded_file(filename):
    return '上传成功'


@app.route('/<user>/sell', methods=['GET', 'POST'])
def sell_list(user):
    user = models.User.query.filter_by(name=user).first_or_404()
    if user is None:
        flash('User' + user_name + 'not found.')
        return redirect(url_for('index'))
    books = models.Book.query.filter_by(user_id=user.id).all()
    return render_template('sell_book_list.html', user=user, books=books)


@app.route('/<book_id>/buy', methods=['GET', 'POST'])
def buy(book_id):
    book = models.Book.query.filter_by(id=book_id).first_or_404()

    return render_template('buy.html',book=book)






