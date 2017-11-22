#coding:utf-8
from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired, length, Email, equal_to


class LoginForm(Form):
    email = StringField('email', validators=[DataRequired(message=u"邮箱不能为空"), Email(message=u"邮箱格式不正确")],
                        render_kw={"placeholder": u"   邮箱", "style": "height: 35px"})
    remember_me = BooleanField('remember_me', default=False)
    password = PasswordField('password', validators=[DataRequired(message=u"密码不能为空"),
                                                     length(5, 12, message=u"密码长度5至12位")],
                             render_kw={"placeholder": u"   密码", "style": "height: 35px "})


class RegisterForm(Form):
    name = StringField('name', validators=[DataRequired(message=u"昵称不能为空"), length(max=24, message=u"昵称长度不超过24个字符")],
                       render_kw={"placeholder": u"   昵称", "style": "height: 35px"})
    password = PasswordField('password', validators=[DataRequired(message=u"密码不能为空"),
                                                     length(5, 12, message=u"密码长度5至12位")],
                             render_kw={"placeholder": u"   密码", "style": "height: 35px "})
    password_again = PasswordField("password", validators=[DataRequired(message=u"请在输入一次您的密码"),
                                                           length(5, 12, message=u"密码长度5至12位"),
                                                           equal_to("password", message=u"两次密码不一致")],
                                   render_kw={"placeholder": u"   请再次输入您的密码", "style": "height: 35px"})
    email = StringField('email', validators=[DataRequired(message=u"邮箱不能为空"), Email(message=u"邮箱格式不正确")],
                        render_kw={"placeholder": u"   邮箱", "style": "height: 35px "})
    job = SelectField('job', choices=[(u"本科生", u"本科生"), ( u"研究生", u"研究生"), (u"教师", u"教师"),
                                      (u"已就业", u"已就业"), (u"其他", u"其他")],
                      render_kw={"style": "height: 35px; width: 321px"}, default=u"本科生")


class RetrieveForm(Form):
    email = StringField('email', validators=[DataRequired(message=u"邮箱不能为空"), Email(message=u"邮箱格式不正确")],
                        render_kw={"placeholder": u"   邮箱", "style": "height: 35px "})


class PasswordForm(Form):
    password = PasswordField('password', validators=[DataRequired(message=u"密码不能为空"),
                                                     length(5, 12, message=u"密码长度5至12位")],
                             render_kw={"placeholder": u"   密码", "style": "height: 35px "})
    password_again = PasswordField("password", validators=[DataRequired(message=u"请在输入一次您的密码"),
                                                           length(5, 12, message=u"密码长度5至12位"),
                                                           equal_to("password", message=u"两次密码不一致")],
                                   render_kw={"placeholder": u"   请再次输入您的密码", "style": "height: 35px"})
    flag = BooleanField('flag', default=False)

class EditForm(Form):
    about_me = TextAreaField('about_me', validators=[length(min=0, max=140)])


class SellBookForm(Form):
    title = StringField('title', validators=[DataRequired(), length(min=0, max=40)])
    info = TextAreaField('info', validators=[length(min=0, max=80)])
    file = FileField('file', validators=[DataRequired()])
