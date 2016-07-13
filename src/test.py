import os
import unittest
from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'


class AllTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATEBASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
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

    @staticmethod
    def test_users_can_register():
        new_user = User('andrew', 'andrew@taskr.com', '1234')
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

    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_users_can_login(self):
        self.register('Andrew', 'andrew@taskr.com', '1234', '1234')
        response = self.login('Andrew', '1234')
        self.assertIn('Welcome to Taskr', response.data)

    def test_invalid_form_data(self):
        self.register('Andrew', 'andrew@taskr.com', '1234', '1234')
        response = self.login('alert("alert box!");', 'foo')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_user_registration_error(self):
        self.app.get('/register/', follow_redirects=True)
        self.register('Andrew', 'andrew@taskr.com', '1234', '1234')
        self.app.get('/register/', follow_redirects=True)
        response = self.register('Andrew', 'andrew@taskr.com', '1234', '1234')
        print response.data
        self.assertIn(b'That Username and/or email already exist.', response.data)


if __name__ == "__main__":
    unittest.main()
