#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, movie, actor, init_db

assistant='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1Ib0haTEFVNmtVQ1pjTlgwNDZTcCJ9.eyJpc3MiOiJodHRwczovL3phaW4wMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA2MTg0NjRmYjc3NDIwMDY5ODQzY2Q1IiwiYXVkIjoiY2FwYXN0b25lQVBJIiwiaWF0IjoxNjE3MjAyNjUwLCJleHAiOjE2MTcyMDk4NTAsImF6cCI6Ing3dlZqZjFCbDk4eE56cDNSZURTeUR5QXptZ3drdlBEIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiXX0.KGbAd8_C3uZ9KlBqgAxTOdFDgvrMCTOTkY6e0kFXhVQwTmnmGpyYVvOAGzpeLA0O8UDTo2HF7NrWJXVAGGcr5YMYryyVfjMEuby59tlgDXwllsi7ZSViywT-KruGGYN5CvIQDpIXuw0pQXkfdO237HPhF6zXwqBJlY8MCP5XLc455Yz-L6Q5v2YcJfoJ8Mu5N-tof7Zs4rDtB0wSofxs_UAX9isJMj4hbRUCRKeJ2_89lQnAQ4zBlfvRbBLbS02UXlktx5sOyQn28EcMBUjmzlkjPnCJ_Z4KMU92e1LFZJqKyFVrFcpulSOkyfDAOnBtYnPw0JUZ399fapMfASa2cg'

director='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1Ib0haTEFVNmtVQ1pjTlgwNDZTcCJ9.eyJpc3MiOiJodHRwczovL3phaW4wMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA2MmM3ZjFhYTI5NGEwMDY5YTYwMjc4IiwiYXVkIjoiY2FwYXN0b25lQVBJIiwiaWF0IjoxNjE3MjAyNDczLCJleHAiOjE2MTcyMDk2NzMsImF6cCI6Ing3dlZqZjFCbDk4eE56cDNSZURTeUR5QXptZ3drdlBEIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.jBqm8A6HADnVL6EDdnrkyzkY6kUf3OAQKcP6DYCl-2YFIDIEwYITcoLhYcYrWGyt77gemd0uYjrVya7AIUO21e99RdBZbaZg1UmwYaUcvxBlUhadr0qXmuP6QX2_f63JuTg312ljqHPLe_EC6AKl8L7irUFByOePFXi8EjQ8u6QbxNbIgmtLUVYwjIqzkE3X5LVCILTfBmYlFELRzXUJNDGrkfjF-ai0nPu7JqbPMwfXT4LRA92CqH0A2CL6U8KS-DzUWktoQnPKFOeG6FVeE3_ECcR3VD-JSndmVlYyEtRAXWp6nleZVCOF_Qt8n8KkRiQXLMuMS7RWzLza8XTeXQ'

producer='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1Ib0haTEFVNmtVQ1pjTlgwNDZTcCJ9.eyJpc3MiOiJodHRwczovL3phaW4wMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxNTUzYjAzNDAyODUwMDcxNjBlZWIyIiwiYXVkIjoiY2FwYXN0b25lQVBJIiwiaWF0IjoxNjE3MjAyMDk0LCJleHAiOjE2MTcyMDkyOTQsImF6cCI6Ing3dlZqZjFCbDk4eE56cDNSZURTeUR5QXptZ3drdlBEIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.KPPWvdsiOPK3Ww0u0Qv23qwpD1wiCWkkWMe94DGFbXiaX_wMS_VqP9JVdWaNy-nSIOQ7PZybiScSmx0VF7-24t8RVoRg6d-ds1oftIl0FtbWUFm7gTrN9s0tWf_2muq36saWOAMlK7bj6_BxEqyzKCEz1SGr0TnJj1wwtTlT2QsU4SEuT1ytCeh0AMYLwfWfVn8PB2_Pth-IXM3rAtFQDTEYKVz7xV-Xi39Z4idY4sE7bwvwGsG_Uhzezty3dkW7BZQFkklSvEcck8DvbkIDF9pOQ5-VohMDD6w1GWsoggobjBrh0Wb80xGEDg4e75iQFYCpUp5OGNmJ8c-HhQLBGQ'

unath = {'code': 'unauthorized', 'description': 'Permission not authorized.'}


