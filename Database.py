from sqlite3 import *
import sqlite3 as sql
from Users import *
from Agencies import *
from VehicleLoc import *


class DataBase:
    def __init__(self,db_name):
        try:
            self.__connexion = sql.connect(db_name)
            print("Connexion établie avec la base de données")
            
        except sql.Error as e:
            print("Erreur lors de la connexion à la base de données", e)  
            
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Vehicles \
                        (license_plate TEXT PRIMARY KEY, \
                        brand TEXT, \
                        model TEXT, \
                        seats INTEGER, \
                        engine TEXT, \
                        transmission TEXT,\
                        category TEXT, \
                        price INTEGER, \
                        mileage INTEGER, \
                        id_agency INTEGER, \
                        picture BLOB)")
                        
            cursor.close()
            print("Table de véhicules opérationnelle")
        except sql.Error as e:
            print("Erreur lors de la création de la table de véhicules",e)
                  
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Users \
                        (username TEXT PRIMARY KEY, \
                        name TEXT, \
                        surname TEXT, \
                        password TEXT,  \
                        email TEXT, \
                        phone TEXT, \
                        address TEXT, \
                        is_admin BOOLEAN)")
            cursor.close()
            print("Table d'utilisateurs opérationnelle")
        except sql.Error as e:
            print("Erreur lors de la création de la table",e)
            
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Agency \
                        (id_agency INTEGER PRIMARY KEY AUTOINCREMENT, \
                        phone TEXT, \
                        street TEXT, \
                        zip_code TEXT, \
                        city TEXT)")
            
            cursor.close()
            print("Table d'agences opérationnelle")
        except sql.Error as e:
            print("Erreur lors de la création de la table d'agences",e)
            
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Reservations\
                        (id_reservation INTEGER PRIMARY KEY AUTOINCREMENT,\
                        startdate TEXT,\
                        enddate TEXT,\
                        license_plate TEXT,\
                        id_agency INTEGER,\
                        username TEXT,\
                        FOREIGN KEY (license_plate) REFERENCES Vehicles (license_plate),\
                        FOREIGN KEY (id_agency) REFERENCES Agency (id_agency),\
                        FOREIGN KEY (username) REFERENCES Users (username))")

            cursor.close()
            print("Table de réservations opérationelle")
        except sql.Error as e:
            print("Erreur lors de la création de la table de réservations")
    def db_close(self):
        try:
            self.__connexion.close()
            print("Base de données fermée")
        except sql.Error as e:
            print("Erreur lors de la fermeture de la base de données",e)
    
    ########################################################################        
    ##########################UTILISATEURS##################################        
    ########################################################################
    
    def db_insertUser(self,Userinsert):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("INSERT INTO Users (username, name, surname, password, email, phone, address, is_admin) \
                        VALUES (?,?,?,?,?,?,?,?)", (Userinsert.get_username(), Userinsert.get_name(), Userinsert.get_surname(), Userinsert.get_password(), Userinsert.get_email(), Userinsert.get_phone(), Userinsert.get_address(), Userinsert.get_admin()))
            cursor.close()
            self.__connexion.commit()
            print("Utilisateur ajouté")
        except sql.Error as e:
            print("Erreur lors de l'insertion d'un utilisateur",e)
            return None
        
    def db_loginVerification(self,Userlogin):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("SELECT COUNT (*) FROM Users WHERE username=? AND password=?", (Userlogin.get_username(), Userlogin.get_password()))
            count=cursor.fetchone()[0]
            cursor.execute("SELECT is_admin FROM Users WHERE username=? AND password=?", (Userlogin.get_username(), Userlogin.get_password()))
            admin=cursor.fetchone()
            cursor.close()
            if count==1:
                return (True,admin)
            else:
                return (False,admin)
        except sql.Error as e:
            print("Erreur lors de la vérification de l'utilisateur",e)
              
    def db_searchUsers(self, Usersearch):
        try:          
            cursor = self.__connexion.cursor()
            query = "SELECT * FROM Users WHERE"
            conditions = []
            parameters = []
            
            if Usersearch.get_name():
                conditions.append("name LIKE ?")
                parameters.append('%' + Usersearch.get_name() + '%')

            if Usersearch.get_surname():
                conditions.append("surname LIKE ?")
                parameters.append('%' + Usersearch.get_surname() + '%')

            if Usersearch.get_username():
                conditions.append("username LIKE ?")
                parameters.append('%' + Usersearch.get_username() + '%')

            if Usersearch.get_email():
                conditions.append("email LIKE ?")
                parameters.append('%' + Usersearch.get_email() + '%')

            if Usersearch.get_phone():
                conditions.append("phone LIKE ?")
                parameters.append('%' + Usersearch.get_phone() + '%')

            if Usersearch.get_address():
                conditions.append("address LIKE ?")
                parameters.append('%' + Usersearch.get_address() + '%')

            if Usersearch.get_admin():
                conditions.append("is_admin LIKE ?")
                parameters.append(Usersearch.get_admin())

            if conditions:
                query += " " + " AND ".join(conditions)

            cursor.execute(query, parameters)
            foundusers = cursor.fetchall()
            cursor.close()
            new_list = []
            for sublist in foundusers:
                dico = {'username': sublist[0], 'name': sublist[1], 'surname': sublist[2], 'password': sublist[3], 'email': sublist[4], 'phone': sublist[5], 'address': sublist[6], 'is_admin': sublist[7]}
                founduser = User()
                founduser.set_user(dico)
                new_list.append(founduser)
            return new_list
        except sql.Error as e:
            print("Erreur lors de la recherche d'un utilisateur", e)
 
    def db_deleteUser(self,Userdelete):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("DELETE FROM Users WHERE username=?", (Userdelete.get_username(),))
            self.__connexion.commit()
            cursor.close()
            print("Utilisateur supprimé: ",Userdelete.get_username())
        except sql.Error as e:
            return("Erreur lors de la suppression d'un utilisateur",e)
            
    def db_updateUser(self,Userupdate):              
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("UPDATE Users SET surname=?, name=?, password=?, email=?, phone=?, address=?, is_admin=? WHERE username=?", (Userupdate.get_surname(), Userupdate.get_name(), Userupdate.get_password(), Userupdate.get_email(), Userupdate.get_phone(), Userupdate.get_address(), Userupdate.get_admin(), Userupdate.get_username()))
            self.__connexion.commit()
            cursor.close()
            print("Utilisateur mis à jour :", Userupdate.get_username())
        except sql.Error as e:
            print("Erreur lors de la modification d'un utilisateur",e)
            
    ###################################################################           
    ##########################AGENCES##################################
    ###################################################################
    def db_insertAgency(self,Agencyinsert):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("INSERT INTO Agency (phone, city, zip_code, street)\
                        VALUES (?,?,?,?)", (Agencyinsert.get_phone(),Agencyinsert.get_city(),Agencyinsert.get_zip(),Agencyinsert.get_street()))
            self.__connexion.commit()
            cursor.close()
            print("Agence ajoutée")
        except sql.Error as e:
            print("Erreur lors de l'insertion d'une agence",e)
    
    def db_updateAgency(self,Agencyupdate):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("UPDATE Agency SET phone=?, city=?, zip_code=?, street=? WHERE id_agency=?", (Agencyupdate.get_phone(),Agencyupdate.get_city(),Agencyupdate.get_zip(),Agencyupdate.get_street(),self.db_getAgency_id(Agencyupdate)))
            self.__connexion.commit()
            cursor.close()
            print("Agence mise à jour :", Agencyupdate.get_id())
        except sql.Error as e:
            print("Erreur lors de la modification d'une agence",e)
            
    def db_getAgency_parc(self,Agencyid):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("SELECT license_plate FROM Vehicles WHERE id_agency=?",(Agencyid.get_id(),))
            agencies_parc=cursor.fetchall()
            cursor.close()
            return agencies_parc
        except sql.Error as e:
            print("Erreur lors de la récupération du parc des agences",e)
            
    def db_getAgencies_location(self):
        try:
            cursor = self.__connexion.cursor()
            cursor.execute("SELECT city, zip_code, id_agency FROM Agency")
            agencies_data = cursor.fetchall()
            cursor.close()
            agencies_list = []
            for agency_data in agencies_data:
                city = agency_data[0]
                zip_code = agency_data[1]
                id_agency = agency_data[2]
                agency_entry = f"{city} ({zip_code[:2]}) id: {id_agency}"
                agencies_list.append(agency_entry)
            return agencies_list
        except sql.Error as e:
            print("Erreur lors de la récupération de la localisation des agences", e)
   
    def db_getAgency(self,Agencyget):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("SELECT * FROM Agency WHERE id_agency=?", (Agencyget.get_id(),))
            agency_infos=cursor.fetchone()
            cursor.close()
            return agency_infos
        except sql.Error as e:
            print("Erreur lors de la récupération des informations d'une agence",e)
            
    def db_getAgency_id(self,Agencyget):
        try:
            cursor=self.__connexion.cursor()
            print(Agencyget.get_city(),Agencyget.get_zip())
            cursor.execute("SELECT id_agency FROM Agency WHERE city=? AND zip_code=?", (Agencyget.get_city(),Agencyget.get_zip()))
            agency_id=cursor.fetchone()
            cursor.close()
            print(agency_id)
            return agency_id[0]
        except sql.Error as e:
            print("Erreur lors de la récupération de l'id d'une agence",e)
            
    def db_deleteAgency(self,Agencydelete):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("DELETE FROM Agency WHERE id_agency=?", (Agencydelete.get_id(),))
            self.__connexion.commit()
            cursor.close()
            cars=self.db_getAgency_parc(Agencydelete)
            for car in cars:
                cursor=self.__connexion.cursor()
                cursor.execute("DELETE FROM Vehicles WHERE license_plate=?", (car[0],))
                self.__connexion.commit()
                cursor.close()
            print("Agence supprimée")
        except sql.Error as e:
            print("Erreur lors de la suppression d'une agence",e)
     
    #####################################################################    
    ##########################VEHICULES##################################
    #####################################################################
    
    def db_insertVehicle(self, Vehicleinsert):
        try:
            cursor = self.__connexion.cursor()
            # Vérifier si le véhicule existe déjà dans la base de données
            cursor.execute("SELECT * FROM Vehicles WHERE license_plate = ?", (Vehicleinsert.get_license_plate(),))
            existing_vehicle = cursor.fetchone()

            if existing_vehicle:
                cursor.execute("UPDATE Vehicles SET brand = ?, model = ?, category = ?, seats = ?, engine = ?, transmission = ?, price = ?, mileage = ?, id_agency = ?, picture = ? WHERE license_plate = ?",
                            (Vehicleinsert.get_brand(), Vehicleinsert.get_model(), Vehicleinsert.get_category(), Vehicleinsert.get_seats(), Vehicleinsert.get_engine(), Vehicleinsert.get_transmission(), Vehicleinsert.get_price(), Vehicleinsert.get_mileage(), Vehicleinsert.get_id_agency(), Vehicleinsert.get_picture(), Vehicleinsert.get_license_plate()))
                print("Véhicule modifié")
            else:
                cursor.execute("INSERT INTO Vehicles (license_plate, brand, model, category, seats, engine, transmission, price, mileage, id_agency, picture) \
                                VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                            (Vehicleinsert.get_license_plate(), Vehicleinsert.get_brand(), Vehicleinsert.get_model(), Vehicleinsert.get_category(), Vehicleinsert.get_seats(), Vehicleinsert.get_engine(), Vehicleinsert.get_transmission(), Vehicleinsert.get_price(), Vehicleinsert.get_mileage(), Vehicleinsert.get_id_agency(), Vehicleinsert.get_picture()))
                print("Véhicule ajouté")

            self.__connexion.commit()
            cursor.close()
        except sql.Error as e:
           print("Erreur lors de l'insertion/modification d'un véhicule :", e)
           
    def db_getAllVehicles(self):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("SELECT license_plate FROM Vehicles")
            vehicles=cursor.fetchall()
            cursor.close()
            return vehicles
        except sql.Error as e:
            print("Erreur lors de la récupération des véhicules",e)
            
    def db_getVehicle(self,Vehicleget):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("SELECT * FROM Vehicles WHERE license_plate=?", (Vehicleget.get_license_plate(),))
            vehicle_infos=cursor.fetchone()
            cursor.close()
            return vehicle_infos
        except sql.Error as e:
            print("Erreur lors de la récupération des informations d'un véhicule",e)
            
    def db_deleteVehicle(self,Vehicledelete):
        try:
            cursor=self.__connexion.cursor()
            print(Vehicledelete.get_license_plate)
            cursor.execute("DELETE FROM Vehicles WHERE license_plate=?", (Vehicledelete.get_license_plate(),))
            self.__connexion.commit()
            cursor.close()
            print("Véhicule supprimé")
        except sql.Error as e:
            print("Erreur lors de la suppression d'un véhicule",e)
            
    def db_getPicture(self,Vehiclepicture):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("SELECT picture FROM Vehicles WHERE license_plate=?", (Vehiclepicture.get_license_plate(),))
            picture=cursor.fetchone()
            cursor.close()
            return picture
        except sql.Error as e:
            print("Erreur lors de la récupération de la photo d'un véhicule",e)
            
    def db_getAgIdVehicle(self,Vehicleget):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("SELECT id_agency FROM Vehicles WHERE license_plate=?", (Vehicleget.get_license_plate(),))
            agid=cursor.fetchone()
            cursor.close()
            return agid[0]
        except sql.Error as e:
            print("Erreur lors de la récupération de l'id d'une agence",e)
            
            
    ######################################################################## 
    ##########################RESERVATIONS##################################
    ########################################################################
    def db_getAllReservations(self):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("SELECT * FROM Reservations")
            reservations=cursor.fetchall()
            cursor.close()
            all=[]
            for res in reservations:
                reservation='Début : '+str(res[1])+' | Fin : '+str(res[2])+' | Véhicule : '+str(res[3])+' | Agence : '+str(res[4])+' | Utilisateur : '+str(res[5])+' | ID : '+str(res[0])
                all.append(reservation)
            return all
        except sql.Error as e:
            print("Erreur lors de la récupération des réservations",e)
    
    def db_insertReservation(self, Reservationinsert):
        try:
            cursor = self.__connexion.cursor()
            # Vérifier si le véhicule existe déjà dans la base de données
            cursor.execute("SELECT * FROM Reservations WHERE id_reservation= ?", (Reservationinsert.get_id(),))
            existing_resa = cursor.fetchone()
            
            if existing_resa:
                cursor.execute("UPDATE Reservations SET startdate = ?, enddate = ?, license_plate = ?, id_agency = ?, username = ? WHERE id_reservation = ?",\
                            (Reservationinsert.get_startdate(), Reservationinsert.get_enddate(), Reservationinsert.get_Vehicle().get_license_plate(), Reservationinsert.get_Agency().get_id(), Reservationinsert.get_User().get_username(), Reservationinsert.get_id()))
                print("Réservation modifiée")
            else:
                cursor.execute("INSERT INTO Reservations (startdate, enddate, license_plate, id_agency, username) \
                            VALUES (?,?,?,?,?)", (Reservationinsert.get_startdate(), Reservationinsert.get_enddate(), Reservationinsert.get_Vehicle().get_license_plate(), Reservationinsert.get_Agency().get_id(), Reservationinsert.get_User().get_username()))
                print("Réservation ajoutée")
            
            self.__connexion.commit()
            cursor.close()
        except sql.Error as e:
            print("Erreur lors de l'insertion d'une réservation",e)
            
            
    def db_getReservations(self,Reservationget):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("SELECT * FROM Reservations WHERE id_reservation=?", (Reservationget.get_id(),))
            reservation_infos=cursor.fetchone()
            cursor.close()
            return reservation_infos
        except sql.Error as e:
            print("Erreur lors de la récupération des informations d'une réservation",e)
            
    def db_searchRes(self, Reservationsearch):
        try:
            cursor = self.__connexion.cursor()
            query = "SELECT * FROM Reservations WHERE"
            conditions = []
            parameters = []
            try:
                if Reservationsearch.get_Agency().get_id():
                    conditions.append("id_agency LIKE ?")
                    parameters.append('%' + Reservationsearch.get_Agency().get_id() + '%')
            except:
                pass
            try:
                if Reservationsearch.get_User().get_username()!='':
                    conditions.append("username LIKE ?")
                    parameters.append('%' + Reservationsearch.get_User().get_username() + '%')
            except:
                pass
            if conditions:
                query += " " + " OR ".join(conditions)
            cursor.execute(query, parameters)
            foundres = cursor.fetchall()
            cursor.close()
            list=[]
            for res in foundres:
                reservation='Début : '+str(res[1])+' | Fin : '+str(res[2])+' | Véhicule : '+str(res[3])+' | Agence : '+str(res[4])+' | Utilisateur : '+str(res[5])+' | ID : '+str(res[0])
                list.append(reservation)
            return list
            
        except sql.Error as e:
            print("Erreur lors de la recherche d'une réservation", e)
                  
    def db_checkResdispo(self, Reservationcheck):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("SELECT COUNT (*) FROM Reservations WHERE license_plate=? AND startdate<=? AND enddate>=? OR startdate <= ? AND enddate >= ?", (Reservationcheck.get_Vehicle().get_license_plate(),Reservationcheck.get_startdate(),Reservationcheck.get_enddate(),Reservationcheck.get_startdate(),Reservationcheck.get_enddate()))
            dispo=cursor.fetchone()
            cursor.close()
            if dispo[0]==0:
                dispo=True
            else:
                dispo=False
            return dispo
        except sql.Error as e:
            print("Erreur lors de la vérification de la disponibilité d'un véhicule",e)
            
    def db_getCarRes(self,Cartoget):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("SELECT startdate,enddate FROM Reservations WHERE license_plate=?",(Cartoget.get_license_plate(),))
            Bookeddate=cursor.fetchall()
            cursor.close()
            return Bookeddate
        except sql.Error as e:
            print("Erreur lors de la recherche de dates réservées",e)
            
    def db_deleteReservation(self,Reservationdelete):
        try:
            cursor=self.__connexion.cursor()
            cursor.execute("DELETE FROM Reservations WHERE id_reservation=?", (Reservationdelete.get_id(),))
            self.__connexion.commit()
            cursor.close()
            print("Réservation supprimée")
        except sql.Error as e:
            print("Erreur lors de la suppression d'une réservation",e)