class User():
    def __init__(self, username='?', name='?', surname='?', password='?', email='?', phone=0, address='?', admin=bool):
        self.__username=username
        self.__name=name
        self.__surname=surname
        self.__password=password
        self.__email=email
        self.__phone=phone
        self.__address=address
        self.__admin=admin
        
    def affiche(self):
        print('username:',self.__username)
        print('name:',self.__name)
        print('surname:',self.__surname)
        print('password:',self.__password)
        print('email:',self.__email)
        print('phone:',self.__phone)
        print('address:',self.__address)
        print('is_admin:',self.__admin)
        
    def get_all(self):
        return {'username':self.__username,'name':self.__name,'surname':self.__surname,'password':self.__password,'email':self.__email,'phone':self.__phone,'address':self.__address,'is_admin':self.__admin}
        
    def get_username(self):
        return self.__username
    
    def get_name(self):
        return self.__name
    
    def get_surname(self):
        return self.__surname
    
    def get_password(self):
        return self.__password
    
    def get_email(self):
        return self.__email
    
    def get_phone(self):
        return self.__phone
    
    def get_address(self):
        return self.__address
    
    def get_admin(self):
        return self.__admin
    
    def set_username(self,username):
        self.__username=username

    def set_name(self,name):
        self.__name=name

    def set_surname(self,surname):
        self.__surname=surname

    def set_password(self,password):
        self.__password=password
    
    def set_admin(self,admin):
        self.__admin=admin

    def set_email(self,email):
        self.__email=email

    def set_phone(self,phone):
        self.__phone=phone

    def set_address(self,address):
        self.__address=address
  
    def set_user(self,dico):
        for key in dico:
            if key=='username':
                self.set_username(dico['username'])
            elif key=='name':
                self.set_name(dico['name'])
            elif key=='surname':
                self.set_surname(dico['surname'])
            elif key=='password':
                self.set_password(dico['password'])
            elif key=='email':
                self.set_email(dico['email'])
            elif key=='phone':
                self.set_phone(dico['phone'])
            elif key=='address':
                self.set_address(dico['address'])
            elif key=='is_admin':
                self.set_admin(dico['is_admin'])
       
