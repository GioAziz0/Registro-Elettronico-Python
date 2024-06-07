import tkinter as tk
import ttkbootstrap as tb
import json
from ttkbootstrap import Style
import SIS
import pickle

SIS.load1()

CL1 = '#228B22'
CL2 = '#F5F5DC'
CL3 = '#FFFFF0'

def change_to_primary(event, BTstyle: str):
    event.widget.config(bootstyle=BTstyle)

def change_to_secondary(event, BTstyle: str):
    event.widget.config(bootstyle=BTstyle)

def on_entry(event):
    if event.widget.get() == "":
        event.widget.config(bg="white")
    else:
        event.widget.config(bg="#D2D2D2")

def disable_entry_input(event):
    return "break"

class Teacher():
    def __init__(self, user, prt):

        root = tb.Toplevel(prt)
        root.title('Registro Elettronico')
        root.geometry("800x600")
        #root.minsize(550, 350)
        root.focus_set()
        root.bind("<Escape>", lambda event: root.focus_set())
        root.iconbitmap('icons/Cap.ico')

        self.parent = prt
        root.protocol("WM_DELETE_WINDOW", self.parent.close)
        
        self.root = root

        self.user = user
        
        self.frame0 = tb.Frame(root, bootstyle="info")
        self.frame0.pack(ipady=5, fill="both")
        self.hello = tb.Label(self.frame0, text=f"Ciao, {self.user.name}!", font=("Helvetica", 25), bootstyle="inverse-info")
        self.hello.pack(side="left", padx=(20,2))

        #Main Frames
        
        self.frame2 = tb.Frame(root, bootstyle="primary")
        self.frame3 = tb.Frame(root, bootstyle= "bg")

        
        self.frame2.pack(fill="x")
        self.frame3.pack(fill='both', expand=True)

        #Frame2
        self.C_Frame2()

        #Frame3
        self.C_Frame3()

        self.root.mainloop()

    def C_Frame2(self):
        self.frame2_1 = tk.Frame(self.frame2)
        self.frame2_1.pack(side='left', padx=15, pady=(4,0))

        self.Frame3C = tk.StringVar()
        RBfA = tb.Radiobutton(self.frame2_1, text="Appello", value='A', bootstyle="bg-outline-toolbutton", variable = self.Frame3C) #RadioButton self.Frame2 Opzione1
        #RBfG = tb.Radiobutton(self.frame2_1, text="Voti", value='G', bootstyle="bg-outline-toolbutton", variable = self.Frame3C)
        #RBfE = tb.Radiobutton(self.frame2_1, text="Eventi", value='E', bootstyle="bg-outline-toolbutton", variable = self.Frame3C)
        self.Frame3C.set('A')
        

        RBfA.grid(column=0, row=0, padx=5, pady=5)
        #RBfG.grid(column=1, row=0, padx=5, pady=5)
        #RBfE.grid(column=2, row=0, padx=5, pady=5)
        
        self.Frame3C.trace_add("write", self.Frame3_Selector)

    def C_Frame3(self):
        self.frameA = tb.Frame(self.frame3, bootstyle="bg")
        self.frameG = tb.Frame(self.frame3, bootstyle="bg")
        self.frameE = tb.Frame(self.frame3, bootstyle="bg")
        
        """
        self.labelA = tk.Label(self.frameA, text="Frame A Content")
        self.labelG = tk.Label(self.frameG, text="Frame G Content")
        self.labelE = tk.Label(self.frameE, text="Frame E Content")

        self.labelA.pack()
        self.labelG.pack()
        self.labelE.pack()
        """

        self.Frame3_Selector()
    

    def Frame3_Selector(self, *args):
        selected_value = self.Frame3C.get()

        # Elimina e ricrea tutti i frame
        self.frameA.destroy()
        self.frameG.destroy()
        self.frameE.destroy()

        self.frameA = tb.Frame(self.frame3, bootstyle="bg")
        self.frameG = tb.Frame(self.frame3, bootstyle="bg")
        self.frameE = tb.Frame(self.frame3, bootstyle="bg")

        # Mostrare il frame selezionato
        if selected_value == 'A':
            self.C_FrameA()
            self.frameA.pack(fill='both', expand=True)
        elif selected_value == 'G':
            self.frameG.pack(fill='both', expand=True)
        elif selected_value == 'E':
            self.frameE.pack(fill='both', expand=True)


    def C_FrameA(self):

        self.frameA0 = tb.Frame(self.frameA, bootstyle="info")
        self.frameA0.pack(fill="x", pady=10)
        self.C_FrameA0()

        self.frameA1 = tb.Frame(self.frameA)
        self.frameA2 = tb.Frame(self.frameA)

        L_Hour = tb.Label(self.frameA1, text = "Ora", bootstyle="info")
        L_Teacher = tb.Label(self.frameA1, text = "Insegnante", bootstyle="info")
        L_Subject = tb.Label(self.frameA1, text = "Materia", bootstyle="info")
        L_Description = tb.Label(self.frameA1, text = "Descrzione", bootstyle="info")

        L_Hour.grid(row=0, column=0, padx=30, pady=10)
        L_Teacher.grid(row=0, column=1, padx=30, pady=10)
        L_Subject.grid(row=0, column=2, padx=30, pady=10)
        L_Description.grid(row=0, column=3, padx=30, pady=10)


    def C_FrameA0(self):
        frame1_1 = tb.Frame(self.frameA0, bootstyle="info")
        frame1_1.pack(pady=5, side="left")

        E_date = tb.DateEntry(frame1_1)
        E_date.entry.bind('<FocusIn>', lambda event: E_date.focus_set())
        E_date.pack(side="left", padx=(20,2))

        self.E_date = E_date

        classes = self.user.clss.keys()
        clss = [k.upper() for k in classes]

        L_class = tb.Label(frame1_1, text="Classe: ", bootstyle="inverse-info")
        L_class.pack(side="left", padx=(20,2))
        C_class = tb.Combobox(frame1_1, width=4)
        C_class.configure(state="readonly")
        C_class.pack(side="left")
        C_class['values'] = clss

        self.C_class = C_class
        
        """
        L_hour = tb.Label(frame1_1, text="Ora: ", bootstyle="inverse-primary")
        L_hour.pack(side="left", padx=(20,2))
        C_hour = tb.Combobox(frame1_1, width=2, bootstyle="primary")
        C_hour.configure(state="readonly")
        C_hour.pack(side="left")
        C_hour['values'] = SIS.hours_lessons

        self.C_hour = C_hour
        """

        self.B_confirmA = tb.Button(frame1_1, text="Conferma", bootstyle="primary-outline", command=self.ConfirmA)
        self.B_confirmA.pack(side="left", padx=(40,2))

        self.SignViewButtons = []
        self.ConfirmAWidgets = []
        self.ViewAWidgets = []

    def ConfirmA(self):
        
        self.frameA1.pack(fill="both", expand=True)
        self.frameA2.destroy()

        for widget in self.ConfirmAWidgets:
            widget.destroy()

        if self.C_class.get() == "":
            return 0
        
        self.cl = self.C_class.get()
        self.date = self.E_date.entry.get()
        
        SIS.load2(self.cl, self.date)
        
        i = 0
        for hour in SIS.lessons:
            i+=1

            L_HourN = tb.Label(self.frameA1, text = i)
            L_HourN.grid(row=i, column=0, padx=10, pady=10)
            
            try:
                teacher = str(hour['teacher']).strip()
                subject = hour['subject']
                description = hour['description'].strip()
                button = "Visualizza"
            except TypeError:
                teacher = "Ora non firmata"
                subject = ""
                description = ""
                button = "Firma"
            
            L_TeacherN = tb.Label(self.frameA1, text = teacher)
            L_TeacherN.grid(row=i, column=1, padx=10, pady=10)

            L_SubjectN = tb.Label(self.frameA1, text = subject)
            L_SubjectN.grid(row=i, column=2, padx=10, pady=10)

            L_DescriptionN = tb.Label(self.frameA1, text = description)
            L_DescriptionN.grid (row=i, column=3, padx=10, pady=10)

            B_Sign_View = tb.Button(self.frameA1, text=button, style="primary")
            B_Sign_View.configure(command=lambda b=B_Sign_View: self.Sign(b))
            B_Sign_View.grid(row=i, column=4, padx=10, pady=10)

            temp = {
                'hour' : i,
                'button' : B_Sign_View
            }

            self.SignViewButtons.append(temp)

            self.ConfirmAWidgets.append(L_TeacherN)
            self.ConfirmAWidgets.append(L_SubjectN)
            self.ConfirmAWidgets.append(L_DescriptionN)
            self.ConfirmAWidgets.append(L_HourN)
    
    def Sign(self, button):

        for btn in self.SignViewButtons:
            if btn['button']==button:
                self.hour = btn['hour']

        #print(f"Firma: {SIS.lessons} termina firma")
        if self.hour in SIS.lessons:
            try:
                s = Sign(self, self.user, self.cl, self.hour)
            except ValueError:
                #print("View")
                ...
        else:
            self.View(button)
            

    def View(self, button=None):

        studentsIDs = list(SIS.lessons[self.hour-1]['presences']) + list(SIS.lessons[self.hour-1]['absences'])
        students = []

        for s in studentsIDs:
            for st in SIS.all_students:
                if s == st:
                    students.append(SIS.all_students[s])


        self.frameA1.pack_forget()
        self.frameA2 = tb.Frame(self.frameA)
        self.frameA2.pack(expand=True, fill="both")
        self.canvasA_2 = tb.Canvas(self.frameA2)
        self.frameA_2 = tb.Frame(self.canvasA_2)
        #self.frameA_02 = tb.Frame(self.frameA_2, bootstyle="info")

        self.scrollA2 = tb.Scrollbar(self.frameA2, orient="vertical", command=self.canvasA_2.yview, bootstyle="primary") 
        self.scrollA2.pack(side="right", fill="y")

        self.canvasA_2.configure(yscrollcommand=self.scrollA2.set)
        self.scrollA2.bind('<Configure>', lambda e: self.canvasA_2.configure(scrollregion=self.canvasA_2.bbox("all")))

        self.frameA_2_id = self.canvasA_2.create_window(0,0, window=self.frameA_2, anchor="nw")
        #self.canvasA_2.bind('<Configure>', lambda e: self.canvasA_2.itemconfigure(self.frameA_2_id, width=e.width))

        self.canvasA_2.pack(side="left", fill="both")
        #self.frameA_02.pack()

        for widget in self.ViewAWidgets:
            widget.destroy()

        self.stds = []
        i=0
        for st in sorted(students, key=lambda x: x.surname):
            i+=1
            prs = "Presente"
            btprs = "Success"
            #if st.cl == self.cl:
            if st.userID in SIS.lessons[self.hour-1]['absences']:
                prs = "Assente"
                btprs = "Danger"
            L_surname = tb.Label(self.frameA_2, text=st.surname+" "+st.name)
            
            B_Presence = tb.Button(self.frameA_2, text=prs, command=..., bootstyle=btprs)
            B_Presence.config(command=lambda btn=B_Presence: self.SetPresence(btn))

            self.ViewAWidgets.append(L_surname)
            self.ViewAWidgets.append(B_Presence)
            L_surname.grid(row=i, column=0, padx=(50, 40), pady=10)
            B_Presence.grid(row=i, column=1, padx=10, pady=10)
            
            temp = {
                'student': st,
                'presence' : prs,
                'button' : B_Presence
            }

            self.stds.append(temp)

    def SetPresence(self, button):
        for st in self.stds:
            if st['button'] == button:
                student = st['student']
                prs = st['presence']
        
        if prs == "Assente":
            for id in SIS.lessons[self.hour-1]['absences'].copy():
                #print(f"Impostando su presente: {SIS.lessons[self.hour-1]['absences']}")
                if id == student.userID:
                    SIS.lessons[self.hour-1]['absences'].discard(id)
                    SIS.lessons[self.hour-1]['presences'].add(id)
            button.config(text="Presente", bootstyle="Success")
            
            for st in self.stds:
                if st['button'] == button:
                    st['presence'] = "Presente"

        else:
            SIS.lessons[self.hour-1]['absences'].add(student.userID)
            SIS.lessons[self.hour-1]['presences'].remove(student.userID)
            button.config(text="Assente", bootstyle="Danger")
            for st in self.stds:
                if st['button'] == button:
                    st['presence'] = "Assente"

        SIS.dumpT(self.cl, self.date)


    def C_FrameG():
        ...

    def C_FrameE():
        ...


