from Vehicles import *

class Agency:
    def __init__(self,street='?',zip=0,city='?',phone=0, id_agency=-1):
        self.__street=street
        self.__zip=zip
        self.__city=city
        self.__phone=phone
        self.__id_agency=id_agency
        self.__parc=[]
        
    def get_street(self):
        return self.__street
                
    def get_city(self):
        return self.__city

    def get_zip(self):
        return self.__zip

    def get_phone(self):
        return self.__phone
    
    def get_id(self):
        return self.__id_agency

    def get_parc(self):
        return self.__parc
    
    def set_street(self,street):
        self.__street=street
        
    def set_zip(self,zip):
        self.__zip=zip
    
    def set_city(self,city):
        self.__city=city
        
    def set_agency(self,dico):
        for key in dico.keys():
            if key=='street':
                self.__street=dico[key]
            elif key=='zip_code':
                self.__zip=dico[key]
            elif key=='city':
                self.__city=dico[key]
            elif key=='phone':
                self.__phone=dico[key]
            elif key=='id':
                self.__id_agency=dico[key]
                
        
    def set_phone(self,phone):
        self.__phone=phone
    
    def set_id(self,id_agency):
        self.__id_agency=id_agency
 
    def add_vehicle(self, vehicle):
        self.__parc.append(vehicle)
        
    def search_vehicle(self,car):
        for i in self.__parc:
            if i.get_license_plate()==car.get_license_plate():
                return i
        return None
        
    def remove_vehicle(self,vehicle):
        for i in self.__parc:
            if i.get_license_plate()==vehicle.get_license_plate():
                self.__parc.remove(i)
                return True
        return False
    
    def affiche(self):
        print(f"Id : {self.__id_agency}")
        print(f"Adresse : {self.__street} {self.__zip} {self.__city}")
        print(f"Téléphone : {self.__phone}")
        print("Véhicules :")