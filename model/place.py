from basemodel import Basemodel
from user import User

class Place(Basemodel):
    def __init__(self, host_id, name, description, number_of_rooms, number_of_bathrooms,\
                 max_guests, price_by_nigth, latitude, longitude, City):
        super().__init__()
        if host_id not in User.user_emails:
            raise ValueError(f"Host with id {host_id} does not exist.")
        self.name = name
        self.description = description
        self.number_of_rooms = number_of_rooms 
        self.number_of_bathrooms = number_of_bathrooms
        self.max_guests = max_guests
        self.price_by_night = price_by_nigth
        self.latitude = latitude
        self.longitude = longitude
        self.City = City
        self.amenities = []
        self.reviews = []
    
    def add_amenity(self, Amenity):
        self.amenities.append(Amenity)
    
    def add_review(self, Review):
        self.reviews.append(Review)


casitapro = Place(casitgg, casitagg2, 5, 2, 999, 999, lat, long, City)

casitapro.add_amenity("wifi")

print(casitapro.amenities)