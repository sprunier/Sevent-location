import tkinter as tk
from tkinter import*
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from tkinter.filedialog import *
from Users import *
from VehicleLoc import *
from Reservations import *
from Agencies import *
from Database import *
from PIL import Image, ImageTk
from io import BytesIO
import copy
from datetime import *
from tkcalendar import *

class App(tk.Tk):
    def __init__(self,dataBase):
        global db
        db=dataBase
        #Initialisation de la classe parente
        super().__init__()
        self.configure(background="#f4811e")
        
        self.__cartoreserve=None
        self.__userlogged=None
        self.__selectedagency=None

        # Paramètres de la fenêtre principale
        self.configure(background="#f4811e")
        self.title("Sevent")   

    ###########################################
    ##### FONCTIONS DE CHANGEMENT DE PAGE ##### 
    ########################################### 
    
    def clear_page(self):
        # Fonction pour afficher une page et cacher les autres
        for widget in self.winfo_children():
            widget.destroy()

    def change_page(self, page_name):
        self.clear_page()
        getattr(self, f"init_{page_name}").__call__()
            
    def build_page(self, page_name,color="#f4811e"):
        self.clear_page()
        frame=tk.Frame(self)
        frame.place(relx=0.5, rely=0.5,anchor=CENTER)
        frame.configure(background=color)
        setattr(self, f"{page_name}_frame", frame)

    def create_survey_frame(self,parent, title, labels=[], entries=[], buttons=[], button_positions=[], label_positions=[], combobox=[], combobox_values=[], combobox_positions=[]):
        # Create the frame
        custom_frame = tk.Frame(parent)
        custom_frame.configure(background="#f4811e")
        custom_frame.columnconfigure(0, weight=1)
        custom_frame.columnconfigure(1, weight=1)
        # Add the title label
        tk.Label(custom_frame, text=title, font=("Arial", 15,"bold"), background="#f4811e", foreground="black").grid(row=0, column=0, columnspan=2)

        for i in range(len(labels)):
            if i >= len(label_positions):
                print("Pas assez de positions de labels fournies.")
                break
            tk.Label(custom_frame, text=labels[i], background="#f4811e", foreground="black", font=("Arial", 10, "bold")).grid(row=label_positions[i][0], column=label_positions[i][1], pady=1)
            if i >= len(entries):
                break
            if entries[i] == "*":
                entries[i] = tk.StringVar()
                tk.Entry(custom_frame, textvariable=entries[i], background="grey",show="*").grid(row=i+1, column=1)
            else:
                tk.Entry(custom_frame, textvariable=entries[i], background="grey").grid(row=i+1, column=1)

        # Add the buttons
        for i in range(len(buttons)):
            if i >= len(button_positions):
                print("Pas assez de positions de boutons fournies. ")
                break
            tk.Button(custom_frame, text=buttons[i][0], command=buttons[i][1],relief=buttons[i][2], background="#f4811e", foreground="black", font=("Arial", 10, "bold")).grid(row=button_positions[i][0], column=button_positions[i][1],columnspan=button_positions[i][2],pady=2)
        
        # Add the comboboxes
        for i in range(len(combobox)):
            if i >= len(combobox_positions):
                print("Pas assez de positions de combobox fournies. ")
                break
            if i >= len(combobox_values):
                print("Pas assez de valeurs de combobox fournies. ")
                break
            combobox[i] = ttk.Combobox(custom_frame, values=combobox_values[i],textvariable=combobox[i])
            combobox[i].grid(row=combobox_positions[i][0], column=combobox_positions[i][1], pady=1)
        return custom_frame
    
    ###########################################
    ############ FONCTIONS UTILES #############
    ###########################################
    
    def setVehicleCalendar(self,calendar,vehicle):
        reservations = db.db_getCarRes(vehicle)

        for reservation in reservations:
            startdate = reservation[0]
            enddate = reservation[1]
            startdate = datetime.strptime(startdate, "%Y-%m-%d")
            enddate = datetime.strptime(enddate, "%Y-%m-%d")
            # Calculer la plage de jours réservés
            bookeddays = []
            current_date = startdate
            while current_date <= enddate:
                bookeddays.append(current_date)
                current_date += timedelta(days=1)
                
            for bookedday in bookeddays:
                event_style = {"background": "red", "foreground": "white"}
                calendar.tag_config("reserved", **event_style)
                calendar.calevent_create(bookedday,'Reservé',"reserved")
        
    #############################
    ##### PAGE DE CONNEXION #####
    #############################           
        
    def init_login(self):
        # Variables pour les entrées utilisateur
        title = "Connexion"
        labelslog = ["Nom d'utilisateur", "Mot de passe"]
        button_positionslog = [(3, 0, 1), (3, 1, 1), (4, 0, 2)]
        label_positionslog = [(1, 0), (2, 0)]
        entrieslog = [tk.StringVar(), "*"]
        buttonslog=[("Connexion",lambda: login(entrieslog[0].get(),entrieslog[1].get()),RAISED),("Créer un compte",lambda:self.change_page("registration"),RAISED),("Se connecter en tant qu'invité",lambda: guest(),FLAT)]
        self.login_frame = self.create_survey_frame(self, title, labels=labelslog, entries=entrieslog, buttons=buttonslog, button_positions=button_positionslog, label_positions=label_positionslog)
        self.login_frame.place(relx=0.5, rely=0.5,anchor=CENTER)
       
        def guest():
            self.change_page("customer")
            self.__userlogged='guest'
            
        def login(username,password):
            # Code pour la connexion de l'utilisateur
            loginUser=User()
            infos={"username":username,"password":password}
            loginUser.set_user(infos)
            test=db.db_loginVerification(loginUser)
            if test is None:
                tk.messagebox.showerror("Erreur", "Erreur de connexion à la base de données")
            elif test[0]==False:
                tk.messagebox.showerror("Erreur", "Mauvais identifiants")
            elif test[0]==True:
                if test[1][0]==1:
                    self.change_page("admin")
                    loginUser.set_admin(1) 
                else:
                    self.change_page("customer")
                    loginUser.set_admin(0)
                self.__userlogged=loginUser

                    
    ##############################   
    ##### PAGE D'INSCRIPTION #####
    ##############################
    
    def init_registration(self):
        # Conteneurs pour les entrées utilisateur
        title = "Inscription"
        labelsreg = ["Nom d'utilisateur", "Mot de passe", "Nom", "Prénom", "Email", "Téléphone", "Adresse"]
        button_positionsreg = [(9, 0, 2), (10, 0, 2)]
        label_positionsreg = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
        entriesreg = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        buttonsreg=[("S'inscrire",lambda: register(entriesreg[0].get(),entriesreg[1].get(),entriesreg[2].get(),entriesreg[3].get(),entriesreg[4].get(),entriesreg[5].get(),entriesreg[6].get()),RAISED),("Retour",lambda:self.change_page("login"),RAISED)]
        self.registration_frame = self.create_survey_frame(self, title, labels=labelsreg, entries=entriesreg, buttons=buttonsreg, button_positions=button_positionsreg, label_positions=label_positionsreg)
        self.registration_frame.place(relx=0.5, rely=0.5,anchor=CENTER)

    
        ##### INSCRIPTION : Erreur si champs vides, admin si username commence par admin puis enregistrement dans la db #####
        def register(username, password, name, surname, email, phone, address):
            infos = {'username': username, 'password': password, 'name': name, 'surname': surname, 'email': email, 'phone': phone, 'address': address}
            is_admin = 0
            for key, value in infos.items():
                if value == "":
                    tk.messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
                    return
                if key == "username":
                    if value.startswith("admin"):
                        is_admin = 1
            infos['is_admin'] = is_admin
            newUser=User()
            newUser.set_user(infos)
            db.db_insertUser(newUser)
            self.change_page('login')

    #################################
    ##### PAGE D'ADMINISTRATION #####
    #################################
    
    def init_admin(self):
        title = "Administration"
        button_pos = [(5, 0, 2), (6, 0, 2), (7, 0, 2), (8, 0, 2), (9, 0, 2)]
        but=[("Gestion des utilisateurs",lambda: self.change_page("userManager"),RAISED),("Gestion des agences",lambda: self.change_page("agencyManager"),RAISED),("Gestion des véhicules",lambda: self.change_page("parcManager"),RAISED),("Gestion des réservations",lambda: self.change_page("reservationManager"),RAISED),("Retour",lambda:self.change_page("login"),RAISED)]
        self.admin_frame = self.create_survey_frame(self, title, buttons=but, button_positions=button_pos)
        self.admin_frame.place(relx=0.5, rely=0.5,anchor=CENTER)
       
    ############################################
    ##### PAGE DE GESTION DES UTILISATEURS #####
    ############################################
    
    def init_userManager(self):
        title = "Gestion des utilisateurs"
        labelman = ["Nom d'utilisateur", "Nom", "Prénom", "Email", "Téléphone", "Adresse","Type de compte"]
        
        label_posman= [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),(7,0)]
        entriesman = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        comboBoxman=[tk.StringVar()]
        comboBoxValuesman = [["Administrateur","Utilisateur"]]
        ComboPositionsman = [(7,1)]
        buttonsman=[("Rechercher",lambda: search(entriesman[0].get(),entriesman[1].get(),entriesman[2].get(),entriesman[3].get(),entriesman[4].get(),entriesman[5].get(),comboBoxman[0].get()),RAISED),("Retour",lambda:self.change_page("admin"),RAISED)]
        buttonpos_man = [(9, 0, 2), (10, 0, 2)]
        self.userManager_frame = self.create_survey_frame(self, title, labels=labelman, entries=entriesman, buttons=buttonsman, button_positions=buttonpos_man, label_positions=label_posman,combobox=comboBoxman,combobox_values=comboBoxValuesman,combobox_positions=ComboPositionsman)
        self.userManager_frame.place(relx=0.5, rely=0.5,anchor=CENTER)


        def search(username,name,surname,email,phone,address,is_admin):
            for widget in self.userManager_frame.winfo_children():
                if isinstance(widget, tk.Listbox):
                    widget.destroy()
            # Code pour la recherche d'un utilisateur
            infos={'username':username,'name':name,'surname':surname,'email':email,'phone':phone,'address':address,'is_admin':is_admin}
            if is_admin=='Administrateur':
                infos['is_admin']='1'
            elif is_admin=='Utilisateur':
                infos['is_admin']='0'
            userssearched=User()
            userssearched.set_user(infos)
            search_result = db.db_searchUsers(userssearched)
            if search_result==[]:
                listbox = tk.Listbox(self.userManager_frame,height=10, width=40)
                listbox.grid(row=11, column=0, columnspan=2)
                listbox.insert(0, "Aucun résultat")
            else:         
                max_length = max(len(str(item.get_all())) for item in search_result)
                listbox = tk.Listbox(self.userManager_frame,height=20, width=max_length)
                listbox.grid(row=11, column=0, columnspan=2)
                for i in range(len(search_result)):
                    listbox.insert(i, search_result[i].get_all())
            
            def on_double_click(event):
                w = event.widget
                # Récupérer la position de l'élément sélectionné dans la liste
                index = int(w.curselection()[0])
                # Récupérer la valeur de l'élément sélectionné
                value = w.get(index)
                # Créer une Entry à la place de l'élément sélectionné et y insérer la valeur de l'élément
                edit_entry = tk.Entry(w,width=max_length)
                edit_entry.insert(0, value)
                edit_entry.grid(row=11+index, column=0, columnspan=2)
                # Supprimer l'élément sélectionné de la liste
                w.delete(index)
                
                def on_entry_keypress(event):
                    if event.keysym == "Return":
                        # Récupérer la nouvelle valeur de l'Entry
                        new_value_str = edit_entry.get()
                        new_value=eval(new_value_str)
                        # Mettre à jour la liste des données utilisateur sélectionnées avec la nouvelle valeur
                        search_result[index]= new_value
                        # Cacher l'Entry
                        edit_entry.grid_forget()
                        # Réinsérer la ligne modifiée dans la Listbox
                        listbox.insert(index, new_value)
                        # Mettre le focus sur la Listbox
                        listbox.focus_set()

                # Lier la touche "Entrée" à l'événement on_entry_keypress
                edit_entry.bind("<Return>", on_entry_keypress)
            
            # Lier le double-clic à chaque élément de la Listbox
            listbox.bind("<Double-Button-1>", on_double_click)
                    
            def submit_users():
                rows=[]
                for i in range(listbox.size()):
                    dico_str=listbox.get(i)
                    dico=eval(dico_str)
                    rows.append(dico)
                    UsertoUpdate=User()
                    UsertoUpdate.set_user(dico)
                    db.db_updateUser(UsertoUpdate)
                listbox.destroy()
                search(entriesman[0].get(),entriesman[1].get(),entriesman[2].get(),entriesman[3].get(),entriesman[4].get(),entriesman[5].get(),comboBoxman[0].get())
                tk.messagebox.showinfo("Modification","Les modifications ont bien été prises en compte")
                       
            def delete_user():
                selected_index = listbox.curselection()
                if selected_index:
                    selected_value = listbox.get(selected_index[0])
                    UsertoDelete=User()
                    UsertoDelete.set_user(eval(selected_value))
                    confirmation = messagebox.askyesno("Suppression", f"Êtes-vous sûr de vouloir supprimer l'utilisateur {UsertoDelete.get_username()} ?\n\nCeci supprimera également toutes les réservations de cet utilisateur.")
                    
                    if confirmation:
                        Resedel=Reservation()
                        Resedel.set_User(UsertoDelete)
                        foundres=db.db_searchRes(Resedel)
                        for res in foundres:
                            print(res)
                            Reservdel=Reservation()
                            id_reservation = res.split("|")[-1].strip().split(":")[-1].strip()
                            Reservdel.set_id(id_reservation)
                            db.db_deleteReservation(Reservdel)
                        db.db_deleteUser(UsertoDelete)
                        tk.messagebox.showinfo("Suppression",f"L'utilisateur {UsertoDelete.get_username()} a bien été supprimé.")
                        search(entriesman[0].get(),entriesman[1].get(),entriesman[2].get(),entriesman[3].get(),entriesman[4].get(),entriesman[5].get(),comboBoxman[0].get())
                    else:
                        tk.messagebox.showinfo("Suppression", "La suppression de l'utilisateur a été annulée.")
                        return
                 
                else:
                    tk.messagebox.showerror("Suppression","Aucun élément selectionné")
                
            # Ajouter un bouton "Valider"
            tk.Button(self.userManager_frame, text="Valider les changements", command=submit_users, background="#f4811e",foreground="black", font=("Arial",10,"bold")).grid(row=12, column=0, padx=10)
            tk.Button(self.userManager_frame, text="Supprimer l'utilisateur", command=delete_user,background="#f4811e",foreground="black", font=("Arial",10,"bold")).grid(row=12, column=1, pady=10,padx=10)
            
    ########################################
    ##### PAGE DE GESTION DES AGENCES ######
    ########################################
    def init_agencyManager(self):
        title="Gerer les agences"
        buttonsman=[("Créer une agence",lambda:self.change_page("agencyCreation"),RAISED),("Supprimer une agence",lambda:self.change_page("agencyDeletion"),RAISED),("Retour",lambda:self.change_page("admin"),RAISED)]
        button_posman = [(9, 0, 2), (10, 0, 2),(11, 0, 2)]
        self.agencyManager_frame= self.create_survey_frame(self, title, buttons=buttonsman, button_positions=button_posman)
        self.agencyManager_frame.place(relx=0.5, rely=0.5,anchor=CENTER)
        
    ########################################
    ###### PAGE DE CREATION D'AGENCE #######
    ########################################
    def init_agencyCreation(self):
        title="Création d'une agence"
        labelscre=["Rue","Code postal","Ville","Téléphone"]
        labelposcre=[(1,0),(2,0),(3,0),(4,0)]
        entriescre=[tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()]

        buttonscre=[("Valider",lambda:submit_agency(entriescre[0].get(),entriescre[1].get(),entriescre[2].get(),entriescre[3].get()),RAISED),("Retour",lambda:self.change_page("agencyManager"),RAISED)]
        button_positionscre = [(5, 0, 2), (6, 0, 2)]
        self.agencyCreation_frame= self.create_survey_frame(self, title, buttons=buttonscre, button_positions=button_positionscre,labels=labelscre,label_positions=labelposcre,entries=entriescre)
        self.agencyCreation_frame.place(relx=0.5, rely=0.5,anchor=CENTER)

        def clear_page():
            for widget in self.agencyCreation_frame.winfo_children():
                widget.destroy()
    
        def submit_agency(streets,zips,citys,phones):
            clear_page()
            newAgency=Agency(city=citys,street=streets,zip=zips,phone=phones)
            db.db_insertAgency(newAgency)
            id=db.db_getAgency_id(newAgency)
            newAgency.set_id(id)
            nb_veh=tk.StringVar()
            tk.Label(self.agencyCreation_frame,text="Combien de véhicules souhaitez vous y ajouter?",font=("Arial",10),background="#f4811e",foreground="black").grid(row=0, column=0,columnspan=2)
            tk.Entry(self.agencyCreation_frame,textvariable=nb_veh,background="grey").grid(row=1,column=0,columnspan=2)
            tk.Button(self.agencyCreation_frame,text="Valider",command=lambda: newVehpage(newAgency,int(nb_veh.get())),background="#f4811e").grid(row=2,column=0,columnspan=2)
                     
        def newVehpage(agency,vehicletoset):               
            def import_image():
                #Importer une image
                global filepath
                filepath= askopenfilename(title="Ouvrir une image",filetypes=[('png files','.png'),('all files','.*')])
                if not filepath:
                    return
                global photo
                global image_label
                imagedata = Image.open(str(filepath))
                photo = ImageTk.PhotoImage(imagedata)
                image_label = tk.Label(frame, image=photo,background="#f4811e")
                image_label.grid(row=11, column=0, columnspan=2)

            def submit_vehicle():
                try:
                    with open(filepath, 'rb') as f:
                        picture_data = f.read()
                except:
                    messagebox.showerror("Erreur", "Veuillez importer une image")
                    return
                dico={'brand':brand_entry.get(),'model':model_entry.get(),'seats':nseats_entry.get(),'license_plate':license_plate_entry.get(),'mileage':nkilometers_entry.get(),'price':price_entry.get(),'category':combo_category.get(),'transmission':combo_transmission.get(),'engine':combo_engine.get(),'id_agency':agency.get_id(),'picture':picture_data}
                empty=False
                for key in dico:
                    if dico[key]=="":
                        empty=True
                if empty==True:
                    messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
                else:
                    newVehicle=VehLoc()
                    newVehicle.setVehLoc(dico)
                    db.db_insertVehicle(newVehicle)
                    increment_count()
                    
                        
            def clear_fields():
                brand_entry.set("")
                model_entry.set("")
                nseats_entry.set("")
                license_plate_entry.set("")
                nkilometers_entry.set("")
                price_entry.set("")
                combo_category.set("")
                combo_transmission.set("")
                combo_engine.set("")
                try:
                    photo.__del__()
                    image_label.grid_forget()
                    image_label.destroy()
                except:
                    pass
                
            def increment_count():
                global vehicleset
                vehicleset+=1
                if vehicleset<vehicletoset+1:
                    clear_fields()
                else:
                    tk.messagebox.showinfo("Succès", "Les véhicules ont bien été ajoutés")
                    self.change_page("agencyManager")
            
            if vehicletoset==0:
                self.change_page("admin")
            clear_page()
            
            frame=tk.Frame(self.agencyCreation_frame)
            frame.grid(row=0, column=0, columnspan=2)
            brand_entry=tk.StringVar()
            nkilometers_entry=tk.StringVar()
            model_entry=tk.StringVar()
            nseats_entry=tk.StringVar()
            price_entry=tk.StringVar()
            license_plate_entry=tk.StringVar()
            
            #Entries
            frame.configure(background="#f4811e")
            tk.Label(frame, text=f"Saisie du véhicule", font=("Arial",15,"bold"),background="#f4811e",foreground="black").grid(row=0, column=0, columnspan=2,sticky='n')
            tk.Label(frame, text="Marque:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=1, column=0)
            tk.Entry(frame, textvariable=brand_entry, background="grey").grid(row=1, column=1)
            tk.Label(frame, text="Modèle:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=2, column=0)
            tk.Entry(frame, textvariable=model_entry, background="grey").grid(row=2, column=1) 
            tk.Label(frame, text="Nombre de places:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=3, column=0)
            tk.Entry(frame,textvariable=nseats_entry,background="grey").grid(row=3, column=1)
            tk.Label(frame, text="Immatriculation:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=4, column=0)
            tk.Entry(frame, textvariable=license_plate_entry, background="grey").grid(row=4, column=1)
            tk.Label(frame, text="Kilométrage:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=5, column=0)
            tk.Entry(frame, textvariable=nkilometers_entry, background="grey").grid(row=5, column=1)
            tk.Label(frame, text="Prix par jour:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=6, column=0)
            tk.Entry(frame, textvariable=price_entry,background="grey").grid(row=6, column=1)
            
            #Listes déroulantes
            tk.Label(frame, text="Catégorie:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=7, column=0)
            category_values = ["Berline", "SUV", "Coupé", "Cabriolet", "Espace", "Break", "Pick-up", "Luxe", "Utilitaire"]
            combo_category=ttk.Combobox(frame, values=category_values)
            combo_category.grid(row=7, column=1)
            tk.Label(frame, text="Type de transmission:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=8, column=0)
            transmission_values = ["Automatique", "Manuelle"]
            combo_transmission=ttk.Combobox(frame, values=transmission_values)
            combo_transmission.grid(row=8, column=1)
            tk.Label(frame, text="Type de moteur:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=9, column=0)
            engine_values = ["Thermique", "Électrique", "Hybride"]
            combo_engine=ttk.Combobox(frame, values=engine_values)
            combo_engine.grid(row=9, column=1) 
            
            import_button=tk.Button(frame, text="Importer une image",background="#f4811e",foreground="black", font=("Arial",10,"bold"), command=lambda: import_image())
            import_button.grid(row=12, column=0, columnspan=2, pady=10)
                
            # Créer un bouton pour valider la saisie du nouveau véhicule
            tk.Button(frame, text="Valider",background="#f4811e",foreground="black", font=("Arial",10,"bold"), command=lambda: submit_vehicle()).grid(row=13, column=0, pady=10)
            tk.Button(frame, text="Annuler",background="#f4811e",foreground="black", font=("Arial",10,"bold"), command=lambda: clear_fields()).grid(row=13, column=1, pady=10)   
                
    ########################################
    ##### PAGE DE SUPPRESSION D'AGENCE #####
    ########################################
    def init_agencyDeletion(self):
        self.build_page("agencyDeletion")
        agencies=db.db_getAgencies_location()
        combo_agencies=ttk.Combobox(self.agencyDeletion_frame, values=agencies)
        combo_agencies.grid(row=0, column=0, columnspan=2,pady=10)
        tk.Button(self.agencyDeletion_frame, text="Supprimer l'agence",background="#f4811e",foreground="black", font=("Arial",10,"bold"), command=lambda: delete() ).grid(row=1, column=0, columnspan=2,pady=10)
        tk.Button(self.agencyDeletion_frame, text="Retour",background="#f4811e",foreground="black", font=("Arial",10,"bold"), command=lambda: self.change_page("agencyManager")).grid(row=25, column=0, columnspan=2)

        def delete():
            agencyinfo=combo_agencies.get()
            indicechaine=agencyinfo.find("id: ")
            agenceid = ""
            indiceid = indicechaine + len("id: ")  # Indice après "id:"
            while indiceid < len(agencyinfo) and agencyinfo[indiceid].isdigit():
                agenceid += agencyinfo[indiceid]
                indiceid += 1
            agenceid = int(agenceid)
            
            agencytodelete=Agency(id_agency=agenceid)
            confirmation = messagebox.askyesno("Suppression", f"Êtes-vous sûr de vouloir supprimer l'agence {agencytodelete.get_id()} ?\nCette action entrainera la suppression de tous les véhicules de cette agence.")
            
            if confirmation:
                db.db_deleteAgency(agencytodelete)
                tk.messagebox.showinfo("Suppression","Agence supprimée")
                self.change_page("agencyDeletion")
            else:
                tk.messagebox.showinfo("Suppression", "La suppression de l'agence a été annulée.")
                return

    ###################################  
    ##### PAGE DE GESTION DE PARC #####  
    ###################################
    
    def init_parcManager(self):
        def select_agency(event):
            selection=combo_agency.get()
            global Selectedagency
            Selectedagency=Agency()
            if selection=="Toutes les agences":
                parcplates = db.db_getAllVehicles()
                
            else:
                indicechaine=selection.find("id: ")
                agenceid = ""
                indiceid = indicechaine + len("id: ")  # Indice après "id:"
                while indiceid < len(selection) and selection[indiceid].isdigit():
                    agenceid += selection[indiceid]
                    indiceid += 1
                agenceid = int(agenceid)
                Selectedagency.set_id(agenceid)
                parcplates=db.db_getAgency_parc(Selectedagency)
                
            for plate in parcplates:
                voiture=VehLoc(license_plate=plate[0])
                carinfo=db.db_getVehicle(voiture)
                dico={'brand':carinfo[1],'model':carinfo[2],'seats':carinfo[3],'engine':carinfo[4],'transmission':carinfo[5],'category':carinfo[6],'price':carinfo[7],'mileage':carinfo[8],'id_agency':carinfo[9],'picture':carinfo[10] }
                voiture.setVehLoc(dico)
                Selectedagency.add_vehicle(voiture)
                
            # Effacer le contenu actuel de la listbox   
            parc_listbox.delete(0, tk.END)
            if Selectedagency.get_parc() is None or len(Selectedagency.get_parc()) == 0:
                parc_listbox.insert(tk.END, "Aucun véhicule dans cette agence")
            else:
                if selection=="Toutes les agences":
                    for voiture in Selectedagency.get_parc():
                        parc_listbox.insert(tk.END, voiture.get_brand() + " | " + voiture.get_model() + " | " + voiture.get_license_plate()+ " | Agence: " + str(voiture.get_id_agency()))
                else:
                    for voiture in Selectedagency.get_parc():
                         parc_listbox.insert(tk.END, voiture.get_brand() + " | " + voiture.get_model() + " | " + voiture.get_license_plate())
        
        def select_vehicle(event):
            # Obtenir l'indice de l'élément sélectionné dans la listbox
            selected_index = parc_listbox.curselection()
            if selected_index:
                clear_fields()
                selectedinfo=parc_listbox.get(selected_index[0])
                if selectedinfo=="Aucun véhicule dans cette agence":
                    return
                elif selectedinfo.split(" | ")[-1].startswith("Agence"):
                    selectedplate=selectedinfo.split(" | ")[-2]
                else:
                    selectedplate=selectedinfo.split(" | ")[-1]
                global Selectedvehicle
                selected_vehicle=VehLoc(license_plate=selectedplate)
                # Obtenir les informations du véhicule sélectionné
                Selectedvehicle = Selectedagency.search_vehicle(selected_vehicle)
                # Remplir les champs de saisie avec les informations du véhicule
                brand_entry.set(Selectedvehicle.get_brand())
                model_entry.set(Selectedvehicle.get_model())
                nseats_entry.set(Selectedvehicle.get_seats())
                license_plate_entry.set(Selectedvehicle.get_license_plate())
                nkilometers_entry.set(Selectedvehicle.get_mileage())
                price_entry.set(Selectedvehicle.get_price())
                combo_category.set(Selectedvehicle.get_category())
                combo_transmission.set(Selectedvehicle.get_transmission())
                combo_engine.set(Selectedvehicle.get_engine())
                self.setVehicleCalendar(calendar,Selectedvehicle)

                # Afficher la photo du véhicule
                photo_data = Selectedvehicle.get_picture()  # Récupérer les données binaires de la photo depuis la sélection
                imagedata = Image.open(BytesIO(photo_data))
                global photo
                photo = ImageTk.PhotoImage(imagedata)
                image_label = tk.Label(right_frame, image=photo, background="#f4811e")
                image_label.grid(row=12, column=0, columnspan=2)
            else:
                pass  
            
        def import_image():
            #Importer une image
            global filepath
            filepath= askopenfilename(title="Ouvrir une image",filetypes=[('png files','.png'),('all files','.*')])
            if not filepath:
                return
            imagedata = Image.open(str(filepath))
            global image_label
            global photo
            photo = ImageTk.PhotoImage(imagedata)
            image_label = tk.Label(right_frame, image=photo,background="#f4811e")
            image_label.grid(row=12, column=0, columnspan=2)

        def submit_vehicle():
            selection=combo_agency.get()
            if selection=="":
                tk.messagebox.showerror("Erreur","Veuillez sélectionner une agence")
                return
            try:
                with open(filepath, 'rb') as f:
                    picture_data = f.read()
            except:
                picture_data=Selectedvehicle.get_picture()
            if selection=="Toutes les agences":
                Selectedagency.set_id(db.db_getAgIdVehicle(Selectedvehicle))    
            dico={'brand':brand_entry.get(),'model':model_entry.get(),'seats':nseats_entry.get(),'license_plate':license_plate_entry.get(),'mileage':nkilometers_entry.get(),'price':price_entry.get(),'category':combo_category.get(),'transmission':combo_transmission.get(),'engine':combo_engine.get(),'id_agency':Selectedagency.get_id(),'picture':picture_data}
            empty=False
            for key in dico:
                if dico[key]=="":
                    empty=True
            if empty==True:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            else:
                newVehicle=VehLoc()
                newVehicle.setVehLoc(dico)
                db.db_insertVehicle(newVehicle)
                select_agency(None)
                # Effacer le contenu des champs de saisie
                clear_fields()
                
        def clear_fields():
            brand_entry.set("")
            model_entry.set("")
            nseats_entry.set("")
            license_plate_entry.set("")
            nkilometers_entry.set("")
            price_entry.set("")
            combo_category.set("")
            combo_transmission.set("")
            combo_engine.set("")
            calendar.calevent_remove("all")
            global image_label
            global filepath
            filepath=None
            try:
                Selectedvehicle=None
            except:
                pass
            try:    
                photo.__del__()
                image_label.grid_forget()
                image_label.destroy()
            except:
                pass

        def delete_vehicle():
            selected_index = parc_listbox.curselection()         
            if selected_index:
                confirmation=messagebox.askyesno("Suppression", f"Êtes-vous sûr de vouloir supprimer ce véhicule?\n Marque: {Selectedvehicle.get_brand()}\n Modèle: {Selectedvehicle.get_model()}\n Immatriculation: {Selectedvehicle.get_license_plate()}\n Agence: {Selectedvehicle.get_id_agency()}\n")
                if confirmation:
                    db.db_deleteVehicle(Selectedvehicle)
                    clear_fields()
                    select_agency(None)
                else:
                    return
            else:
                tk.messagebox.showerror("Erreur", "Veuillez sélectionner un véhicule") 
        
        self.build_page('parcManager')         
        self.parcManager_frame.configure(background="#f4811e")
        self.parcManager_frame.columnconfigure(0,weight=1,uniform='group1')
        self.parcManager_frame.columnconfigure(1, weight=1,uniform='group1')
        tk.Button(self.parcManager_frame, text="Retour",background="#f4811e",foreground="black", font=("Arial",10,"bold"), command=lambda: self.change_page("admin")).grid(row=10, column=0, columnspan=2)

        right_frame=tk.Frame(self.parcManager_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        left_frame=tk.Frame(self.parcManager_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ###########################################################
        ###FRAME DE DROITE : SAISIE DES INFORMATIONS DU VEHICULE###
        ###########################################################
        
        brand_entry=tk.StringVar()
        nkilometers_entry=tk.StringVar()
        model_entry=tk.StringVar()
        nseats_entry=tk.StringVar()
        price_entry=tk.StringVar()
        license_plate_entry=tk.StringVar()
        
        #Entries
        right_frame.configure(background="#f4811e")
        tk.Label(right_frame, text="Saisie/modification de véhicule", font=("Arial",15,"bold"),background="#f4811e",foreground="black").grid(row=0, column=0, columnspan=2,sticky='n')
        tk.Label(right_frame, text="Marque:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=1, column=0)
        tk.Entry(right_frame, textvariable=brand_entry, background="grey").grid(row=1, column=1)
        tk.Label(right_frame, text="Modèle:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=2, column=0)
        tk.Entry(right_frame, textvariable=model_entry, background="grey").grid(row=2, column=1) 
        tk.Label(right_frame, text="Nombre de places:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=3, column=0)
        tk.Entry(right_frame,textvariable=nseats_entry,background="grey").grid(row=3, column=1)
        tk.Label(right_frame, text="Immatriculation:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=4, column=0)
        tk.Entry(right_frame, textvariable=license_plate_entry, background="grey").grid(row=4, column=1)
        tk.Label(right_frame, text="Kilométrage:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=5, column=0)
        tk.Entry(right_frame, textvariable=nkilometers_entry, background="grey").grid(row=5, column=1)
        tk.Label(right_frame, text="Prix par jour:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=6, column=0)
        tk.Entry(right_frame, textvariable=price_entry,background="grey").grid(row=6, column=1)
        
        #Listes déroulantes
        tk.Label(right_frame, text="Catégorie:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=7, column=0)
        category_values = ["Berline", "SUV", "Coupé", "Cabriolet", "Espace", "Break", "Pick-up", "Luxe", "Utilitaire"]
        combo_category=ttk.Combobox(right_frame, values=category_values)
        combo_category.grid(row=7, column=1)
        tk.Label(right_frame, text="Type de transmission:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=8, column=0)
        transmission_values = ["Automatique", "Manuelle"]
        combo_transmission=ttk.Combobox(right_frame, values=transmission_values)
        combo_transmission.grid(row=8, column=1)
        tk.Label(right_frame, text="Type de moteur:", font=("Arial",10),background="#f4811e",foreground="black").grid(row=9, column=0)
        engine_values = ["Thermique", "Électrique", "Hybride"]
        combo_engine=ttk.Combobox(right_frame, values=engine_values)
        combo_engine.grid(row=9, column=1) 
        tk.Label(right_frame, text="Disponibilité:", font=("Arial",15,"bold"),background="#f4811e",foreground="black").grid(row=15, column=0, columnspan=2)        
        calendar = Calendar(right_frame, locale="fr_FR")
        calendar.grid(row=16,column=0,columnspan=2)
        import_button=tk.Button(right_frame, text="Importer une image",background="#f4811e",foreground="black", font=("Arial",10,"bold"), command=lambda: import_image())
        import_button.grid(row=13, column=0, columnspan=2, pady=10)
             
        # Créer un bouton pour valider la saisie du nouveau véhicule
        tk.Button(right_frame, text="Valider",background="#f4811e",foreground="black", font=("Arial",10,"bold"), command=lambda: submit_vehicle()).grid(row=14, column=0, pady=10)
        tk.Button(right_frame, text="Annuler",background="#f4811e",foreground="black", font=("Arial",10,"bold"), command=lambda: clear_fields()).grid(row=14, column=1, pady=10)
        
       
        #####################################################        
        ###FRAME DE GAUCHE : SELECTION DE L'AGENCE ET PARC###
        #####################################################
        
        left_frame.configure(background="#f4811e")
        
        for i in range(left_frame.grid_size()[0]):
            # Répartir l'espace disponible horizontalement
            left_frame.grid_columnconfigure(i, weight=1)  
        for i in range(left_frame.grid_size()[1]):
            # Répartir l'espace disponible verticalement
            left_frame.grid_rowconfigure(i, weight=1)

        #Agencies_list=db.db_getAgencies()
        tk.Label(left_frame, text="Sélectionner une agence", font=("Arial",15,"bold"),background="#f4811e",foreground="black").grid(row=0, column=0, columnspan=2, sticky='n')
        Agencies_list=db.db_getAgencies_location()
        Agencies_list.insert(0,"Toutes les agences")
        combo_agency=ttk.Combobox(left_frame, values=Agencies_list,background="grey")
        combo_agency.grid(row=1, column=0, columnspan=2, sticky='nsew')
        tk.Label(left_frame, text="Véhicules de l'agence", font=("Arial",15,"bold"),background="#f4811e",foreground="black").grid(row=2, column=0, columnspan=2)
        parc_listbox=tk.Listbox(left_frame,width=50, height=20,background="grey")
        parc_listbox.grid(row=3, column=0,rowspan=2, columnspan=2, sticky='nsew')
        tk.Button(left_frame,text="Supprimer véhicule",background="#f4811e",foreground="black", font=("Arial",10,"bold"), command=lambda: delete_vehicle()).grid(row=6, column=0, pady=10,columnspan=2)
        
        
        # Associer la fonction select_vehicle à l'événement de sélection dans la listbox
        parc_listbox.bind("<<ListboxSelect>>", select_vehicle)
        #Associer la fonction select_agency à l'événement de sélection dans la combobox
        combo_agency.bind("<<ComboboxSelected>>", select_agency)
                  
            
    ####################################
    ##### PAGE D'AFFICHAGE CLIENT ######
    ####################################
    
    def init_customer(self):
        def clean_frame():
            try:
                for widget in self.customer_frame.winfo_children():
                    if isinstance(widget, tk.PanedWindow) and widget != search_paned and widget!=title_window:
                        widget.destroy()
            except:
                pass     
             
        def select_agency(self):
            custagency=Agency()
            extract_agency(custagency)
            self.__selectedagency=custagency
            clean_frame()
            print_car(self,custagency)
                
        def search_button_click(self):
            selected_category = category_combobox.get()
            selected_motor = motor_combobox.get()
            passenger_count = int(passenger_spinbox.get())
            select_trans = automatic_checkbox_var.get()
            
            if selected_category.startswith('Toute'):
                selected_category = ''
            if selected_motor.startswith('Tout'):
                selected_motor= ''
                
            if select_trans:
                select_trans='Automatique'
            else:
                select_trans='Manuelle'
            
            clean_frame()
            searchedagency=Agency()
            extract_agency(searchedagency)
            copied_agency = copy.deepcopy(searchedagency)

            # Supprimer les éléments de la copie
            for car in searchedagency.get_parc():
                if car.get_seats() < passenger_count or selected_motor!='' and selected_motor!=car.get_engine() or selected_category != '' and selected_category != car.get_category() or select_trans == 'Automatique' and car.get_transmission() != select_trans:
                    copied_agency.remove_vehicle(car)
            print_car(self,copied_agency)
        
        def print_car(self,agency):
            car_panedwindow = tk.PanedWindow(self.customer_frame, orient=tk.VERTICAL)
            car_panedwindow.pack(fill=tk.BOTH)
            car_panedwindow.place(relheight=0.95, relwidth=0.8, anchor='nw', relx=0.2, rely=0.05)
            car_panedwindow.configure(background="#f4811e")

            # Création du Canvas à l'intérieur du PanedWindow
            canvas = tk.Canvas(car_panedwindow)
            car_panedwindow.add(canvas)

            # Création de la frame à l'intérieur du Canvas
            frame = tk.Frame(canvas)
            frame.configure(background="#f4811e")
            canvas.create_window((0, 0), window=frame, anchor=tk.NW)

            # Création de la barre de défilement pour le Canvas
            scrollbar = tk.Scrollbar(car_panedwindow, command=canvas.yview,bd=0,activebackground="black")
            scrollbar.configure(width=20)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Placer la barre de défilement à droite

            for i, car in enumerate(agency.get_parc()):
                createcar_frame(i, frame, car)
            # Configuration du scrolling dynamique
            frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.configure(yscrollcommand=scrollbar.set, background="#f4811e")
                
        def createcar_frame(i,master,car):
            car_frame = tk.Frame(master,bd=10)
            car_frame.configure(background="#f4811e")
            
            row = i // 2 + 2  # Calcul de la ligne en utilisant la division entière
            column = i % 2 + 1  # Calcul de la colonne en utilisant le modulo
            car_frame.grid(row=row, column=column,sticky='sewn')
            photo_data = car.get_picture()
            image = Image.open(BytesIO(photo_data))
            image = image.resize((350,200))
            photo = ImageTk.PhotoImage(image)
           
            image_label = tk.Label(car_frame, image=photo,background="#f4811e")
            image_label.image = photo
            image_label.grid(row=0, column=0,rowspan=2)

            infos_frame=tk.Frame(car_frame)
            infos_frame.configure(background="#f4811e")
            infos_frame.grid(row=0,column=1,sticky='w')
                # Marque et modèle
            ttk.Label(infos_frame, text=car.get_brand() + " " + car.get_model(), font=("Arial", 14, "bold"), background="black", foreground="#f4811e").grid(row=0, column=0, columnspan=4, padx=5, pady=5)
            

            # Catégorie
            ttk.Label(infos_frame, text="Catégorie:", background="#f4811e",font=("Arial",10,"bold")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
            ttk.Label(infos_frame, text=car.get_category(), background="#f4811e").grid(row=1, column=1, sticky="w", padx=5, pady=5)
           
            # Moteur
            ttk.Label(infos_frame, text="Moteur:", background="#f4811e",font=("Arial",10,"bold")).grid(row=1, column=2, sticky="w", padx=5, pady=5)
            ttk.Label(infos_frame, text=car.get_engine(), background="#f4811e").grid(row=1, column=3, sticky="w", padx=5, pady=5)

            # Transmission
            ttk.Label(infos_frame, text="Transmission:", background="#f4811e",font=("Arial",10,"bold")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
            ttk.Label(infos_frame, text=car.get_transmission(), background="#f4811e").grid(row=2, column=1, sticky="w", padx=5, pady=5)

            # Places
            ttk.Label(infos_frame, text="Places:", background="#f4811e",font=("Arial",10,"bold")).grid(row=2, column=2, sticky="w", padx=5, pady=5)
            ttk.Label(infos_frame, text=str(car.get_seats()), background="#f4811e").grid(row=2, column=3, sticky="w", padx=5, pady=5)
            

            # Prix par jour
            ttk.Label(infos_frame, text="Prix par jour:", background="#f4811e",font=("Arial",10,"bold")).grid(row=3, column=0, sticky="w", padx=5, pady=5)
            ttk.Label(infos_frame, text=str(car.get_price()) + "€", background="#f4811e").grid(row=3, column=1, sticky="w", padx=5, pady=5)
            
            tk.Button(infos_frame, text=f"RESERVER",foreground='#f4811e',background="black",font=("Arial",10,"bold"), command=lambda: reservation(car)).grid(row=4, column=0, columnspan=4, pady=10)
            
        def extract_agency(Agency):
            selection=comboagencies.get()
            indicechaine=selection.find("id: ")
            agenceid = ""
            indiceid = indicechaine + len("id: ")  # Indice après "id:"
            while indiceid < len(selection) and selection[indiceid].isdigit():
                agenceid += selection[indiceid]
                indiceid += 1
            if agenceid=="":
                return
            agenceid = int(agenceid)
            Agency.set_id(agenceid)
            parcplates=db.db_getAgency_parc(Agency)
            info=db.db_getAgency(Agency)
            Agency.set_phone(info[1])
            dico={'street':info[2],'zip_code':info[3],'city':info[4]}
            Agency.set_agency(dico)
            for plate in parcplates:
                voiture=VehLoc(license_plate=plate[0])
                carinfo=db.db_getVehicle(voiture)
                dico={'brand':carinfo[1],'model':carinfo[2],'seats':carinfo[3],'engine':carinfo[4],'transmission':carinfo[5],'category':carinfo[6],'price':carinfo[7],'mileage':carinfo[8],'id_agency':carinfo[9],'picture':carinfo[10]}
                voiture.setVehLoc(dico)
                Agency.add_vehicle(voiture)   
                
        def reservation(car):
            if self.__userlogged is None or self.__userlogged=='guest':
                tk.messagebox.showerror("Erreur","Veuillez vous connecter pour réserver un véhicule")
                self.change_page("login")
            else:
                self.__cartoreserve=car
                self.change_page("reservation")   
                    
        self.build_page('customer')   
        self.customer_frame.pack(fill=BOTH, expand=1) 
        self.customer_frame.configure(background="#f4811e")       
        #PanedWindow pour le titre
        title_window=PanedWindow(self.customer_frame, orient=tk.HORIZONTAL)
        title_window.configure(background="#f4811e")
        title_window.pack(fill=tk.X)
        title_window.place(relwidth=1,relheight=0.05,anchor='nw')
        tk.Label(title_window,text="Sevent Cars", font=("Arial",25,"bold"),background="#f4811e",foreground="black").pack(fill=BOTH,expand=1)
        #PanedWindow pour la recherche
        search_paned = tk.PanedWindow(self.customer_frame, orient=tk.VERTICAL, sashwidth=4, sashrelief=tk.RAISED)
        search_paned.configure(background="#f4811e")
        search_paned.pack(fill=tk.Y)
        search_paned.place(relwidth=0.2,relheight=0.95,rely=0.05, anchor='nw')
        search_frame=tk.Frame(search_paned)
        search_paned.add(search_frame)
        search_frame.configure(background="#f4811e")
        search_frame.place(rely=0.3,relx=0.1,anchor='nw')
    
        tk.Button(search_frame, text="Retour",background="#f4811e",foreground="black", font=("Arial",10,"bold"), command=lambda: self.change_page("login")).grid(row=25, column=0, columnspan=3, pady=10)     
        tk.Label(search_frame,text="D'où partez-vous ?", font=("Arial",15,"bold"),background="#f4811e",foreground="black").grid(row=0, column=0, sticky='n',columnspan=2)
        agencies=db.db_getAgencies_location()
        comboagencies=ttk.Combobox(search_frame,values=agencies)
        comboagencies.grid(row=1, column=0,columnspan=2,pady=10)

        # Catégorie de véhicule (Combobox)
        category_label = tk.Label(search_frame, text="Catégorie de véhicule:",background="#f4811e")
        category_label.grid(row=2, column=0, sticky="w")

        categories = ["Toute catégorie","Berline", "SUV", "Coupé", "Cabriolet", "Espace", "Break", "Pick-up", "Luxe", "Utilitaire"]
        category_combobox = ttk.Combobox(search_frame, values=categories)
        category_combobox.current(0)
        category_combobox.grid(row=2, column=1,sticky='nsew')
        
        # Moteur (Combobox)
        motor_label = tk.Label(search_frame, text="Moteur:",background="#f4811e")
        motor_label.grid(row=3, column=0, sticky="w")
        
        motor= ["Tout type","Thermique", "Électrique", "Hybride"]
        motor_combobox = ttk.Combobox(search_frame, values=motor)
        motor_combobox.current(0)
        motor_combobox.grid(row=3, column=1,sticky='nsew')
        # Boîte automatique (Checkbox)
        automatic_label = tk.Label(search_frame, text="Boîte automatique:",background="#f4811e")
        automatic_label.grid(row=4, column=0, sticky="w")

        automatic_checkbox_var = tk.BooleanVar()
        automatic_checkbox = tk.Checkbutton(search_frame, variable=automatic_checkbox_var)
        automatic_checkbox.configure(background="#f4811e")
        automatic_checkbox.grid(row=4, column=1,sticky='nsew')

        # Nombre de passagers (Spinbox)
        tk.Label(search_frame, text="Nombre de passagers:",background="#f4811e").grid(row=5, column=0, sticky="w")

        passenger_spinbox = tk.Spinbox(search_frame, from_=1, to=10)
        passenger_spinbox.grid(row=5, column=1,sticky='nsew')


        # Bouton de recherche
        tk.Button(search_frame, text="Rechercher", command=lambda: search_button_click(self),background="#f4811e",foreground="black", font=("Arial",10,"bold")).grid(pady=10,row=6, column=0,columnspan=2)
        
        comboagencies.bind("<<ComboboxSelected>>", lambda event: select_agency(self))
        
    ##########################################
    ##### PAGE D'AFFICHAGE DE RESERVATION#####
    ##########################################

    def init_reservation(self):      
        def retour():
            # Fermer la fenêtre principale
            self.__cartoreserve=None
            self.change_page("customer")
            
        def createRes_frame(master,car):
            car_frame = tk.Frame(master,bd=10)
            car_frame.configure(background="#f4811e")
            
            car_frame.grid(row=1, column=0, columnspan=2,sticky='sewn')
            photo_data = car.get_picture()
            image = Image.open(BytesIO(photo_data))
            image = image.resize((350,200))
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(car_frame, image=photo,background="#f4811e")
            image_label.image = photo
            image_label.grid(row=0, column=0,rowspan=2)

            infos_frame=tk.Frame(car_frame)
            infos_frame.configure(background="#f4811e")
            infos_frame.grid(row=0,column=1,sticky='w')
                # Marque et modèle
            brand_model_label = ttk.Label(infos_frame, text=car.get_brand() + " " + car.get_model(), font=("Arial", 14, "bold"), background="black", foreground="#f4811e")
            brand_model_label.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

            # Catégorie
            category_label = ttk.Label(infos_frame, text="Catégorie:", background="#f4811e",font=("Arial",10,"bold"))
            category_value_label = ttk.Label(infos_frame, text=car.get_category(), background="#f4811e")
            category_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            category_value_label.grid(row=1, column=1, sticky="w", padx=5, pady=5)

            # Moteur
            engine_label = ttk.Label(infos_frame, text="Moteur:", background="#f4811e",font=("Arial",10,"bold"))
            engine_value_label = ttk.Label(infos_frame, text=car.get_engine(), background="#f4811e")
            engine_label.grid(row=1, column=2, sticky="w", padx=5, pady=5)
            engine_value_label.grid(row=1, column=3, sticky="w", padx=5, pady=5)

            # Transmission
            transmission_label = ttk.Label(infos_frame, text="Transmission:", background="#f4811e",font=("Arial",10,"bold"))
            transmission_value_label = ttk.Label(infos_frame, text=car.get_transmission(), background="#f4811e")
            transmission_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
            transmission_value_label.grid(row=2, column=1, sticky="w", padx=5, pady=5)

            # Places
            seats_label = ttk.Label(infos_frame, text="Places:", background="#f4811e",font=("Arial",10,"bold"))
            seats_value_label = ttk.Label(infos_frame, text=str(car.get_seats()), background="#f4811e")
            seats_label.grid(row=2, column=2, sticky="w", padx=5, pady=5)
            seats_value_label.grid(row=2, column=3, sticky="w", padx=5, pady=5)

            # Prix par jour
            price_label = ttk.Label(infos_frame, text="Prix par jour:", background="#f4811e",font=("Arial",10,"bold"))
            price_value_label = ttk.Label(infos_frame, text=str(car.get_price()) + "€", background="#f4811e")
            price_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
            price_value_label.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        def valider_reservation():
            # Récupérer les informations saisies par l'utilisateur
            enddate = entry_enddate.get_date()
            startdate = entry_startdate.get_date()
            startdate_iso = datetime.strptime(str(startdate), "%Y-%m-%d").date()
            enddate_iso = datetime.strptime(str(enddate), "%Y-%m-%d").date()
            if calculer_prix_total()<=0 or startdate<datetime.now().date():
                messagebox.showerror("Erreur","Veuillez saisir des dates valides")
            else:
                    res=Reservation()
                    dico={'Vehicle':self.__cartoreserve,'User':self.__userlogged,'enddate':enddate_iso,'Agency':self.__selectedagency,'startdate':startdate_iso}
                    res.set_reservation(dico)
                    Dispo=db.db_checkResdispo(res)
                    if Dispo==True:
                        confirmation=messagebox.askyesno("Confirmation", f"Souhaitez-vous confirmer la réservation? :\nDate de début : {startdate}\nJusqu'au : {enddate} \nPrix total : {calculer_prix_total()} €")
                        if confirmation:
                            db.db_insertReservation(res)
                            adresse=self.__selectedagency.get_street()+", "+str(self.__selectedagency.get_zip())+" "+self.__selectedagency.get_city()
                            messagebox.showinfo("Confirmation", f"Votre réservation a bien été prise en compte.\n\nVous pouvez contacter l'agence pour plus d'informations.\n\nAdresse: {adresse} \n\nTéléphone: {self.__selectedagency.get_phone()}")
                            self.change_page("customer")
                        else:
                            return
                    else:
                        messagebox.showerror("Erreur","Le véhicule n'est pas disponible pour cette période")
                        return
                
        
        def calculer_prix_total():
            prix_par_jour = self.__cartoreserve.get_price()
            startdate=entry_startdate.get_date()
            enddate=entry_enddate.get_date()
            prixtotal = prix_par_jour * ((enddate-startdate).days +1)
            return prixtotal
        
        def afficher_prix_total(event):
            try:
                prix_total=calculer_prix_total()
                if prix_total <=0:
                    label_prix.config(text='Saisissez des dates valides')
                else:
                    label_prix.config(text=prix_total)  
            except ValueError:
                label_prix.config(text="")
                
        self.build_page('reservation')       
        self.reservation_frame.configure(background="#f4811e")
        createRes_frame(self.reservation_frame,self.__cartoreserve)
        tk.Label(self.reservation_frame, text="Disponibilité :",bg="#f4811e", fg="black", font=("Arial",15,"bold")).grid(row=2, column=0,columnspan=2, padx=10, pady=10)
        calendar=Calendar(self.reservation_frame, locale="fr_FR")
        self.setVehicleCalendar(calendar,self.__cartoreserve)
        calendar.grid(row=3,column=0,columnspan=2)
        
        label_startdate= tk.Label(self.reservation_frame,text="Date de début :",bg="#f4811e", fg="black")
        label_startdate.grid(row=4, column=0, padx=10, pady=10)
        entry_startdate = DateEntry(self.reservation_frame, selectmode="day", locale="fr_FR", date_pattern="dd/mm/yyyy", background="grey")
        entry_startdate.grid(row=4, column=1, padx=10, pady=10)
 
        label_enddate = tk.Label(self.reservation_frame, text="Jusqu'à :",bg="#f4811e", fg="black")
        label_enddate.grid(row=5, column=0, padx=10, pady=10)
        entry_enddate = DateEntry(self.reservation_frame,selectmode="day", locale="fr_FR", date_pattern="dd/mm/yyyy", background="grey")
        entry_enddate.grid(row=5, column=1, padx=10, pady=10)
        
        entry_enddate.bind('<<DateEntrySelected>>', lambda event: afficher_prix_total(event))

        label_prix_total = tk.Label(self.reservation_frame, text="Prix total :", bg="#f4811e", fg="black")
        label_prix_total.grid(row=6, column=0, padx=10, pady=10)

        label_prix = tk.Label(self.reservation_frame, text="", bg="#f4811e", fg="black")
        label_prix.grid(row=6, column=1, padx=10, pady=10)

    
        # Créer les boutons Valider et Retour
        button_valider = tk.Button(self.reservation_frame, text="Valider", bg="#f4811e", fg="black", command=lambda: valider_reservation())
        button_valider.grid(row=7, column=0, padx=10, pady=10)

        button_retour = tk.Button(self.reservation_frame, text="Retour", bg="#f4811e", fg="black", command=lambda: retour())
        button_retour.grid(row=7, column=1, padx=10, pady=10)
        
    ##########################################
    ##### PAGE DE GESTION DE RESA#############
    ##########################################
        
    def init_reservationManager(self):
        def search():
            for widget in self.reservationManager_frame.winfo_children():
                if isinstance(widget, tk.Listbox):
                    widget.destroy()
            # Code pour la recherche d'une réservation
            if combo_agencies.get()=='Toutes les agences':
                search_result=db.db_getAllReservations()
            else:
                if combo_agencies.get()!='':
                    id_ag=combo_agencies.get().split(" ")[-1]
                else:
                    id_ag=-1
                Agencysearched=Agency(id_agency=id_ag)
                Usersearched=User(username=username_entry.get())        
                Resasearched=Reservation()
                dico={'User':Usersearched,'Agency':Agencysearched}
                Resasearched.set_reservation(dico)
                search_result = db.db_searchRes(Resasearched)
            if hasattr(self, "listbox"):
                global listbox
                listbox.destroy()
            if search_result==[]:
                listbox = tk.Listbox(self.reservationManager_frame,height=10, width=40)
                listbox.grid(row=6, column=0, columnspan=2)
                listbox.insert(0, "Aucun résultat")
            else:         
                max_length = max(len(str(item)) for item in search_result)
                listbox = tk.Listbox(self.reservationManager_frame,height=20, width=max_length)
                listbox.grid(row=6, column=0, columnspan=2)
                tk.Button(self.reservationManager_frame, text="Retour du véhicule",background="#f4811e",foreground="black", font=("Arial",10,"bold"), command=lambda: car_arrival()).grid(row=7, column=0,columnspan=2 ,pady=5)
                for i in range(len(search_result)):
                    listbox.insert(i, search_result[i])
            
            def on_double_click(event):
                w = event.widget
                # Récupérer la position de l'élément sélectionné dans la liste
                index = int(w.curselection()[0])
                # Récupérer la valeur de l'élément sélectionné
                value = w.get(index)
                # Créer une Entry à la place de l'élément sélectionné et y insérer la valeur de l'élément
                edit_entry = tk.Entry(w,width=max_length)
                edit_entry.insert(0, value)
                edit_entry.grid(row=11+index, column=0, columnspan=2)
                # Supprimer l'élément sélectionné de la liste
                w.delete(index)
                
                def on_entry_keypress(event):
                    if event.keysym == "Return":
                        # Récupérer la nouvelle valeur de l'Entry
                        new_value = edit_entry.get()
                        search_result[index]= new_value
                        # Cacher l'Entry
                        edit_entry.grid_forget()
                        # Réinsérer la ligne modifiée dans la Listbox
                        listbox.insert(index, new_value)
                        # Mettre le focus sur la Listbox
                        listbox.focus_set()

                # Lier la touche "Entrée" à l'événement on_entry_keypress
                edit_entry.bind("<Return>", on_entry_keypress)
            
            # Lier le double-clic à chaque élément de la Listbox
            listbox.bind("<Double-Button-1>", on_double_click)
                        
            def submit_res():
                rows=[]
                for i in range(listbox.size()):
                    selection=listbox.get(i)
                    donnees=selection.split(" | ")
                    dico={'startdate':donnees[0].split(':')[1].strip(),'enddate':donnees[1].split(':')[1].strip(),'Vehicle':Vehicle(license_plate=donnees[2].split(':')[1].strip()),'Agency':Agency(id_agency=donnees[3].split(':')[1].strip()),'User':User(username=donnees[4].split(':')[1].strip()),'id':donnees[5].split(':')[1].strip()}
                    rows.append(dico)
                    ResatoUpdate=Reservation()
                    ResatoUpdate.set_reservation(dico)
                    db.db_insertReservation(ResatoUpdate)
                listbox.destroy()    
                search()
                tk.messagebox.showinfo("Modification","Les modifications ont bien été prises en compte")
                                
            def delete_res():
                selected_index = listbox.curselection()
                if selected_index:
                    selected_value = listbox.get(selected_index[0])
                    ResatoDelete=Reservation()
                    donnees=selected_value.split(" | ")
                    Veh=VehLoc(license_plate=donnees[2].split(':')[1].strip())
                    Ag=Agency(id_agency=donnees[3].split(':')[1].strip())
                    Us=User(username=donnees[4].split(':')[1].strip())
                    dico={'startdate':donnees[0].split(':')[1].strip(),'enddate':donnees[1].split(':')[1].strip(),'Vehicle':Veh,'Agency':Ag,'User':Us,'id':donnees[5].split(':')[1].strip()}
                    ResatoDelete.set_reservation(dico)
                    confirmation = messagebox.askyesno("Suppression", f"Êtes-vous sûr de vouloir supprimer la réservation {ResatoDelete.get_id()} ?")
                    if confirmation:
                        db.db_deleteReservation(ResatoDelete)
                        tk.messagebox.showinfo("Suppression",f"Suppression de la réservation {ResatoDelete.get_id()} effectuée")
                        infoscar=db.db_getVehicle(ResatoDelete.get_Vehicle())
                        dico={'brand':infoscar[1],'model':infoscar[2],'seats':infoscar[3],'engine':infoscar[4],'transmission':infoscar[5],'category':infoscar[6],'price':infoscar[7],'mileage':infoscar[8],'id_agency':infoscar[9],'picture':infoscar[10] }
                        Vehicle=Veh
                        Vehicle.setVehLoc(dico)
                        db.db_insertVehicle(Vehicle)
                        search()
                    else:
                        tk.messagebox.showinfo("Suppression", "La suppression de la réservation a été annulée.")
                        return 
                else:
                    tk.messagebox.showerror("Suppression","Aucun élément selectionné")
                search()   
            tk.Button(self.reservationManager_frame, text="Valider les changements", command=lambda:submit_res(), background="#f4811e",foreground="black", font=("Arial",10,"bold")).grid(row=8, column=0, padx=10)
            tk.Button(self.reservationManager_frame, text="Supprimer la réservation", command=lambda:delete_res(),background="#f4811e",foreground="black", font=("Arial",10,"bold")).grid(row=8, column=1, pady=10,padx=10)
        
        def car_arrival():
            selected_index = listbox.curselection()
            vehicleplate=listbox.get(selected_index[0]).split(" | ")[2].split(':')[1].strip()
            if selected_index:
                nbkilometers = simpledialog.askinteger("Arrivée du véhicule", "Quel est le kilométrage du véhicule à son arrivée?")
                Veh=VehLoc(license_plate=vehicleplate)
                infos=db.db_getVehicle(Veh)
                dico={'brand':infos[1],'model':infos[2],'seats':infos[3],'engine':infos[4],'transmission':infos[5],'category':infos[6],'price':infos[7],'mileage':infos[8],'id_agency':infos[9],'picture':infos[10] }
                Veh.setVehLoc(dico)
                Veh.arrival(nbkilometers)
                db.db_insertVehicle(Veh)
                db.db_deleteReservation(Reservation(id=listbox.get(selected_index[0]).split(" | ")[-1].split(':')[1].strip()))
            else:
                tk.messagebox.showerror("Erreur", "Veuillez sélectionner une réservation")
        
        self.build_page('reservationManager')        
        username_entry = tk.StringVar()
        
        self.reservationManager_frame.configure(background="#f4811e")
        tk.Label(self.reservationManager_frame, text="Gestion des réservations", font=("Arial",15),background="#f4811e",foreground="black").grid(row=0, column=0, columnspan=2)
        tk.Label(self.reservationManager_frame, text="Nom d'utilisateur",background="#f4811e",foreground="black", font=("Arial",10,"bold")).grid(row=3, column=0)
        tk.Entry(self.reservationManager_frame,textvariable=username_entry,background="grey").grid(row=3, column=1)
        agencies=db.db_getAgencies_location()
        agencies.insert(0,"Toutes les agences")
        combo_agencies=ttk.Combobox(self.reservationManager_frame, values=agencies)
        combo_agencies.grid(row=4, column=1)
        tk.Label(self.reservationManager_frame, text="Agence de location",background="#f4811e",foreground="black", font=("Arial",10,"bold")).grid(row=4, column=0)
        
        tk.Button(self.reservationManager_frame, text="Rechercher",background="#f4811e",foreground="black", font=("Arial",10,"bold"), command=lambda: search()).grid(row=5, column=0, columnspan=2,pady=5)
        tk.Button(self.reservationManager_frame, text="Retour",background="#f4811e",foreground="black", font=("Arial",10,"bold"), command=lambda: self.change_page("admin")).grid(row=25, column=0, columnspan=2,pady=5)