"""These are ORM models provided to the blog."""

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from blog_app import db, login_manager


@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    """This class represents User in blog.
    id: is a unique identification of a User in DB, integer, auto increment.
    user_name: string max 30 characters, can be repeated in DB
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(100), nullable=False)

    posts = db.relationship("Posts", back_populates="user")

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return f"{self.user_name}"


class PostsCategory(db.Model):
    """ This class represents Posts categories available in blog.
    category_id: is a unique identification of a Post's Category in DB, integer, auto increment.
    category_name: string, can be repeated in DB
    """
    __tablename__ = "post_category"

    category_id = db.Column(db.Integer, nullable=False, primary_key=True)
    category_name = db.Column(db.String, nullable=False)

    posts = db.relationship("Posts", back_populates="post_category")

    def __repr__(self):
        return f"Post's Category Id #{self.category_id}, Category name {self.category_name}"


tag_posts_relation = db.Table("tags_posts_relation", db.metadata,
                              db.Column("post_id", db.Integer, db.ForeignKey("posts.post_id")),
                              db.Column("tag_id", db.Integer, db.ForeignKey("tags.tag_id"))
                              )

class Posts(db.Model):
    """ This class represents Posts in blog
    post_id: is a unique identification of a Post in DB, integer, auto increment.
    post_date_creation: datetime
    post_reading_time: string
    author_id: integer, relation type with User class one to many
    category_id: integer, relation type with PostsCategory class one to many
    post_title: string, 120 characters max
    post_text: text
    is_post_published: Boolean, False as default value
    posts_claps: integer, amount of "likes" of this post's.

    Posts have a many2many relation with Tags class.
    """
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, nullable=False, primary_key=True)
    post_date_creation = db.Column(db.Date, nullable=False, default=datetime.now())
    post_reading_time = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(PostsCategory.category_id))
    post_title = db.Column(db.String(120), nullable=False)
    short_description = db.Column(db.String(300), default="")
    post_text = db.Column(db.String, nullable=False)
    is_post_published = db.Column(db.Boolean, nullable=False, default=False)
    posts_claps = db.Column(db.Integer, default=0)

    user = db.relationship(User, back_populates="posts", lazy="joined")
    post_category = db.relationship(PostsCategory, back_populates="posts")
    tags = db.relationship("Tags", secondary=tag_posts_relation, back_populates="posts")

    def __repr__(self):
        return f"Post{self.post_id} {self.post_title}"


class Tags(db.Model):
    """ This class represents Tags in blog.
    tag_id: is a unique identification of a Tag in DB, integer, auto increment.
    tag_name: string, 120 characters max
    """
    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, nullable=False, primary_key=True)
    tag_name = db.Column(db.String(120), nullable=False)

    posts = db.relationship(Posts, secondary=tag_posts_relation, back_populates="tags")

    def __repr__(self):
        return f"{self.tag_name}"
