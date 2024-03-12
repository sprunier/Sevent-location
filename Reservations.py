class Reservation():
    def __init__(self, startdate='?',enddate='?', Vehicle='?', Agency='?', User='?', id=-1):
        self.__startdate = startdate
        self.__enddate = enddate
        self.__vehicle = Vehicle
        self.__agency = Agency
        self.__user = User
        self.__id = id
    
    def get_id(self):
        return self.__id

    def get_startdate(self):
        return self.__startdate
    
    def get_enddate(self):
        return self.__enddate
    
    def get_Vehicle(self):
        return self.__vehicle
    
    def get_Agency(self):
        return self.__agency
    
    def get_User(self):
        return self.__user
    
    def set_id(self, id):
        self.__id = id
    
    def set_enddate(self, enddate):
        self.__enddate = enddate
        
    def set_startdate(self, startdate):
        self.__startdate = startdate
        
    def set_Vehicle(self, Vehicle):
        self.__vehicle = Vehicle
    
    def set_Agency(self, Agency):
        self.__agency = Agency
        
    def set_User(self, User):
        self.__user = User
        
    def set_reservation(self, dico):
        for key in dico:
            if key=='enddate':
                self.__enddate=dico['enddate']
            elif key=='Vehicle':
                self.__vehicle=dico['Vehicle']   
            elif key=='Agency':
                self.__agency=dico['Agency']
            elif key=='User':
                self.__user=dico['User']
            elif key=='startdate':
                self.__startdate=dico['startdate']
            elif key=='id':
                self.__id=dico['id']
                
    def affiche(self):
        print('startdate:',self.__startdate)
        print('enddate:',self.__enddate)
        print('Vehicle:',self.__vehicle)
        print('Agency:',self.__agency)
        print('User:',self.__user)
        print('id:',self.__id)