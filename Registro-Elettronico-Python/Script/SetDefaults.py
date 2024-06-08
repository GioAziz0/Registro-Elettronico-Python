import SIS
import tkinter as tk
import ttkbootstrap as tb
import pickle
import Login

class SetDefaults:
    def __init__(self, prt):
        self.parent = prt
        self.root = tb.Toplevel(self.parent)
        self.root.title('Impostazioni')
        self.root.geometry("1200x600")
        self.root.minsize(450, 200)
        self.root.focus_set()
        try:
            self.root.iconbitmap('icons/Gear.ico')
        except Exception:
            pass

        self.frameT = tb.Frame(self.root, bootstyle="info")
        self.frameT.pack(fill="x")
        self.C_FrameT()

        self.classes = []
        self.subjects = []
        self.widgets = []

        self.frameC = tb.Frame(self.root, bootstyle="bg")
        self.frameC.pack(fill="both", expand=True)
        self.C_FrameC()

        

    def C_FrameT(self):
        Label = tb.Label(self.frameT, text = "Impostazioni", font = ("Arial", 15), bootstyle ="inverse-info")
        Label.pack(pady=10)

    def C_FrameC(self):
        
        self.frameC2 = tb.Frame(self.frameC, bootstyle="bg")
        self.frameC2.pack(fill="x", expand=True)

        self.sepC1C2 = tb.Separator(self.frameC, orient="horizontal")
        self.sepC1C2.pack(fill="x", padx=20)

        self.frameC1 = tb.Frame(self.frameC, bootstyle="bg")
        self.frameC1.pack(fill="both", expand=True)

        self.B_Confirm = tb.Button(self.frameC, text="Conferma modifiche", bootstyle="Success", command=self.ConfirmChanges)
        self.B_Confirm.pack()

        self.info = tb.Label(self.frameC, text = "Attenzione! La rimozione di classi utilizzate precedentemente comprometterà i dati correlati, \n come ore firmate e insegnanti o studenti associati a tale classe",
                             bootstyle = "Danger", justify='center')
        self.info2 = tb.Label(self.frameC, text = "Classi o materie con lo stesso nome verranno considerate una sola volta")

        self.info.pack()
        self.info2.pack()

        L_Classes = tb.Label(self.frameC1, text = "Classi: ")
        L_Subjects = tb.Label(self.frameC1, text = "Materie: ")
        L_Hours_X_Lesson = tb.Label(self.frameC1, text = "Ore per lezione: ")
        L_Password = tb.Label(self.frameC2, text = "Password per Admin: ")

        L_Classes.grid(row=0, column=0, padx=10, pady=20)
        L_Subjects.grid(row=1, column=0, padx=10, pady=20)
        L_Hours_X_Lesson.grid(row=2, column=0, padx=10, pady=20)
        L_Password.grid(row=0, column=0, padx=10, pady=20)
        
        self.C_FrameC1()

    def C_FrameC1(self):
        
        for widget in self.widgets:
            widget.destroy()


        self.C_FrameC1C()
        self.C_FrameC1S()

        self.lessons = tk.StringVar(value=str(len(SIS.hours_lessons)))
        self.C_lessons = tb.Spinbox(self.frameC1, from_= 1, to=24, width=5, state="readonly", textvariable=self.lessons)
        self.C_lessons.grid(row=2, column=1, padx=10, pady=20, sticky="w")

        self.L_Confirmed = tb.Label(self.frameC2, text="Password modificata correttamente", bootstyle = "Success")

        self.B_ChangePass = tb.Button(self.frameC2, text="Cambia password", command = self.SetPass, bootstyle="Info")
        self.B_ChangePass.grid(row=0, column=1, padx=10, pady=20, sticky="w")

    def SetPass(self):
        self.OldPassword = SIS.AdminT.password
        self.L_Confirmed.grid_forget()
        self.temp = Login.NewPassword(self, SIS.AdminT, r=True)

    def PasswordCallBack(self, event=None):
        self.NewPassword = SIS.AdminT.password
        SIS.pswAdmin = SIS.AdminT.password
        if self.NewPassword != self.OldPassword:
            ...
            self.L_Confirmed.grid(row=0, column=2, padx=10, pady=20, sticky="w")

            SIS.dumpD()


    def C_FrameC1C(self):
        
        self.frameC1C = tb.Frame(self.frameC1, bootstyle="bg")
        self.frameC1C.grid(row=0, column=1, sticky="w")

        #i=0
        for cl in sorted(SIS.all_classes):
            #i+=2
            #Str_Class = tk.StringVar(value=cl)
            E_Class = tb.Entry(self.frameC1C, text=cl, width=5)
            E_Class.delete(0, tk.END)
            E_Class.insert(0, cl)
            E_Class.configure(state="readonly")
            B_Delete = tb.Button(self.frameC1C, text="X", bootstyle="Danger", width=1)

            E_Class.pack(side="left", padx=(10,0))
            B_Delete.pack(side="left", padx=(0,10))
            B_Delete.configure(command=lambda b=B_Delete: self.Delete(b))

            temp = {
                "button" : B_Delete,
                "entry" : E_Class
            }

            self.classes.append(temp)

            #self.widgets.append(E_Class)
            #self.widgets.append(B_Delete)
        
        self.B_AddCl = tb.Button(self.frameC1C, text="Aggiungi", bootstyle="Primary", command=self.AddCl)
        self.B_AddCl.pack(side="right", padx=(0,10))
    
    def C_FrameC1S(self):
        #i=0
        self.frameC1S = tb.Frame(self.frameC1, bootstyle="bg")
        self.frameC1S.grid(row=1, column=1, sticky="w")

        for sb in sorted(SIS.all_subjects):
            #i+=2
            #Str_Class = tk.StringVar(value=sb)
            E_Subj = tb.Entry(self.frameC1S, text=sb, width=10)
            E_Subj.delete(0, tk.END)
            E_Subj.insert(0, sb)
            E_Subj.configure(state="readonly")
            B_Delete2 = tb.Button(self.frameC1S, text="X", bootstyle="Danger", width=1)

            E_Subj.pack(side="left", padx=(10,0))
            B_Delete2.pack(side="left", padx=(0,10))
            B_Delete2.configure(command=lambda b=B_Delete2: self.Delete2(b))

            temp = {
                "button" : B_Delete2,
                "entry" : E_Subj
            }

            self.subjects.append(temp)

            #self.widgets.append(E_Subj)
            #self.widgets.append(B_Delete2)

        self.B_AddSb = tb.Button(self.frameC1S, text="Aggiungi", bootstyle="Primary", command=self.AddSb)
        self.B_AddSb.pack(side="right", padx=(0,10))
    
    def Delete(self, btn):
        
        for button in self.classes:
            if button['button'] == btn:
                entry = button['entry']
                self.classes.remove(button)
        
        btn.destroy()
        entry.destroy()

    def Delete2(self, btn):
        
        for button in self.subjects:
            if button['button'] == btn:
                entry = button['entry']
                self.subjects.remove(button)

        btn.destroy()
        entry.destroy()

        self.C_FrameC1
    
    def AddCl(self):
        E_Class = tb.Entry(self.frameC1C, width=5)
        B_Delete = tb.Button(self.frameC1C, text="X", bootstyle="Danger", width=1)

        E_Class.pack(side="left", padx=(10,0))
        B_Delete.pack(side="left", padx=(0,10))
        B_Delete.configure(command=lambda b=B_Delete: self.Delete(b))

        temp = {
            "button" : B_Delete,
            "entry" : E_Class
        }

        self.classes.append(temp)
    
    def AddSb(self):
        E_Subj = tb.Entry(self.frameC1S, width=10)
        B_Delete2 = tb.Button(self.frameC1S, text="X", bootstyle="Danger", width=1)

        E_Subj.pack(side="left", padx=(10,0))
        B_Delete2.pack(side="left", padx=(0,10))
        B_Delete2.configure(command=lambda b=B_Delete2: self.Delete2(b))

        temp = {
            "button" : B_Delete2,
            "entry" : E_Subj
        }

        self.subjects.append(temp)

    def ConfirmChanges(self):
        clss = set()
        for cl in self.classes:
            if cl['entry'].get() != "":
                clss.add(cl['entry'].get())

        subjs = set()
        for sb in self.subjects:
            if sb['entry'].get() != "":
                subjs.add(sb['entry'].get())

        SIS.all_classes = [cl for cl in sorted(clss)]
        SIS.all_subjects = [sb for sb in sorted(subjs)]
        SIS.hours_lessons = set(range(1, int(self.lessons.get())+1))
        
        SIS.dumpD()

        self.root.destroy()