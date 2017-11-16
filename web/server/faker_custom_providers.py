from faker import Faker
fake = Faker()

# first, import a similar Provider or use the default one
from faker.providers import BaseProvider

# create new provider class
class CarsProvider(BaseProvider):
    def __init__(self, other):
        super().__init__(other)
        self.__carmakesmodels = {
            'VW':['Jetta', 'Golf', 'Passat','Beetle'],
            'Toyota':['Corolla', 'Celica', 'Camry', 'Prius'],
            'Honda':['Civic', 'Accord', 'City', '2000'],
            'Nissan':['Sentra', 'Altima', '370Z', 'Frontier']
        }
        self.__carmakes = self.__carmakesmodels.keys()

    def car_make(self):
        return fake.random_element(self.__carmakes)

    def car_model(self,make=None):
        if(make):
            return fake.random_element(self.__carmakesmodels[make])
        # choose a random model from a random make
        return fake.random_element(self.__carmakesmodels[self.car_make()])

class ServicesProvider(BaseProvider):
    def __init__(self, other):
        super().__init__(other)
        self.__types = [
            'car share', 
            'house share', 
            'other service type'
            ]
        self.__perks = [
            'first 60 mi free',
            '50% discount after 120 mi',
            '1 day free after 3 days',
            'hotel 50% off after a week'
            ]
        
    def service_type(self):
        return fake.random_element(self.__types)

    def service_perks(self):
        return fake.random_element(self.__perks)

class TripsProvider(BaseProvider):
    def __init__(self, other):
        super().__init__(other)
        self.__highlights = [
            'I can kiss you as much you want.',
            'Trip Highligh 2',
            'Trip Highligh 3'
            ]
    
    def trip_highligh(self):
        return fake.random_element(self.__highlights)


# then add new provider to faker instance
fake.add_provider(CarsProvider)
fake.add_provider(ServicesProvider)
fake.add_provider(TripsProvider)