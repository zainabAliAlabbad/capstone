#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, movie, actor, init_db

assistant='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1Ib0haTEFVNmtVQ1pjTlgwNDZTcCJ9.eyJpc3MiOiJodHRwczovL3phaW4wMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA2NTU1YTYwMWUyYzUwMDY5MjEzOWFkIiwiYXVkIjoiY2FwYXN0b25lQVBJIiwiaWF0IjoxNjE3MzA0MjQ1LCJleHAiOjE2MTczOTA2NDUsImF6cCI6Ing3dlZqZjFCbDk4eE56cDNSZURTeUR5QXptZ3drdlBEIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiXX0.Puqf98XJSWNTcIszhwqluMK2CEZ56W422zEdCD0UhHiQjQC9-lbqpvsGsmdqHLescebIti86OOqqXBbr2AOAJOcWJSG1zT6iSmU0I1ybUywZ32-pPaSmfMjeCia_7Hyjr3HzNhjxGn4i3o7rgT2wdxYfjoSSPX9v_7y1JWolYun_jkhZO4sn2zF0TpiAjVMasR3jWuDWGF-rJGGfPAyktJOZING0sBvGKfgMgmsbOOpYYBLY0j0ObXRi7BBFDWcY0_CYH6NTwd-6y9H9p08Ho_V0KWVWdfnP55mSosHHQZ0ZspXhN9B3E7z3kzYgrX4BMwTc5wfdhaN7SYRDESiTnQ'

director='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1Ib0haTEFVNmtVQ1pjTlgwNDZTcCJ9.eyJpc3MiOiJodHRwczovL3phaW4wMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA2NTU2OWUwMzQ2MjMwMDY5Zjc1Y2IzIiwiYXVkIjoiY2FwYXN0b25lQVBJIiwiaWF0IjoxNjE3MzA0MjQzLCJleHAiOjE2MTczOTA2NDMsImF6cCI6Ing3dlZqZjFCbDk4eE56cDNSZURTeUR5QXptZ3drdlBEIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.oqACKi6qlVPbo7oI4K7ldBpBy1o5sVHOYcWt9QrxfX4Vfaqij3URfSefD64cK8tQM4TCrh631TZ133HDI-nMObbEH_7SuUaeAp2wMnmY3Q2mq87z-FIJG-GnVoT7EbxXvMxT7oNg0S6hxZ0aJXOctYrj5sWfxVPRAdsvqAXrsJ5MqRfAMzw49gBuaJaoYHSL2dM9xnhedq9b0FYACUcgt0A64QYBOOK9L0Y9tZF0EqIt0x7VIZsQr8XgqRZHvw7SWyzolxOScBiFB_ncrKZOSINoP04BKplBOg7NbTIWW2No7NORHwPWEdjba5rh69U0yIo52Br4ni9a91BY8uWfUw'

producer='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1Ib0haTEFVNmtVQ1pjTlgwNDZTcCJ9.eyJpc3MiOiJodHRwczovL3phaW4wMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA2NTU2ZDIwMzQ2MjMwMDY5Zjc1Y2JmIiwiYXVkIjoiY2FwYXN0b25lQVBJIiwiaWF0IjoxNjE3MzA0MjM3LCJleHAiOjE2MTczOTA2MzcsImF6cCI6Ing3dlZqZjFCbDk4eE56cDNSZURTeUR5QXptZ3drdlBEIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.DWhPADzigrCBVTQhrg6QeK3sLq7NJSO8cA6KQXVa-8-Exa_OpCRJwv-CE71nQSDgBO6Kqp0b_U_nl7T0GdkGEUogcqbu4EUrfCM8L2ZHmutNt2EXRccM9tgFPxu7oi9iEorzCuzx0A6tzZiCsOlOMHVe4AKJXlbcuXwN31xwCq98JhcQMXRNd2GOBiKiCOmq5_yXphcEGFjCzi50U3Zj_NvGMXyURHy4ky5j-3p9wNXh0PgV4teRqQnLRgmxxl-ZCDU164IhgFkn9lbabNO5gSL7fT2VEBwe6QbRK1e6Piq7Fvdj6rfMp_KsSLGrlJTwvgM9yHj0CC7eW__OnkrhFg'

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
