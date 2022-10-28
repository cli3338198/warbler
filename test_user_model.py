"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows, connect_db

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

connect_db(app)

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)

    # Does the repr method work as expected?
    def test_user_repr(self):
        """Test the repr method."""
        u1 = User.query.get(self.u1_id)

        self.assertEqual(
            repr(u1),
            f"<User #{self.u1_id}: u1, u1@email.com>")

        self.assertEqual(
            repr(User.query.get(self.u1_id)),
            f"<User #{self.u1_id}: u1, u1@email.com>")

    # Does is_following successfully detect when user1 is following user2?
    def test_user_is_following(self):
        """Test the is_following method."""

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.followers.append(u2)

        self.assertTrue(u2.is_following(u1))


    # Does is_following successfully detect when user1 is not following user2?
    def test_user_is_not_following(self):
        """Test the is_following method."""

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u2.followers.append(u1)

        self.assertFalse(u2.is_following(u1))

    # Does is_followed_by successfully detect when user1 is followed by user2?
    def test_user_is_followed_by(self):
        """Test if is_followed detects when user1 is followed by user2"""

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.followers.append(u2)

        self.assertTrue(u1.is_followed_by(u2))

    # Does is_followed_by successfully detect when user1 is not followed by user2?
    def test_user_is_followed_by_false(self):
        """Test when user1 is not followed by user2"""

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        self.assertFalse(u1.is_followed_by(u2))

    # Does User.signup successfully create a new user given valid credentials?
    def test_user_signup(self):
        """Test the user signup successful if given valid credentials.
            check that user is in database
        """

        user = User.signup("u3", "u3@email.com", "password", None)

        user_in_db = User.query.filter(User.email == 'u3@gmail.com')

        self.assertEqual(repr(user), f"<User #{user.id}: u3, u3@email.com>")
        self.assertTrue(bool(user_in_db))

    # Does User.signup fail to create a new user if any of the validations (eg uniqueness, non-nullable fields) fail?
    def test_user_signup_fail(self):
        """Test the user signup fail if any invalid data.
            check new user not in database
        """

        with self.assertRaises(ValueError):
            User.signup("u3", "u3@email.com", "", None)

    # Does User.authenticate successfully return a user when given a valid username and password?
    def test_authenticate_user(self):
        """Test if user is returned being given a valid username and password.
        """

        User.signup("testname", "u3@email.com", "password", None)

        user = User.authenticate("testname", "password")

        self.assertTrue(user)

    # Does User.authenticate fail to return a user when the username is invalid?
    def test_authenticate_username_invalid(self):
        """Test if False is returned if invalid username is given.
        """

        User.signup("testname", "u3@email.com", "password", None)
        user = User.authenticate("", password="password")

        self.assertFalse(user)

    # Does User.authenticate fail to return a user when the password is invalid?
    def test_authenticate_password_invalid(self):
        """Test if False is returned if invalid password is given.
        """

        User.signup("testname", "u3@email.com", "password", None)
        user = User.authenticate("", password="paxxword")

        self.assertFalse(user)