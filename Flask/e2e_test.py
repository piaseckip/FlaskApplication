from website import create_app
from flask import url_for
import os 
import sys
import pytest
import requests

@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    ctx = app.app_context()
    ctx.push()
    with ctx:
        pass

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

def test_home(client):
    response = client.get("/")
    assert b"Welcome" in response.data
    
def test_adding(client):
    url = url_for("views.adding")
    form_data = {'tech_name': 'test_adding', 'tech_descr': 'test', "image_link":'test' }
    requests.post(url, data=form_data)
    response = client.get("/")
    assert b"test_adding" in response.data

def test_deleting(client):
    url = url_for("views.deleting")
    form_data = {'tech_name': 'test_adding'}
    requests.post(url, data=form_data)
    response = client.get("/")
    assert b"test_adding" in response.data   
    