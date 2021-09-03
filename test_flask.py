"""Integration test for app.py routes"""

from unittest import TestCase
from app import app
from models import User, Post, Tag, PostTag, db

db.drop_all()
db.create_all()

class BloglyUserTestCase(TestCase):
    """test cases for user routes"""
    
    @classmethod
    def setUp(self):
        """empty tables, set up sample user and post models"""

        PostTag.query.delete()
        Tag.query.delete()
        Post.query.delete()
        User.query.delete()

        test_user = User(first_name='FIRST_NAME',
                         last_name='LAST_NAME',
                         image_url='https://unsplash.com/photos/2LowviVHZ-E')
        
        db.session.add(test_user)
        db.session.commit()

        test_post = Post(title='TITLE',
                         content='CONTENT',
                         user_id=test_user.id)

        db.session.add(test_post)
        db.session.commit()

        test_tag = Tag(name="TAG_NAME")
        
        db.session.add(test_tag)
        db.session.commit()
        
        self.user_id = test_user.id
        self.post_id = test_post.id
        self.tag_id = test_tag.id

    @classmethod
    def tearDown(self):
        """rollback database"""

        db.session.rollback()

    # CREATE

    def test_user_form(self):
        """test new user form page"""
        with app.test_client() as client:
            response = client.get('/users/new')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Add a user</h1>', html)

    def test_submit_user_form(self):
        """test new user form submission"""
        with app.test_client() as client:
            data = {
                "first-name": "FIRST_NAME",
                "last-name": "LAST_NAME",
                "img-url": "https://unsplash.com/photos/2LowviVHZ-E"}

            response = client.post('/users/new', data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("FIRST_NAME LAST_NAME", html)

    def test_post_form(self):
        """test new post form display"""

        with app.test_client() as client:

            response = client.get(f"/users/{self.user_id}/posts/new")
            html = response.get_data(as_text=True)

            user = User.query.get(self.user_id)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f"<h1>Add Post for {user.full_name()}</h1>", html)
    
    def test_post_form_submit(self):
        """test new post submission"""

        with app.test_client() as client:
            data = {
                "title": "TITLE",
                "content": "CONTENT"
            }

            response = client.post(f"/users/{self.user_id}/posts/new", data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("TITLE", html)
    

    # READ

    def test_home(self):
        """test home route"""
        with app.test_client() as client:
            response = client.get('/')

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, 'http://localhost/users')

    def test_user_list(self):
        """test user list home page"""
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
            self.assertIn('FIRST_NAME LAST_NAME', html)
    
    def test_user_profile(self):
        """test user profile display"""
        with app.test_client() as client:
            response = client.get(f"/users/{self.user_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("FIRST_NAME LAST_NAME", html)
            self.assertIn("https://unsplash.com/photos/2LowviVHZ-E", html)

    def test_view_post(self):
        """test post display page"""

        with app.test_client() as client:

            response = client.get(f"/posts/{self.post_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("TITLE", html)
            self.assertIn("CONTENT", html)

    # UPDATE

    def test_edit_user_form(self):
        """test edit form display"""
        with app.test_client() as client:
            response = client.get(f"/users/{self.user_id}/edit")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Edit a user</h1>', html)
    
    def test_submit_user_edit(self):
        """test edit user form submission"""
        with app.test_client() as client:
            data = {
                "first-name": "EDITED_FIRST_NAME",
                "last-name": "EDITED_LAST_NAME",
                "img-url": "https://unsplash.com/photos/Up5a1cLjFPs"}
            
            response = client.post(f"/users/{self.user_id}/edit", data=data)

            user = User.query.get(self.user_id)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, 'http://localhost/users')
            self.assertListEqual(
                [user.full_name(), user.image_url],
                ["EDITED_FIRST_NAME EDITED_LAST_NAME", "https://unsplash.com/photos/Up5a1cLjFPs"])

    def test_edit_post(self):
        """test post edit form display"""

        with app.test_client() as client:

            response = client.get(f"/posts/{self.post_id}/edit")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Edit Post</h1>', html)
        
    def test_submit_post_edit(self):
        """test post edit submission route"""
    
        with app.test_client() as client:

            response = client.post(f"/posts/{self.post_id}/edit", data={
                "title": "EDITED_TITLE",
                "content": "EDITED_CONTENT"
            }, follow_redirects=True)
            
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("EDITED_TITLE", html)
            self.assertIn("EDITED_CONTENT", html)

    # DELETE

    def test_delete_user(self):
        """test user deletion"""
        with app.test_client() as client:
            response = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertNotIn('FIRST_NAME LAST_NAME', html)
            self.assertEqual(Post.query.filter_by(user_id=self.user_id).one_or_none(), None)

    def test_delete_post(self):
        """test post deletion route"""

        with app.test_client() as client:

            response = client.post(f"/posts/{self.post_id}/delete",
                                   follow_redirects=True)

            html = response.get_data(as_text=True)

            deleted_post = Post.query.filter_by(id=self.post_id).one_or_none()

            self.assertEqual(response.status_code, 200)
            self.assertNotIn('TITLE', html)
            self.assertEqual(deleted_post, None)







