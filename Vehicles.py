class Vehicle():
    def __init__(self, brand='?',category='?', model='?', seats=0, engine='?',transmission='?', license_plate='?',id_agency=0, mileage=0,picture='?'):
        self.__brand = brand
        self.__model = model
        self.__transmission=transmission
        self.__category=category
        self.__seats = seats
        self.__engine = engine
        self.__license_plate = license_plate
        self.__id_agency = id_agency
        self.__mileage = mileage
        self.__picture=picture
        
    def get_transmission(self):
        return self.__transmission
        
    def get_picture(self):
        return self.__picture
    
    def get_brand(self):
        return self.__brand
    
    def get_model(self):
        return self.__model
    
    def get_category(self):
        return self.__category
    
    def get_seats(self):
        return self.__seats
    
    def get_engine(self):
        return self.__engine
    
    def get_license_plate(self):
        return self.__license_plate
    
    def get_id_agency(self):
        return self.__id_agency
    
    def get_mileage(self):
        return self.__mileage
     
    def set_vehicle(self,dico):
        for key in dico:
            if key=='brand':
                self.__brand=dico['brand']
            elif key=='model':
                self.__model=dico['model']
            elif key=='category':
                self.__category=dico['category']
            elif key=='seats':
                self.__seats=dico['seats']
            elif key=='engine':
                self.__engine=dico['engine']
            elif key=='license_plate':
                self.__license_plate=dico['license_plate']
            elif key=='mileage':
                self.__mileage=dico['mileage']
            elif key=='id_agency':
                self.__id_agency=dico['id_agency']
            elif key=='picture':
                self.__picture=dico['picture']
            elif key=='transmission':
                self.__transmission=dico['transmission']
                
    def set_mileage(self,mileage):
        self.__mileage=mileage

    def affiche(self):
        print(f"Marque : {self.__brand}")
        print(f"Modèle : {self.__model}")
        print(f"Catégorie : {self.__category}")
        print(f"Transmission : {self.__transmission}")
        print(f"Nombre de places : {self.__seats}")
        print(f"Moteur : {self.__engine}")
        print(f"Immatriculation : {self.__license_plate}")
        print(f"Agence : {self.__id_agency}")
        print(f"Kilométrage : {self.__mileage}")
        print(f"Photo : {self.__picture}")
                                
    
    

            

            
