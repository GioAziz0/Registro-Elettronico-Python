#Admin Menu

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
import SIS
import pickle
import string
import SetUser as SU
import SetDefaults as SD

def change_to_primary(event):
    event.widget.config(bootstyle="Primary")

def change_to_secondary(event):
    event.widget.config(bootstyle="Secondary")

class Admin():
    def __init__(self, prt=None):
        
        self.root = tb.Toplevel(prt)
        self.root.title('Registro Elettronico')
        self.root.geometry("800x600")
        self.root.minsize(550, 350)
        self.root.focus_set()
        #self.root.bind_class("Entry", "<Escape>", self.on_escape)
        try:
            self.root.iconbitmap('icons/MOD.ico')
        except Exception:
            pass

        self.parent = prt

        SIS.load1()
        
        SIS.all_students
        SIS.all_teachers

        self.frame1 = tb.Frame(self.root, bootstyle="secondary")
        self.frame2 = tb.Frame(self.root, bootstyle="info")
        self.frame3 = tb.Frame(self.root, bootstyle= "bg")

        self.frame1.pack(fill="x")
        self.frame2.pack(fill="x")
        self.frame3.pack(fill='both', expand=True)

        #Frame1
        self.C_Frame1()

        #Frame2
        self.C_Frame2()

        #Frame3
        self.C_Frame3()

        self.search_results_labels = []

        self.FindUser("None")

        self.root.bind_all("<Escape>", self.on_escape)

        self.root.bind("<Destroy>", self.Save)
        self.root.protocol("WM_DELETE_WINDOW", self.parent.close)

        self.root.mainloop()

        
    
    def on_escape(self, event):
        self.root.focus_set()

    def C_Frame1(self):
        self.frame1_1 = tb.Frame(self.frame1, bootstyle="secondary")
        self.frame1_1.pack(padx=5, pady=5)

        B_NewUser = tb.Button(self.frame1_1, text="Nuovo utente", bootstyle = "info", command=self.NewUser)
        B_NewUser.grid(row=0, column=1, padx=10)

        B_EditDefaults = tb.Button(self.frame1_1, text="Impostazioni", bootstyle = "info", command=self.EditDefaults)
        B_EditDefaults.grid(row=0, column=0, padx=10)

    def EditDefaults(self):
        SD.SetDefaults(self)
    
    def Nothing(self, event):
        ...
    
    def C_Frame2(self):
        self.frame2_1 = tb.Frame(self.frame2, bootstyle ="info")
        self.frame2_1.pack(padx=5, pady=5)

        L_FindUser1 = tb.Label(self.frame2_1, text="Cerca utente: ", bootstyle = "inverse-info")
        L_FindUser2 = tb.Label(self.frame2_1, text="per: ", bootstyle = "inverse-info")
        L_FindUser3 = tb.Label(self.frame2_1, text="in: ", bootstyle = "inverse-info")

        #self.IDtoFind = tk.StringVar()
        E_FindUser = tb.Entry(self.frame2_1, bootstyle = "primary")
        E_FindUser.bind("<FocusIn>", change_to_primary)
        E_FindUser.bind("<FocusOut>", change_to_secondary)
        E_FindUser.bind("<Key>", self.FindUserFormat)
        E_FindUser.bind("<KeyRelease>", self.FindUser)
        E_FindUser.bind("<Escape>", self.Nothing)

        self.E_FindUser = E_FindUser

        self.DelButtons = []
        self.users_class = tk.StringVar()
        RB_Students = tb.Radiobutton(self.frame2_1, text="Studenti", value='S', bootstyle = "primary-outline-toolbutton", variable=self.users_class)
        RB_Teachers = tb.Radiobutton(self.frame2_1, text="Insegnanti", value='T', bootstyle = "primary-outline-toolbutton", variable=self.users_class)
        self.users_class.set('S')
        self.users_class.trace_add("write", self.FindUser)

        self.parameter_to_find = tk.StringVar()
        RB_id = tb.Radiobutton(self.frame2_1, text="ID", value='I', bootstyle = "primary-outline-toolbutton", variable=self.parameter_to_find)
        RB_surname = tb.Radiobutton(self.frame2_1, text="Cognome", value='S', bootstyle = "primary-outline-toolbutton", variable=self.parameter_to_find)
        RB_class = tb.Radiobutton(self.frame2_1, text="Classe", value='C', bootstyle = "primary-outline-toolbutton", variable=self.parameter_to_find)
        self.parameter_to_find.set('S')
        self.parameter_to_find.trace_add("write", self.FindUser)


        L_FindUser1.grid(column=0, row=0, padx=5, pady=5)
        E_FindUser.grid(column=1, row=0, padx=5, pady=5)
        L_FindUser2.grid(column=2, row=0, padx=5, pady=5)
        RB_id.grid(column=3, row=0, padx=5, pady=5)
        RB_surname.grid(column=4, row=0, padx=5, pady=5)
        RB_class.grid(column=5, row=0, padx=5, pady=5)
        L_FindUser3.grid(column=6, row=0, padx=5, pady=5)
        RB_Students.grid(column=7, row=0, padx=5, pady=5)
        RB_Teachers.grid(column=8, row=0, padx=5, pady=5)

    def C_Frame3(self):
        self.canvas3 = tb.Canvas(self.frame3)
        self.frame3_0 = tb.Frame(self.canvas3)
        self.frame3_1 = tb.Frame(self.frame3_0)
        """
        self.frame3_id = tb.Frame(self.frame3_0)
        self.frame3_surname = tb.Frame(self.frame3_0)
        self.frame3_name = tb.Frame(self.frame3_0)
        self.frame3_class = tb.Frame(self.frame3_0)
        self.frame3_operations = tb.Frame(self.frame3_0)
        """
        
        self.scroll3 = tb.Scrollbar(self.frame3, orient="vertical", command=self.canvas3.yview, bootstyle="primary-round")
        self.scroll3.pack(side="right", fill="y")
        
        self.canvas3.configure(yscrollcommand=self.scroll3.set)
        self.scroll3.bind('<Configure>', lambda e: self.canvas3.configure(scrollregion=self.canvas3.bbox("all")))

        self.frame3_0_id = self.canvas3.create_window(0,0, window=self.frame3_0, anchor="nw")
        self.canvas3.bind('<Configure>', lambda e: self.canvas3.itemconfigure(self.frame3_0_id, width=e.width))

        self.canvas3.pack(expand=True, fill="both", side="left")
        self.frame3_1.pack(expand=True, fill="both")
        for col in range(5):
            self.frame3_1.grid_columnconfigure(col, weight=1)
        """
        self.frame3_id.pack(side="left", expand=True, fill="both", padx=(20,5), pady=5)
        self.frame3_surname.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.frame3_name.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.frame3_class.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.frame3_operations.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        """

    def FindUser(self, event, *args):

        T = False

        for label in self.search_results_labels:
            label.destroy()
        self.search_results_labels.clear()

        users_class = self.users_class.get()
        if users_class == 'S':
            self.users = SIS.all_students
        elif users_class == 'T':
            self.users = SIS.all_teachers
            T = True
        else:
            pass

        
        r=0

        for user in self.users:

            parameter_to_find = self.parameter_to_find.get()
            if parameter_to_find == 'I':
                parameter =  self.users[user].userID
            elif parameter_to_find == 'S':
                parameter =  self.users[user].surname
            elif parameter_to_find == 'C' and T == False:
                parameter =  self.users[user].cl
            elif parameter_to_find == 'C' and T==True:
                parameter =  self.users[user].clss


            #print(self.E_FindUser.get())
            #print(parameter)
            
            if self.E_FindUser.get().lower() in str(parameter).lower():
                #print("Trovato!")
                L_id = tb.Label(self.frame3_1, text=f"{self.users[user].userID}")
                L_surname = tb.Label(self.frame3_1, text=f"{self.users[user].surname}")
                L_name = tb.Label(self.frame3_1, text=f"{self.users[user].name}")

                B_delete = tb.Button(self.frame3_1, text="Elimina", bootstyle="Danger", width=5)
                B_delete.configure(command = lambda b=B_delete: self.user_delete(b))
                try:
                    L_class = tb.Label(self.frame3_1, text=f"{self.users[user].cl}")
                except AttributeError:
                    classes = [cl.upper() for cl in self.users[user].clss.keys()]
                    
                    classes_str = f"{classes[0]}"
                    for cl in classes[1:]:
                        classes_str += f", {cl}"

                    subjects = [s.upper() for s in self.users[user].subjects]
                    L_class = tb.Label(self.frame3_1, text=f"{classes_str}")

                L_id.grid(row=r, column=0, pady=5, sticky="ew", padx=20)
                L_surname.grid(row=r, column=1, pady=5, sticky="ew",padx=20)
                L_name.grid(row=r, column=2, pady=5, sticky="ew", padx=20)
                L_class.grid(row=r, column=3, pady=5, sticky="ew", padx=20)
                B_delete.grid(row=r, column=4, pady=5, sticky="ew", padx=20)

                temp = {
                    'button' : B_delete,
                    'id' : self.users[user].userID,
                    'L-id' : L_id,
                    'L-surname' : L_surname,
                    'L-name'  : L_name,
                    'L-class' : L_class
                }

                self.DelButtons.append(temp)

                self.search_results_labels.extend([L_id, L_surname, L_name, L_class, B_delete])

                r+=1

    def FindUserFormat(self, event):
        allowed = set(string.ascii_letters + string.digits + '-')
        if not ((len(event.widget.get())>30) and (event.keysym != 'BackSpace')):
            if not (event.char in allowed or event.keysym == 'BackSpace'):  # Verifica se il carattere non è una cifra
                return "break"
            #if not (event.keysym == 'BackSpace'):
                #if len(event.widget.get()) == 2:
                    #event.widget.insert(tk.END, "-")
        else:
            return "break"
        
        return None
    
    def NewUser(self):
        NewUserWindow = SU.NewUser(self, self.FindUser)
        
        
    def Save(self, *args):
        SIS.dump()

    def user_delete(self, btn):
        if self.users_class.get() == 'S':
            s = "L'eliminazione di uno studente comporta anche la sua eliminazione dagli appelli passati."
        else:
            s =""
        
        confirm = messagebox.askyesno("Conferma", f"Questa operazine è irreversibile. {s} Vuoi procedere?", icon="warning")
        if confirm:
            if self.users_class.get() == 'S':
                l = SIS.all_students
            else:
                l = SIS.all_teachers
            
            for b in self.DelButtons:
                if b['button'] == btn:
                    b['button'].destroy()
                    b['L-id'].destroy()
                    b['L-surname'].destroy()
                    b['L-name'].destroy()
                    b['L-class'].destroy()
                    
                    del l[b['id']]
        else:
            pass

    