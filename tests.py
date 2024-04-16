from unittest import TestCase

from app import app
from models import db, Cupcake

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

with app.app_context():
    db.drop_all()
    db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Set up test data within an application context."""
        with app.app_context():
            Cupcake.query.delete()
            db.session.commit()
            cupcake = Cupcake(**CUPCAKE_DATA)
            db.session.add(cupcake)
            db.session.commit()
            db.session.refresh(cupcake)
            self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""
        with app.app_context():
            db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")
            self.assertEqual(resp.status_code, 200)
            data = resp.get_json()
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_get_cupcake_missing(self):
        with app.test_client() as client:
            url = "/api/cupcakes/99999"
            resp = client.get(url)
            self.assertEqual(resp.status_code, 404)

    def test_create_cupcake(self):
        with app.test_client() as client:
            resp = client.post("/api/cupcakes", json=CUPCAKE_DATA_2)
            self.assertEqual(resp.status_code, 201)
            data = resp.get_json()
            self.assertIsInstance(data['cupcake']['id'], int)
            self.assertEqual(data['cupcake']['flavor'], 'TestFlavor2')

    def test_update_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.patch(url, json={"flavor": "UpdatedFlavor", "size": "medium", "rating": 8, "image": "http://new-image.com"})
            self.assertEqual(resp.status_code, 200)
            data = resp.get_json()
            self.assertEqual(data['cupcake']['flavor'], 'UpdatedFlavor')

    def test_update_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.patch(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 1)

    def test_delete_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.delete(url)
            self.assertEqual(resp.status_code, 200)
            data = resp.get_json()
            self.assertEqual(data['message'], "Deleted")

    def test_delete_cupcake_missing(self):
        with app.test_client() as client:
            url = "/api/cupcakes/99999"
            resp = client.delete(url)
            self.assertEqual(resp.status_code, 404)

if __name__ == "__main__":
    with app.app_context():
        unittest.main()