class AppTest(unittest.TestCase):
    """Setup test suite for the routes"""

    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = 'postgresql://postgres:A1b2c3d4@localhost:5432/capstone-project'
        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after each test"""
        pass

#  Movie Tests

    def test_get_all_movies(self):
        response = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + assistant})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movie_byID(self):

        mov = movie(title='capstone', genres='Drama',
                    year='2021')
        mov.insert()
        movie_id = mov.id

        response = self.client().get(
            f'/movies/{movie_id}',
            headers={"Authorization": "Bearer " + assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies'], mov.format())

    def test_404_get_movie_byID(self):
        response = self.client().get(
            '/movies/1000',
            headers={"Authorization": "Bearer " + assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_post_movie(self):
        new_movie = {
            'title': 'capstone',
            'genres': 'Drama',
            'year': '2021'
        }

        mov = movie(title='capstone', genres='Drama', year='2021')
        response = self.client().post(
            '/movies',
            headers={"Authorization": " Bearer " + producer}, json=new_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'added Successfully')

    def test_422_post_movie(self):
        new_movie = {
            'title': 'capstone'
        }
        response = self.client().post(
            '/movies',
            headers={"Authorization": " Bearer " + producer}, json=new_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_Unauth_post_movie(self):

        new_movie = {
            'title': 'capstone',
            'genres': 'Drama',
            'year': '2021'
        }
        response = self.client().post(
            '/movies',
            headers={"Authorization": " Bearer " + director}, json=new_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], unath)

    def test_patch_movie(self):

        mov = movie(title='capstone', genres='Drama',
                    year='2021')
        mov.insert()
        movie_id = mov.id

        edit_movie = {
            'title': 'capstone2',
            'genres': 'comedy',
            'year': '2022'
        }
        response = self.client().patch(
            f'/movies/{movie_id }',
            headers={"Authorization": " Bearer " + producer}, json=edit_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Updated Successfully')
        self.assertEqual(data['movie'], mov.format())

    def test_404_patch_movie(self):

        edit_movie = {
            'title': 'capstone2',
            'genres': 'comedy',
            'year': '2022'
        }
        response = self.client().patch(
            '/movies/1800',
            headers={"Authorization": " Bearer " + producer}, json=edit_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_movie(self):

        mov = movie(title='capstone', genres='Drama',
                    year='2021')
        mov.insert()
        movie_id = mov.id

        response = self.client().delete(
            f'/movies/{movie_id }',
            headers={"Authorization": " Bearer " + producer}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Deleted Successfully')
        self.assertEqual(data['movie'], mov.title)

    def test_404_delete_movie(self):

        response = self.client().delete(
            f'/movies/50',
            headers={"Authorization": " Bearer " + producer}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_Unauth_delete_movie(self):

        response = self.client().delete(
            '/movies/50',
            headers={"Authorization": " Bearer " + director}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], unath)

    # Actors Test

    def test_get_all_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + assistant})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actor_byID(self):

        act = actor(name='name', age=50,
                    gender='male')
        act.insert()
        actor_id = act.id

        response = self.client().get(
            f'/actors/{actor_id}',
            headers={"Authorization": "Bearer " + assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors'], act.format())

    def test_404_get_actor_byID(self):
        response = self.client().get(
            '/actors/1000',
            headers={"Authorization": "Bearer " + assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_post_actor(self):
        new_actor = {
            'name': 'name',
            'age': 50,
            'gender': 'male'
        }

        act = actor(name='name', age=50, gender='male')
        response = self.client().post(
            '/actors',
            headers={"Authorization": " Bearer " + producer}, json=new_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'added Successfully')

    def test_422_post_actor(self):
        new_actor = {
            'age': 54
        }
        response = self.client().post(
            '/actors',
            headers={"Authorization": " Bearer " + producer}, json=new_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_Unauth_post_actor(self):

        new_actor = {
            'name': 'name',
            'age': 50,
            'gender': 'male'
        }
        response = self.client().post(
            '/actors',
            headers={"Authorization": " Bearer " + assistant}, json=new_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], unath)

    def test_patch_actor(self):

        act = actor(name='name', age=50,
                    gender='male')
        act.insert()
        actor_id = act.id

        edit_actor = {
            'name': 'name2',
            'age': 34,
            'gender': 'Female'
        }
        response = self.client().patch(
            f'/actors/{actor_id }',
            headers={"Authorization": " Bearer " + producer}, json=edit_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Updated Successfully')
        self.assertEqual(data['actor'], act.format())

    def test_404_patch_actor(self):

        edit_actor = {
            'name': 'name2',
            'age': 34,
            'gender': 'Female'
        }
        response = self.client().patch(
            '/actors/1800',
            headers={"Authorization": " Bearer " + producer}, json=edit_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_actor(self):

        act = actor(name='name', age=50,
                    gender='male')
        act.insert()
        actor_id = act.id

        response = self.client().delete(
            f'/actors/{actor_id}',
            headers={"Authorization": " Bearer " + producer}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Deleted Successfully')
        self.assertEqual(data['actor'], act.name)

    def test_404_delete_actor(self):

        response = self.client().delete(
            f'/actors/20',
            headers={"Authorization": " Bearer " + producer}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_Unauth_delete_actor(self):

        act = actor(name='name', age=50,
                    gender='male')
        act.insert()
        actor_id = act.id

        response = self.client().delete(
            '/actors/50',
            headers={"Authorization": " Bearer " + assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], unath)


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
