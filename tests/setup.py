import pytest
from app import create_app, db
from config import TestConfig


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()



# import config
# import unittest
# from app import create_app, db
#
#
# class TestConfig(config.Config):
#     Testing = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
#
#
# class SetupTestSuite(unittest.TestCase):
#
#     def setUp(self):
#         self.app = create_app(TestConfig)
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()
#
#     def tearDown(self) -> None:
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()
