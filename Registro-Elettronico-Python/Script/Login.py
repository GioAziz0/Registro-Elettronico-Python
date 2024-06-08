import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
import SIS
import AMenu
import TMenu
import string

class LoginWindow:
    def __init__(self):
        root = tb.Window(themename="journal")
        root.geometry("400x300")
        
        self.root = root

        self.root.title("Finestra di Login")
        self.root.iconbitmap('icons/Login.ico')
        
        # Frame per organizzare gli elementi
        self.frame = tb.Frame(root)
        self.frame.pack(expand=True)
        
        # Label e casella di testo per il nome utente
        self.username_label = tb.Label(self.frame, text="USER ID:")
        self.username_label.grid(row=0, column=0, sticky="e")
        self.username_entry = tb.Entry(self.frame)
        self.username_entry.grid(row=0, column=1)
        self.username_entry.bind('<Key>', self.UserNameFormat)
        
        # Label e casella di testo per la password
        self.password_label = tb.Label(self.frame, text="Password:")
        self.password_label.grid(row=1, column=0, sticky="e")
        self.password_entry = tb.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1)
        
        # Creazione del pulsante "Continua"
        self.continue_button = tb.Button(self.frame, text="Continua", command=self.on_continue)
        self.continue_button.grid(row=2, columnspan=2, pady=10)

        root.mainloop()
        
    def on_continue(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        SIS.load1()
        usertype, userid = username.split("-")

        if (usertype == "00") and (password == SIS.pswAdmin):
            self.root.withdraw()
            AMenu.Admin(self)
            return 0

        if (usertype == "01"):
            if (userid == "0000") and (password == SIS.pswAdmin):
                self.root.withdraw()
                TMenu.Teacher(SIS.AdminT, self)
                return 0
            
            else:
                for us in SIS.all_teachers:
                    usr = SIS.all_teachers[us]
                    if usr.userID == username:
                        if usr.password == password:
                            if usr.password == "firstlogin":
                                NP = NewPassword(self, usr)
                                return 0
                            else:
                                self.root.withdraw()
                                USER = TMenu.Teacher(usr, self)
                                return 0
                    
        NoUser = messagebox.showerror("Errore", "Username e/o password non validi")

                
    def close(self):
        self.root.destroy()

    def UserNameFormat(self, event):
        allowed = set(string.digits)
        if not ((len(event.widget.get())>6) and (event.keysym != 'BackSpace')):
            if not (event.char in allowed or event.keysym == 'BackSpace'):  # Verifica se il carattere non è una cifra
                return "break"
            if not (event.keysym == 'BackSpace'):
                if len(event.widget.get()) == 2:
                    event.widget.insert(tk.END, "-")
        else:
            return "break"
        
        return None

class NewPassword:
    def __init__(self, prt, user, r=False):
        self.root = tb.Toplevel(prt)
        self.root.title("Nuova password")
        self.root.geometry("400x300")
        self.root.iconbitmap('icons/Password.ico')
        self.root.grab_set()

        self.r = r
        self.user = user
        self.parent = prt

        if r == True:
            #self.root.bind("<Destroy>", self.parent.PasswordCallBack)
            self.root.bind("<Destroy>", self.CallBack)
        else:
            self.root.bind("<Destroy>", self.on_close)
            self.parent.root.attributes('-disabled', True)
        
        self.frame = tb.Frame(self.root)
        self.frame.pack(expand=True)

        self.newPass_label = tb.Label(self.frame, text="Nuova password:")
        self.newPass_label.grid(row=0, column=0, sticky="e")
        self.newPass_entry = tb.Entry(self.frame, show="*")
        self.newPass_entry.grid(row=0, column=1)
        
        # Label e casella di testo per la password
        self.confirm_label = tb.Label(self.frame, text="Conferma nuovo password:")
        self.confirm_label.grid(row=1, column=0, sticky="e")
        self.confirm_entry = tb.Entry(self.frame, show="*")
        self.confirm_entry.grid(row=1, column=1)

        self.continue_button = tb.Button(self.frame, text="Continua", command=self.on_continue)
        self.continue_button.grid(row=2, columnspan=2, pady=10)

    def on_continue(self):
        if (self.newPass_entry.get() == self.confirm_entry.get()):
            try:
                self.user.password = self.newPass_entry.get()

                self.root.destroy()
                if self.r == False:
                    SIS.dump()
                    self.parent.root.deiconify()
                    self.parent.root.attributes('-disabled', False)

            except ValueError as e:
                message = str(e)
                messagebox.showerror("Errore", f"Password non valida: {message}")
                self.root.focus_set()
                
            
            #else:
            #   self.password = self.user.password()
            #    self.root.quit()
        else:
            #self.root.lift()
            messagebox.showerror("Errore", "Le password non sono uguali")
            self.root.focus_set()
    

    def on_close(self, event):
        if event.widget == self.root:
            self.parent.root.attributes('-disabled', False)

    def CallBack(self, event):
        if event.widget == self.root:
            self.parent.PasswordCallBack()


        
def main():
    app = LoginWindow()
    
if __name__ == "__main__":
    main()
