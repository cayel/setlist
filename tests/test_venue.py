import unittest
from venue import Venue

class TestVenue(unittest.TestCase):
    def test_venue_initialization(self):
        venue = Venue(1, "Madison Square Garden", 100)
        self.assertEqual(venue.id, 1)
        self.assertEqual(venue.name, "Madison Square Garden")
        self.assertEqual(venue.cityId, 100)

    def test_to_dict(self):
        venue = Venue(1, "Madison Square Garden", 100)
        expected_dict = {
            'id': 1,
            'name': "Madison Square Garden",
            'cityId': 100
        }
        self.assertEqual(venue.to_dict(), expected_dict)

if __name__ == '__main__':
    unittest.main()