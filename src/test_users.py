import os
import unittest
from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'


class UsersTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name, password=password
        ), follow_redirects=True)

    def register(self, name, email, password, confirm):
        return self.app.post('register/', data=dict(
            name=name, email=email, password=password, confirm=confirm
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    @staticmethod
    def create_user(name, email, password):
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def test_users_can_register():
        new_user = User('andrew', 'andrew@taskr.com', '123456')
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == "andrew"

    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login to access your task list.', response.data)

    def test_users_can_login(self):
        self.register('Andrew', 'andrew@taskr.com', '123456', '123456')
        response = self.login('Andrew', '123456')
        self.assertIn(b'Welcome!', response.data)

    def test_invalid_form_data(self):
        self.register('Andrew', 'andrew@taskr.com', '123456', '123456')
        response = self.login('alert("alert box!");', 'foo')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access the task list.', response.data)

    def test_user_registration(self):
        self.app.get('register/', follow_redirects=True)
        response = self.register('Andrew', 'andrew@taskr.com', '123456', '123456')
        self.assertIn(b'Thanks for registering. Please login.', response.data)

    def test_user_registration_error(self):
        self.app.get('register/', follow_redirects=True)
        self.register('Andrew', 'andrew@taskr.com', '123456', '123456')
        self.app.get('register/', follow_redirects=True)
        response = self.register('Andrew', 'andrew@taskr.com', '123456', '123456')
        self.assertIn(b'That username and/or email already exists.', response.data)

    def test_logged_in_users_can_logout(self):
        self.register('Andrew', 'andrew@taskr.com', '123456', '123456')
        self.login('Andrew', '123456')
        response = self.logout()
        self.assertIn(b'Goodbye!', response.data)

    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b'Goodbye!', response.data)