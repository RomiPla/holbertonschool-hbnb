"""
    Creacion clase review
"""
from basemodel import Basemodel

class Review (Basemodel):
    def __init__(self, Place, User, comment):
        super().__init__()
        self.Place = Place
        self.User = User
        self.comment = comment

"""def add_comment (self, comment):
        self.comment.append(Review)
        
        No va equis de"""


#rev1 = Review(UUID4 place, UUID4 user, "estuvo buena che")