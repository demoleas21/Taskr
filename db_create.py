from src import db
from src.models import Task, User
from datetime import date, datetime

db.create_all()
db.session.add(User('Administrator', 'admin@taskr.com', '123456', 'admin'))
db.session.add(Task('Finish this website', date(2016, 6, 30), 10, datetime.utcnow(), 1, 1))
db.session.add(Task('Finish iOS application', date(2016, 8, 31), 10, datetime.utcnow(), 1, 1))
db.session.commit()
