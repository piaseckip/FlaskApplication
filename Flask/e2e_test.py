from website import create_app
from flask import url_for
import os 
import sys
import pytest
import requests
import json

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
def self(app):
    return app.test_client()

def test_home(self):
    response = self.get("/")
    assert b"Welcome" in response.data
    
def test_adding(self):
    with self.app() as client, self.app_context():
        form_data = {'tech_name': 'test_adding', 'tech_descr': 'test', "image_link":'test' }
    response = client.post("/adding",data=json.dumps(form_data))
    self.assertEqual('succesfully ',response.data) 

def test_deleting(self):
    with self.app() as client, self.app_context():
        form_data = {'tech_name': 'test_adding'}
    response = client.post("/deleting",data=json.dumps(form_data))
    self.assertEqual('succesfully',response.data)   
    