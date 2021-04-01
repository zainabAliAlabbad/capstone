#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, movie, actor, init_db

assistant='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1Ib0haTEFVNmtVQ1pjTlgwNDZTcCJ9.eyJpc3MiOiJodHRwczovL3phaW4wMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA2NTU1YTYwMWUyYzUwMDY5MjEzOWFkIiwiYXVkIjoiY2FwYXN0b25lQVBJIiwiaWF0IjoxNjE3MjU0NzQzLCJleHAiOjE2MTcyNjE5NDMsImF6cCI6Ing3dlZqZjFCbDk4eE56cDNSZURTeUR5QXptZ3drdlBEIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiXX0.jDVFCu1eunRqG0hrXYHLurA8pBz2XK4X11SKbc_r_D-uv-3Zjnm3bdzdO8xYPpfKBJhhlh9lkwmQuyU8vJJ-ORyel8u0XzDPHRBUck7LuuAp6xlPHNIkQuJuth9QS6XYsD82rfHUN2zzM5PCjW3ZoYYjhDS8srkfqsEpQbeutgSQz9EK-al8nLxvzjjDjUONSafJNkEdDyWi63vOZlneeL8Swm93H86d2UOqmf8dEkbXrv6ugejjA0P8u4czsNdWjVmBH9hXu02L1g3LkesgI8RpR0pVUlYUIX_n2etB2G31yDzuPC-blbhC0R9pKrNWhwPaPwVe-Fi32sNDTZmtyg'

director='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1Ib0haTEFVNmtVQ1pjTlgwNDZTcCJ9.eyJpc3MiOiJodHRwczovL3phaW4wMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA2NTU2OWUwMzQ2MjMwMDY5Zjc1Y2IzIiwiYXVkIjoiY2FwYXN0b25lQVBJIiwiaWF0IjoxNjE3MjU0NzQxLCJleHAiOjE2MTcyNjE5NDEsImF6cCI6Ing3dlZqZjFCbDk4eE56cDNSZURTeUR5QXptZ3drdlBEIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.JmwEQQnN7bsASF5kLiFIcy5vwRAeVzDWsABesZi1w8ggge3ZcnSD8p-rQ144dnh54g78q1VuYf4a5m0Lc0Ud_6dFGg6aW7Ixb2J6tuGF0Tw9NThsQfLnXED7VaycqLhPLdVa4XZCeEVcBIEzn_eTk6Kze9EOwgCetDgALuGtkggW0AqxzMw97bS9XEf6Qs0jfNf9OmW6LnLPYcPU0Zns_Zs_jZFBNWPqOzG2q9UlWLd7x4yE6YngfcVgouEs7e-O90izvkeEaX62fYenXuP5eXJ2dXXwNh02YQvtgUnEvFR-hX3kc44XEGkzsssiOrd1wkzdPn6RSPldz_8vSGYZRQ'

producer='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1Ib0haTEFVNmtVQ1pjTlgwNDZTcCJ9.eyJpc3MiOiJodHRwczovL3phaW4wMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA2NTU2ZDIwMzQ2MjMwMDY5Zjc1Y2JmIiwiYXVkIjoiY2FwYXN0b25lQVBJIiwiaWF0IjoxNjE3MjU0NzM5LCJleHAiOjE2MTcyNjE5MzksImF6cCI6Ing3dlZqZjFCbDk4eE56cDNSZURTeUR5QXptZ3drdlBEIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.nAiT17tGzRRYpcPXAEuwnGqHL6Rhd_d2LmL6G7oe9PGFzuxHR-2vZX6t-Trmcq_dje6T7nzHabvYZa6lkb7a09PA5DQvs2w0I6wpJSax7Jxdyf_OsNIfKttyAaIHBE6sKj99cTXl_h7iUt0QzQMiGX0uOy1jb_66qVzAwIt8VLXppWlzaLDpxQhJPgLQC-T16fo0mdGV1hKE0LGwywkG7A5kiVuO6wnQpmuqf2RVwPWO4xJ6fyHBsCgHh5eqrp_4vmPjxoTO13S4z5SEm2zwo4Gj_50xl2Hi237SEOD8AezN24PMna6trNLsHBtlMN7lRb63UBzhTe9N2EkwLqzyTg'

unath = {'code': 'unauthorized', 'description': 'Permission not authorized.'}


class AppTest(unittest.TestCase):
    """Setup test suite for the routes"""

    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone-test"
        self.database_path = 'postgresql://postgres:A1b2c3d4@localhost:5432/capstone-test'
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
