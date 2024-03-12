from Vehicles import Vehicle

class VehLoc(Vehicle):
    def __init__(self, brand='?', model='?', category='?', seats=0, engine='?', license_plate='?', mileage=0, price=0.0,picture='?',id_agency=0,transmission='?'):
        super().__init__(brand, model, category,transmission, seats, engine, license_plate, id_agency, mileage,picture)
        self.__price = price
        
    def affiche(self):
        super().affiche()
        print(f"Prix : {self.__price}")
    
    def get_license_plate(self):
        return super().get_license_plate()
    
    def get_picture(self):
        return super().get_picture()
    
    def get_brand(self):
        return super().get_brand()
    
    def get_category(self):
        return super().get_category()
    
    def get_engine(self):
        return super().get_engine()
    
    def get_id_agency(self):
        return super().get_id_agency()
    
    def get_mileage(self):
        return super().get_mileage()
    
    def get_model(self):
        return super().get_model()
    
    def get_seats(self):
        return super().get_seats()
    
    def get_transmission(self):
        return super().get_transmission()
      
    def get_price(self):
        return self.__price
        
    def setVehLoc(self, dico):
        super().set_vehicle(dico)
        for key in dico:
            if key=='price':
                self.__price=dico['price']    
    
    def arrival(self, mileage):
        super().set_mileage(mileage)
        
    def affiche(self):
        super().affiche()
        print(f"Prix : {self.__price}")