import os





from unittest import TestCase
#from sqlalchemy import exc

from app import app

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

from models import db,User,Message,Follows,Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

db.create_all()

class UserModelTestCase(TestCase): 
    def setUp(self):
        db.drop_all()
        db.create_all()

        self.uid = 9888
        u = User.signup("xinjuanTesting","dengxinjuan@gmail.com","123456",None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)
        self.client = app.test_client()
    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    



