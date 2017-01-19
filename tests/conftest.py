"""Setup testing."""

from main import app, db

app.testing = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db.create_all()
