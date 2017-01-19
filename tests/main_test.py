"""Test everything."""

from flask import request
from main import app, URL, db

client = app.test_client()


def test_testing():
    assert app.testing is True


def test_db():
    assert db.engine.url.database == ':memory:'


def test_home():
    assert isinstance(client.get(path='/').data, bytes)
    assert URL.query.count() == 0


def test_not_found():
    assert client.get('/localhost').status_code == 404


def test_add():
    hostname = 'http://localhost'
    response = client.post(path='/', data={'url': hostname})
    assert b'<p>Your URL is <a href="' in response.data
    assert URL.query.filter_by(url=hostname).count() == 1
