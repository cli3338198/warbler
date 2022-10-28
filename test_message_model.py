"""Message model tests."""

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



class MessageModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_create_message(self):
        """Test message model works and is created in the database."""

        message = Message(text="TEST", user_id=self.u1_id)

        db.session.add(message)

        self.assertIn(message, Message.query.all())


    # def test_failed_create_message(self):
    #     """Test that invalid message and is not created in the database."""

    #     message = Message(text="123--+", user_id=self.u1_id)

    #     db.session.add(message)

    #     self.assertIn(message, Message.query.all())

    #     # with self.assertRaises(InvalidTextRepresentation):
    #     #         User.signup("u3", "u3@email.com", "", None)