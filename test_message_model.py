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

    def test_message_model(self):
        """test message model"""
        msg = Message(
            text="first message",
            user_id = self.uid
        )

        db.session.add(msg)
        db.session.commit()

        self.assertEqual(len(self.u.messages),1)
        self.assertEqual(self.u.messages[0].text,"first message")
    
    def test_message_likes(self):
        """test message like function"""
        msg1 = Message(
            text="first message",
            user_id = self.uid
        )

        msg2 = Message(
            text="second message",
            user_id=self.uid
        )

        user = User.signup("dengxinjuan","dengxinj@gmail.com","12345",None)
        uid = 19888
        user.id = uid
        db.session.add_all([msg1,msg2,user])
        db.session.commit()

        user.likes.append(msg1)

        db.session.commit()
        
        l = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(l),1)
        self.assertEqual(l[0].message_id,msg1.id)




    
