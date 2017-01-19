from os import urandom
from urllib.parse import urljoin
from attrs_sqlalchemy import attrs_sqlalchemy
from flask import Flask, render_template, request, flash, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, validators

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(64)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@attrs_sqlalchemy
class URL(db.Model):
    """A URL."""
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), unique=True)


class URLForm(FlaskForm):
    """Add a URL to the database."""
    url = StringField(
        'URL',
        [validators.Length(min=10, max=URL.__table__.c['url'].type.length)]
    )


@app.route('/', methods=['GET', 'POST'])
def index():
    """The home page."""
    url_id = None
    form = URLForm()
    if request.method == "POST":
        if form.validate_on_submit():
            url = form.data['url']
            q = URL.query.filter_by(url=url)
            if q.count():
                url_id = q.first().id
            else:
                u = URL(url=url)
                db.session.add(u)
                db.session.commit()
                url_id = u.id
        else:
            flash('You must specify a URL.')
    return render_template(
        'index.html',
        form=form,
        url_id=url_id,
        urljoin=urljoin
    )


@app.route('/<int:id>')
def url_route(id):
    """Get a URL."""
    q = URL.query.filter_by(id=id)
    if q.count():
        return redirect(q.first().url)
    else:
        abort(404)


if __name__ == '__main__':
    db.create_all()
    app.run()
