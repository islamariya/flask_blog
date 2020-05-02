from blog_app import db, app
import view


if __name__ == "__main__":
    db.create_all()
    app.run()
