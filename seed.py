"""Seed file to make sample data for pets db."""


from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

ben = User(first_name='Ben', last_name='Briones')
jazz = User(first_name='Jazz', last_name='Cheema')

db.session.add(ben)
db.session.add(jazz)

db.session.commit()
