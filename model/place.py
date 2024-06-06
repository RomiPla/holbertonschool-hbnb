class Place:
    def __init__(self, name, description, number_of_rooms, number_of_bathrooms, max_guests, price_by_nigth, latitude, longitude, city_id):
        self.name = name
        self.description = description
        self.number_of_rooms = number_of_rooms 
        self.number_of_bathrooms = number_of_bathrooms
        self.max_guests = max_guests
        self.price_by_night = price_by_nigth
        self.latitude = latitude
        self.longitude = longitude
        self.city_id = city_id
        amenity_ids = []