from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from admin import app, session
from blog_app import login_manager
from config import POSTS_PER_PAGE
import forms
import models


# user's block
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if current_user.is_authenticated:
        return redirect("index_page")
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        email = form.email.data
        password = form.password.data
        try:
            new_user = models.User(user_name=user_name, email=email, password_hash=password)
            new_user.set_password_hash(password)
            session.add(new_user)
            session.commit()
        except:
            print("Ошибка добавления в БД")
        flash("Вы успешно зарегистрированы", "success")
        return redirect(url_for("index_page"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index_page'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(user_name=form.user_name.data).first_or_404()
        if user is None or not user.check_password(form.password.data):
            flash("Неверный пароль или пользователь не найден")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index_page")
        return redirect(next_page)
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index_page'))



@app.route("/")
@app.route("/all_posts", methods=["GET"])
@app.route("/all_posts/page/<int:page>")
def index_page(page=1):
    posts = models.Posts.query.filter_by(is_post_published=True).\
        order_by(models.Posts.post_date_creation.desc()).paginate(page,POSTS_PER_PAGE, False)
    return render_template("index.html", posts=posts)


# content block
@app.route("/posts/<int:post_id>", methods=["GET"])
def post_detail(post_id):
    post = models.Posts.query.filter_by(post_id=post_id).first_or_404()
    return render_template("post_detail.html", post=post)


@app.route("/posts/category/<int:category_id>", methods=["GET"])
def all_posts_by_category(category_id, page=1):
    all_posts = models.Posts.query.filter(models.Posts.category_id == category_id).order_by(
        models.Posts.post_date_creation.desc()).paginate(page,POSTS_PER_PAGE, False)
    return render_template("index.html", posts=all_posts)


@app.route("/posts_by_tags/<int:tag_id>")
def posts_by_tag(tag_id, page=1):
    all_posts = models.Posts.query.filter(models.Posts.tags.any(tag_id=tag_id)).order_by(
        models.Posts.post_date_creation.desc()).paginate(page,POSTS_PER_PAGE, False)
    return render_template("index.html", posts=all_posts)


@app.route("/posts_by_user/<int:user_id>")
def posts_by_user(user_id, page=1):
    all_posts = models.Posts.query.filter_by(author_id=user_id).order_by(
        models.Posts.post_date_creation.desc()).paginate(page,POSTS_PER_PAGE, False)
    print(all_posts)
    return render_template("index.html", posts=all_posts)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