class Sign():
    def __init__(self, prt, user, cl, hour):
        self.signW = tb.Toplevel(prt)
        self.signW.title('Firma')
        self.signW.geometry('300x300')
        self.signW.focus_set()
        
        self.prt = prt

        self.hour = hour
        self.cl = cl
        self.user = user

        self.L_Subject = tb.Label(self.signW, text="Materia: ")
        self.C_Subject = tb.Combobox(self.signW)
        self.C_Subject.configure(state="readonly")

        subjs = [s for s in user.clss[cl]]
        self.C_Subject['values'] = subjs

        self.L_description = tb.Label(self.signW, text="Descrivi la lezione: ")
        self.E_description = tb.Text(self.signW, width=50, height=5)

        self.L_Subject.pack(pady=10, padx=10)
        self.C_Subject.pack(pady=10, padx=10)
        self.L_description.pack(pady=10, padx=10)
        self.E_description.pack(pady=10, padx=10)

        self.B_confirm = tb.Button(self.signW, text="Conferma", command=self.Confirm)
        self.B_confirm.pack(pady=10, padx=10)

    def Confirm(self):
        self.user.sign(self.hour, self.cl, self.C_Subject.get(), self.E_description.get("1.0", tk.END))
        #print(f"Firmando: {SIS.lessons}")
        SIS.dumpT(self.cl, self.prt.date)
        self.signW.destroy()
        self.prt.ConfirmA()