from models import db
from app import app

# create tables
db.drop_all()
db.create_all()