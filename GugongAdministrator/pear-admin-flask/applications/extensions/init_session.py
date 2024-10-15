from flask_session import Session

sess = Session()


def init_session(app):
    sess.init_app(app)