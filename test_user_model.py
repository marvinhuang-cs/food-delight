# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_model.py

import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, connect_db, User

os.environ['DATABASE_URL'] = "postgresql:///food_delight_test"
from app import app, CURR_USER_KEY

db.create_all()

class UserTestCase(TestCase):
    
    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="beepboop", email="beepboop@", password="beepboop", full_name="beepboop")
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        db.session.commit()