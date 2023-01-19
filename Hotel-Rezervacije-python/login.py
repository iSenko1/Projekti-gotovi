from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from main import *


class Autentifikacija:
    user = 'user'
    passw = 'user'

    managerUser = 'manager'
    managerPass = 'manager'

    def __init__(self, root):
        self.root = root
        photo = PhotoImage(file="login.png")
        self.root.iconphoto(False, photo)
        self.root.title('LOGIN KORISNIKA')
        self.root.configure(bg='#333333')
        self.root.geometry("340x440+1300+200")
        frame = tkinter.Frame(bg='#333333')

        '''Username i Password'''
        login_label = tkinter.Label(
            frame, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
        login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)

        Label(frame, text=' Korisničko ime ', bg='#333333', fg="#FFFFFF",
              font=("Arial", 16)).grid(row=1, column=0)
        self.username = ttk.Entry(frame)
        self.username.grid(row=1, column=1, pady=20)

        Label(frame, text=' Lozinka ', bg='#333333', fg="#FFFFFF",
              font=("Arial", 16)).grid(row=2, column=0)
        self.password = ttk.Entry(frame, show='*')
        self.password.grid(row=2, column=1, pady=20)

        # Button
        login_button = tkinter.Button(frame, text="Login", bg="#FF3399",
                        fg="#FFFFFF", font=("Arial", 16), command=self.login_user)
        login_button.grid(row=3, column=0, columnspan=2, pady=30)
        frame.pack()

    def login_user(self):

        '''Provjera točnosti unesenih podataka'''
        if self.username.get() == self.user and self.password.get() == self.passw:
            messagebox.showinfo(title="Uspješan login", message="Ulogirani ste u aplikaciju.")
            # Uništavanje ovog prozora ali popravit da se samo sakrije
            root.destroy()

            # Otvori novi prozor
            newroot = Tk()
            application = StartPage(newroot, self.user)
            newroot.mainloop()

        elif self.username.get() == self.managerUser and self.password.get() == self.managerPass:
            messagebox.showinfo(title="Uspješan login", message="Ulogirani ste u aplikaciju.")
            # Uništavanje ovog prozora ali popravit da se samo sakrije
            root.destroy()

            # Otvori novi prozor
            newroot = Tk()
            application = StartPage(newroot, self.managerUser)
            newroot.mainloop()

        else:
            if self.username.get() != self.user and self.password.get() != self.passw:
                messagebox.showerror(title="Greška",
                                     message="Neuspješan login. Molimo pokušajte ponovno!")

            elif self.password.get() != self.passw:
                messagebox.showerror(title="Greška",
                                     message="Pogrešna lozinka. Molimo pokušajte ponovno!")
                self.password.delete(0, END)

            elif self.username.get() != self.user:
                messagebox.showerror(title="Greška",
                                     message="Pogrešno korisničko ime. Molimo pokušajte ponovno!")

if __name__ == '__main__':
    root = Tk()
    root.geometry('425x185+1500+300')
    application = Autentifikacija(root)

    root.mainloop()

