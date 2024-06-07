import SIS
import tkinter as tk
import ttkbootstrap as tb
import string
import pickle

class NewUser():
    def __init__(self, prt, refresh):
        self.refresh = refresh
        self.parent = prt
        self.root = tb.Toplevel(self.parent)
        self.root.title('Nuovo Utente')
        self.root.geometry("500x600")
        self.root.minsize(450, 200)
        self.root.focus_set()
        self.root.iconbitmap('icons/UserGear.ico')

        self.frameT = tb.Frame(self.root, bootstyle="info")
        self.frameB = tb.Frame(self.root, bootstyle="info")
        self.frameC = tb.Frame(self.root, bootstyle="bg")

        self.frameT.pack(fill="x")
        self.frameC.pack(fill="both", expand=True)
        self.frameB.pack(fill="x")

        self.C_FrameT()
        self.C_FrameB()
        self.C_FrameC()

        self.root.mainloop()

    def C_FrameT(self):
        Label = tb.Label(self.frameT, text = "Nuovo Utente", font = ("Arial", 15), bootstyle ="inverse-info")
        Label.pack(pady=10)

    def C_FrameB(self):
        self.B_prv = tb.Button(self.frameB, text = "← Indietro", bootstyle="info", command=self.B_Previous)
        self.B_next = tb.Button(self.frameB, text = "Avanti →", bootstyle="info", command=self.B_Next)
        self.B_prv.pack(side="left")
        self.B_next.pack(side="right")
        #B_next.configure(state="disabled")



    def C_FrameC(self):
        
        self.user_class = tk.StringVar()
        self.frameC_1 = tb.Frame(self.frameC, bootstyle="bg")
        self.frameC_1.pack(pady=20)

        self.toUnpack = []

        self.frameC_2S = tb.Frame(self.frameC, bootstyle="bg")
        self.frameC_2T = tb.Frame(self.frameC, bootstyle="bg")

        self.frameC_3 = tb.Frame(self.frameC, bootstyle="bg")


        self.C_frameC_1()
        self.C_frameC_2S()
        self.C_frameC_2T()
        
        self.frameCs = [self.frameC_1, self.frameC_2S, self.frameC_2T, self.frameC_3]

        self.CFrame = tk.IntVar()
        self.CFrame.trace_add("write", self.FrameC_Selector)
        self.CFrame.trace_add('write', self.A_Next)
        self.CFrame.trace_add('write', self.A_Previous)
        self.CFrame.set(1)

    def C_frameC_1(self):

        L_class = tb.Label(self.frameC_1, text="Tipologia Utente: ")
        self.frameC_1_1 = tb.Frame(self.frameC_1)
        RB_Students = tb.Radiobutton(self.frameC_1_1, text="Studente", value='S', bootstyle = "info-outline-toolbutton", variable=self.user_class)
        RB_Teachers = tb.Radiobutton(self.frameC_1_1, text="Insegnante", value='T', bootstyle = "primary-outline-toolbutton", variable=self.user_class)
        self.user_class.set('S')

        L_class.grid(column=0, row=0, padx=5, pady=5)
        self.frameC_1_1.grid(column=1, row=0, padx=5, pady=5)
        RB_Students.grid(column=1, row=0, padx=5, pady=5)
        RB_Teachers.grid(column=2, row=0, padx=5, pady=5)


        L_name = tb.Label(self.frameC_1, text="Nome: ")
        L_surname = tb.Label(self.frameC_1, text="Cognome: ")
        self.E_name = tb.Entry(self.frameC_1, bootstyle="primary")
        self.E_surname = tb.Entry(self.frameC_1, bootstyle="info")
        self.E_name.bind("<KeyRelease>", self.A_Next)
        self.E_surname.bind("<KeyRelease>", self.A_Next)

        L_name.grid(column=0, row=1, padx=5, pady=5)
        self.E_name.grid(column=1, row=1, padx=5, pady=5)
        L_surname.grid(column=0, row=2, padx=5, pady=5)
        self.E_surname.grid(column=1, row=2, padx=5, pady=5)

        self.E_name.bind("<Key>", self.SurName_Format)
        self.E_name.bind("<Escape>", lambda event: self.E_name.focus_set())

        self.E_surname.bind("<Key>", self.SurName_Format)
        self.E_surname.bind("<Escape>", lambda event: self.E_surname.focus_set())


    def C_frameC_2S(self):
        L_class = tb.Label(self.frameC_2S, text="Classe: ")
        L_class.pack(side="left", padx=(0,2))
        self.C_classS = tb.Combobox(self.frameC_2S, width=5)
        self.C_classS.bind("<<ComboboxSelected>>", self.A_Next)
        self.C_classS.configure(state="readonly")
        self.C_classS.pack(side="left")
        self.C_classS['values'] = SIS.all_classes

    def C_frameC_2T(self):

        self.canvas2T = tb.Canvas(self.frameC_2T)
        self.canvas2T.pack(side="left", fill="both", expand=True)

        self.scroll2T = tb.Scrollbar(self.frameC_2T, orient="vertical", command=self.canvas2T.yview, bootstyle="primary-round")
        self.scroll2T.pack(side="right", fill="y")

        self.canvas2T.configure(yscrollcommand=self.scroll2T.set)
        self.scroll2T.bind('<Configure>', lambda e: self.canvas2T.configure(scrollregion=self.canvas2T.bbox("all")))

        self.frameC_2TA = tb.Frame(self.canvas2T)

        self.canvas2T.create_window(0,0, window=self.frameC_2TA, anchor="nw")
        
        self.ExtraClasses = tk.IntVar()
        self.ExtraClasses.set(0)
        self.Classes = []

        self.frameC_2T0 = tb.Frame(self.frameC_2TA)
        self.frameC_2T0.pack(pady=10)

        self.L_class = tb.Label(self.frameC_2T0, text="1^classe:")
        self.L_class.grid(row=0, column=0, padx=(15,3), pady=10)
        self.C_class = tb.Combobox(self.frameC_2T0, width=5)
        self.C_class.bind("<<ComboboxSelected>>", self.A_Next)
        self.C_class.configure(state="readonly")
        self.C_class['values'] = SIS.all_classes
        self.C_class.grid(row=0, column=1)

        self.B_AddClass = tb.Button(self.frameC_2TA, text="Aggiungi classe", command=self.AddClass, bootstyle="info")

        self.D_frameC_2T()

        self.L_subject = tb.Label(self.frameC_2T0, text="1^materia: ")
        self.L_subject.grid(row=0, column=2, padx=(15,3), pady=10)
        self.C_subject = tb.Combobox(self.frameC_2T0, width=10)
        self.C_subject.bind("<<ComboboxSelected>>", self.A_Next)
        self.C_subject.configure(state="readonly")
        self.C_subject['values'] = SIS.all_subjects
        self.C_subject.grid(row=0, column=3)

        self.B_AddSub = tb.Button(self.frameC_2T0, text="Aggiungi materia")
        self.B_AddSub.configure(command= lambda b=self.B_AddSub: self.AddSub(b))
        self.B_AddSub.grid(row=0, column=4, padx=10)

        ClassDict = {
            'C-Class': self.C_class,
            'C-Subjects': [self.C_subject],
            'B-Subjects': self.B_AddSub,
            'Frame': self.frameC_2T0
        }
        self.Classes.append(ClassDict)


    def D_frameC_2T(self):
        self.B_AddClass.pack_forget()
        if self.ExtraClasses.get() <= 4:
            #self.B_AddClass.grid(row=1+self.ExtraClasses.get(), column=0, pady=10)
            self.B_AddClass.pack(pady=15)



    def AddClass(self):
        
        temp = self.ExtraClasses.get()
        if (temp<5):
            self.ExtraClasses.set(temp+1)

            self.frameC_2TN = tb.Frame(self.frameC_2TA)
            self.frameC_2TN.pack(pady=10)

            L_class = tb.Label(self.frameC_2TN, text=f"{temp+2}^classe: ")
            L_class.grid(row=0, column=0, padx=(15,3), pady=10)
            self.C_classE = tb.Combobox(self.frameC_2TN, width=5)
            self.C_classE.bind("<<ComboboxSelected>>", self.A_Next)
            self.C_classE.configure(state="readonly")
            self.C_classE.grid(row=0, column=1)
            self.C_classE['values'] = SIS.all_classes

            L_subjectE = tb.Label(self.frameC_2TN, text="1^materia: ")
            L_subjectE.grid(row=0, column=2, padx=(15,3), pady=10)
            self.C_subjectE = tb.Combobox(self.frameC_2TN, width=10)
            self.C_subjectE.bind("<<ComboboxSelected>>", self.A_Next)
            self.C_subjectE.configure(state="readonly")
            self.C_subjectE['values'] = SIS.all_subjects
            self.C_subjectE.grid(row=0, column=3)

            self.B_AddSubE = tb.Button(self.frameC_2TN, text="Aggiungi materia")
            self.B_AddSubE.configure(command= lambda b=self.B_AddSubE: self.AddSub(b))
            self.B_AddSubE.grid(row=0, column=4, padx=10)

            ClassDict = {
                'C-Class': self.C_classE,
                'C-Subjects': [self.C_subjectE],
                'B-Subjects': self.B_AddSubE,
                'Frame': self.frameC_2TN
            }
            self.Classes.append(ClassDict)

            self.D_frameC_2T()


        
        self.A_Next(None)

    def AddSub(self, button):
        
        for btn in self.Classes:
            if btn['B-Subjects'] == button:
                temp=len(btn['C-Subjects'])
                if temp < len(SIS.all_subjects):
                    tframe=btn['Frame']
                    L_subjectEN = tb.Label(tframe, text=f"{temp+1}^materia: ")
                    L_subjectEN.grid(row=temp, column=2, padx=(15,3), pady=10)
                    self.C_subjectEN = tb.Combobox(tframe, width=10)
                    self.C_subjectEN.bind("<<ComboboxSelected>>", self.A_Next)
                    self.C_subjectEN.configure(state="readonly")
                    self.C_subjectEN['values'] = SIS.all_subjects
                    self.C_subjectEN.grid(row=temp, column=3)

                    btn['C-Subjects'].append(self.C_subjectEN)

                    button.grid(row=temp, column=4, padx=10)

        self.A_Next(None)

    def B_Next(self):
        temp = self.CFrame.get()
        if  1 <= temp < 3:
            self.CFrame.set(temp+1)

    def B_Previous(self):
        temp = self.CFrame.get()
        if  1 < temp <= 3:
            self.CFrame.set(temp-1)

    def A_Next(self, event, *args):
        match self.CFrame.get():
            case 1:
                if (self.E_name.get() == "") or (self.E_surname.get() == ""):
                    self.B_next.configure(state="disabled")
                else:
                    self.B_next.configure(state="abled")
            case 2:
                if (self.user_class.get() == 'S'):
                    if self.C_classS.get() == "":
                        self.B_next.configure(state="disabled")
                    else:
                        self.B_next.configure(state="abled")
                if (self.user_class.get() == 'T'):
                    for cl in self.Classes:
                        if cl['C-Class'].get() != "":
                            for sb in cl['C-Subjects']:
                                if sb.get() != "":
                                    self.B_next.configure(state="abled")
                                else:
                                    self.B_next.configure(state="disabled")
                        else:
                            self.B_next.configure(state="disabled")
            case 3:
                self.B_next.configure(state="disabled")
    
    def C_FrameC_3(self):
        for widget in self.toUnpack:
            widget.destroy()
        
        name = self.E_name.get()
        surname = self.E_surname.get()
        user = self.user_class.get()
        subj = set()
        clss = dict()

        if user == 'T':
            for cl in self.Classes:
                for sb in cl['C-Subjects']:
                    subj.add(sb.get())

            for cl in self.Classes:
                temp = set()
                for sb in cl['C-Subjects']:
                    temp.add(sb.get())
                
                clss[cl['C-Class'].get()] = set(temp)
            
            self.New = SIS.Teacher(name, surname, subj, clss)
        
        if user == 'S':
            cl = self.C_classS.get()

            self.New = SIS.Student(name, surname, cl)


        self.L_id = tb.Label(self.frameC_3, text=f"{self.New}", font = ("Arial", 10), bootstyle="inverse-primary")
        self.L_id.pack(pady=10)

        self.B_confirm = tb.Button(self.frameC_3, text=f"Conferma", bootstyle="info", command=self.Confirm)
        self.B_confirm.pack()

        self.toUnpack = [self.L_id, self.B_confirm]

    def Confirm(self):

        user = self.user_class.get()
        if user == "S":
            SIS.all_students[self.New.userID] = self.New

            type, lfs = self.New.userID.split('-')
            SIS.lfs = lfs

        if user == "T":
            SIS.all_teachers[self.New.userID] = self.New

            type, lft = self.New.userID.split('-')
            SIS.lft = lft

        self.root.destroy()
        self.refresh(None)
        

        


    def A_Previous(self, event, *args):
        if self.CFrame.get() == 1:
            self.B_prv.configure(state="disabled")
        else:
            self.B_prv.configure(state="abled")

    def FrameC_Selector(self, event, *args):
        for frame in self.frameCs:
            frame.pack_forget()
        
        match self.CFrame.get():
            case 1:
                self.frameC_1.pack(pady=20)
            case 2:
                if self.user_class.get() == 'S':
                    self.frameC_2S.pack(pady=20)
                elif self.user_class.get() == 'T':
                    self.frameC_2T.pack(pady=20, expand=True, fill="both")
            case 3:
                self.C_FrameC_3()
                self.frameC_3.pack(pady=20)

    
    def SurName_Format(self, event):
        allowed = set(string.ascii_letters)
        if not (event.char in allowed or event.keysym == 'BackSpace'):  
                return "break"