
import os
os.environ["DATABASE_URL"] = "postgresql:///blogly_test"
from unittest import TestCase
from app import app, db
from models import User, Post



# DEFAULT_IMAGE

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.session.rollback()

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

        test_post = Post(
            title = 'this is a cool story',
            content = 'best story ever written',
            user_id = self.user_id
        )

        db.session.add(test_post)
        db.session.commit()

        self.post_id = test_post.user_id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_redirect_user_on_edit(self):
        """test redirect, check if username edited"""
        with app.test_client() as c:

            resp = c.post(f"/users/{self.user_id}/edit",
                          data={'first_name': 'Ben',
                                'last_name': 'Last',
                                'image_url': 'literally_anything'},
                          follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertIn('Ben Last', html)

    def test_user_info(self):
        """tests for user info on their page"""

        with app.test_client() as client:
            response = client.get(f'/users/{self.user_id}')
            html = response.get_data(as_text=True)

            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_user_edit(self):
        """tests for edit info on their page"""

        with app.test_client() as client:
            response = client.get(f'/users/{self.user_id}/edit')
            html = response.get_data(as_text=True)

            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_user_create(self):
        """tests for new user page"""

        with app.test_client() as client:
            response = client.get('/users/new')
            html = response.get_data(as_text=True)

            self.assertIn("Create a User", html)

    def test_show_post(self):
        """tests for showing a post"""

        with app.test_client() as client:
            response = client.get(f'/posts/{self.post_id}')
            html = response.get_data(as_text=True)

            self.assertIn("this is a cool story", html)
            self.assertEqual(response.status_code, 200)

    def test_add_post(self):
        """tests for adding a new post"""

        with app.test_client() as client:
            response = client.get(f'/users/{self.user_id}/posts/new')
            html = response.get_data(as_text=True)

            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)
            self.assertEqual(response.status_code, 200)


    def test_delete_button(self):
        """tests for delete button"""

        with app.test_client() as client:
            response = client.post(f'/posts/{self.post_id}/delete',
                                   follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertNotIn("this is a cool story", html)
            self.assertEqual(response.status_code, 200)











