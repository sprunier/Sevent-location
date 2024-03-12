from Apps import *
from Database import *

DB=DataBase('Location.db')
GUI=App(DB)
GUI.init_login()
GUI.state('zoomed')
GUI.mainloop()
