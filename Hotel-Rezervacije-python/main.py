from tkinter import *
from tkcalendar import DateEntry
import tkinter.messagebox
from tkinter import ttk
from tkinter import messagebox
import datetime
import time
import sqlite3
from login import *
import os
import numpy as np

from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


class StartPage:
    ime_db = "rezervacije.db"

    def __init__(self, root, user="2"):
        # def __init__(self, root, user):
        self.root = root
        self.root.configure(background="#5D6D7E")
        self.root.title("Registracija gosta")
        self.root.geometry("1100x900+1300+200")
        photo = PhotoImage(file="image.png")
        self.root.iconphoto(False, photo)

        self.conn = sqlite3.connect("rezervacije.db")
        self.cur = self.conn.cursor()

        """---------------------------------------------------------------------------------------"""

        """------------------------------------Menu Bar------------------------------"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar, tearoff=0)

        filemenu.add_command(label="Novo", command=self.reset)
        if user == "2":
            filemenu.add_command(label="Promjena cijena", command=self.azuCijena)

        filemenu.add_command(label="Ažuriraj...", command=self.azu_glavna)
        filemenu.add_separator()
        filemenu.add_command(label="Izlaz", command=root.destroy)
        menubar.add_cascade(label="Izbornik", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="O programu", command=self.oProg)
        menubar.add_cascade(label="Pomoć", menu=helpmenu)

        """-----------------LAYOUT APLIKACIJE---------------------------------"""

        ttk.Label(self.root, text="INFORMACIJE O GOSTU", style="Heading.TLabel").grid(
            row=0, column=1, pady=3
        )

        ttk.Label(self.root, text="Ime", padding="5").grid(row=1, column=0)
        self.ime_field = ttk.Entry(self.root)
        self.ime_field.grid(row=1, column=1, ipadx="100")
        self.ime_field.focus()
        self.ime_field.bind("<Return>", lambda e: self.prezime_field.focus_set())

        ttk.Label(self.root, text="Prezime", padding="5").grid(row=2, column=0)
        self.prezime_field = ttk.Entry(self.root)
        self.prezime_field.grid(row=2, column=1, ipadx="100")
        self.prezime_field.bind("<Return>", lambda e: self.datRod_field.focus_set())

        ttk.Label(self.root, text="Datum Rođenja", padding="5").grid(row=3, column=0)
        self.datRod_field = DateEntry(
            self.root, selectmode="day", date_pattern="dd-MM-yyyy"
        )
        self.datRod_field.grid(row=3, column=1, ipadx="100")
        self.datRod_field.bind("<Return>", lambda e: self.dol_field.focus_set())

        ttk.Label(self.root, text="Dolazak").grid(row=4, column=0)
        self.dol_field = DateEntry(
            self.root,
            selectmode="day",
            date_pattern="dd-MM-yyyy",
            style="dol.DateEntry",
        )
        self.dol_field.grid(row=4, column=1, ipadx="100")
        self.dol_field.bind("<Return>", lambda e: self.odl_field.focus_set())

        ttk.Label(self.root, text="Odlazak", padding="5").grid(row=5, column=0)
        self.odl_field = DateEntry(
            self.root,
            selectmode="day",
            date_pattern="dd-MM-yyyy",
            style="odl.DateEntry",
        )
        self.odl_field.grid(row=5, column=1, ipadx="100")
        self.odl_field.bind("<Return>", lambda e: self.email_field.focus_set())

        ttk.Label(self.root, text="Email", padding="5").grid(row=6, column=0)
        self.email_field = ttk.Entry(self.root)
        self.email_field.grid(row=6, column=1, ipadx="100")
        self.email_field.bind("<Return>", lambda e: self.adresa_field.focus_set())

        ttk.Label(self.root, text="Addresa", padding="5").grid(row=7, column=0)
        self.adresa_field = ttk.Entry(self.root)
        self.adresa_field.grid(row=7, column=1, ipadx="100")

        kat = []
        query1 = "SELECT kategorija FROM cijenikSoba"
        db_table = self.baza_pokreni(query1)
        for n in db_table:
            kat.append(n)

        ttk.Label(self.root, text="Vrsta sobe", padding="5").grid(row=8, column=0)
        self.kat_field = ttk.Combobox(
            self.root, state="readonly", style="comb.TCombobox"
        )
        self.kat_field["values"] = kat
        self.kat_field.current(0)
        self.kat_field.grid(row=8, column=1, ipadx="100")
        self.kat_field.bind("<Return>", lambda e: self.lezaj_field.focus_set())

        ttk.Label(self.root, text="Broj sobe").grid(row=9, column=0)
        self.soba_field = ttk.Combobox(
            self.root,
            state="readonly",
            postcommand=lambda: self.dodajSobe(self.kat_field, self.soba_field),
        )
        # self.soba_field['values'] = (self.dodajSobe())
        # self.soba_field.bind('<<ComboboxSelected>>', self.dodajSobe())
        self.soba_field.grid(row=9, column=1, ipadx="100")
        # self.cijena_field.grid(row=8, column=1, ipadx="100")self.broj_sobe()
        # self.cijena_field.bind('<Return>', lambda e: self.lezaj_field.focus_set())

        ttk.Label(self.root, text="Dodatnji ležaj", padding="5").grid(row=10, column=0)
        self.lezaj_field = ttk.Combobox(self.root, state="readonly")
        self.lezaj_field["values"] = ("DA", "NE")
        self.lezaj_field.current(1)
        self.lezaj_field.grid(row=10, column=1, ipadx="100")
        self.lezaj_field.bind("<Return>", lambda e: self.pet_field.focus_set())

        ttk.Label(self.root, text="Ljubimac u sobi").grid(row=11, column=0)
        self.pet_field = ttk.Combobox(self.root, state="readonly")
        self.pet_field["values"] = ("DA", "NE")
        self.pet_field.current(1)
        self.pet_field.grid(row=11, column=1, ipadx="100")
        self.pet_field.bind("<Return>", lambda e: submit.focus_set())

        self.message = ttk.Label(text="", foreground="white", background="#5D6D7E")
        self.message.grid(row=12, column=1)
        # root.after(2000, lambda: self.message.destroy())

        """---------------------------------BUTTONS----------------------------------------------"""

        sobaBtn = ttk.Button(
            self.root,
            text="Osvježi",
            style="refresh.TButton",
            command=lambda: self.birsanjeDatuma(),
        )
        sobaBtn.place(x=450, y=425)

        submit = ttk.Button(
            self.root,
            text="UNOS",
            style="TButton",
            command=lambda: self.dodaj_podatke(
                self.kat_field, self.dol_field, self.odl_field
            ),
        )
        submit.place(x=185, y=425)

        btnReset = ttk.Button(
            self.root, text="RESET", style="TButton", command=self.reset
        )
        btnReset.place(x=300, y=425)

        brisiBtn = ttk.Button(
            self.root,
            text="BRISANJE",
            width=15,
            command=lambda: self.brisanje_podataka(),
        )
        brisiBtn.place(x=165, y=725)

        brisiBtn = ttk.Button(
            self.root,
            text="RAČUN",
            width=10,
            style="racun.TButton",
            command=lambda: self.izdaj_racun(),
        )
        brisiBtn.place(x=350, y=725)

        """---------------------------------STILOVI------------------------------------------------------"""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "refresh.TButton",
            background="#2F4F4F",
            foreground="#F8F8FF",
            width=13,
            borderwidth=1,
            focusthickness=1,
            font=("Calibri", 11, "bold"),
            focuscolor="none",
        )
        style.map("refresh.TButton", background=[("active", "#708090")])

        style.configure(
            "racun.TButton",
            background="#620101",
            foreground="#F8F8FF",
            width=13,
            borderwidth=1,
            focusthickness=1,
            font=("Calibri", 11, "bold"),
            focuscolor="none",
        )
        style.map("racun.TButton", background=[("active", "#900101")])

        style.configure(
            "TButton",
            background="#370228",
            foreground="white",
            width=13,
            borderwidth=1,
            focusthickness=1,
            font=("Calibri", 11, "bold"),
            focuscolor="none",
        )
        style.map("TButton", background=[("active", "#720554")])

        style.configure(
            "Treeview.Heading",
            background="#3E3837",
            foreground="white",
            font=("Calibri", 13, "bold"),
        )
        style.map("Treeview.Heading", background=[("active", "#3E3837")])
        # style.configure("Treeview.Heading", font=('Calibri', 13, 'bold'))
        style.layout(
            "Treeview", [("Treeview.treearea", {"sticky": "nswe"})]
        )  # micanje bordera
        style.configure(
            "Treeview",
            highlightthickness=0,
            bd=0,
            font=("Calibri", 11),
            foreground="#4B0082",
            background="#DEDEDE",
        )
        style.map(
            "Treeview",
            background=[("selected", "#C1C1C1")],
            foreground=[("selected", "#4B0082")],
        )

        style.configure(
            "TLabel",
            font="Calibri 13",
            background="#5D6D7E",
            foreground="#DAA520",
            anchor="left",
        )
        style.configure("Heading.TLabel", font="times 17", background="#5D6D7E")

        style.configure(
            "dol.DateEntry",
            fieldbackground="#CDFBCD",
            background="#81FD81",
            foreground="#000000",
            arrowcolor="black",
        )
        style.configure(
            "odl.DateEntry",
            fieldbackground="#FFE4E1",
            background="#FF6C81",
            foreground="#000000",
            arrowcolor="black",
        )

        style.configure("TEntry", fieldbackground="#D8D1D9", foreground="#000000")

        style.configure("comb.TCombobox", fieldbackground="orange", background="white")

        """---------------------------------TREEVIEW----------------------------------------------------------"""
        self.tree = ttk.Treeview(
            self.root,
            selectmode="extended",
            column=["", "", "", "", "", ""],
            show="headings",
        )
        self.tree.column("#1", anchor=CENTER, stretch=NO, width=150)
        self.tree.heading("#1", text="Broj Rezervacije")
        self.tree.column("#2", anchor=CENTER, width=150)
        self.tree.heading("#2", text="Ime")
        self.tree.column("#3", anchor=CENTER, width=150)
        self.tree.heading("#3", text="Prezime")
        self.tree.column("#4", anchor=CENTER, width=100)
        self.tree.heading("#4", text="Dolazak")
        self.tree.column("#5", anchor=CENTER, width=100)
        self.tree.heading("#5", text="Odlazak")
        self.tree.column("#6", anchor=CENTER, width=100)
        self.tree.heading("#6", text="Broj sobe")

        self.tree.place(x=35, y=475)

        self.prikaz_podataka()

        """---------------------------------VRIJEME-----------------------------------------------"""

        def tick():
            datum = datetime.datetime.now()
            today = "{:%d - %m - %Y}".format(datum)

            mytime = time.strftime("%H:%M:%S")
            self.lblInfo.config(text=(mytime + " \n " + today))
            self.lblInfo.after(200, tick)

        self.lblInfo = Label(font=("arial", 20, "bold"), fg="#D8D1D9", bg="#5D6D7E")
        self.lblInfo.place(x=650, y=50)
        tick()

    def birsanjeDatuma(self):
        # brise sve rezervacije koje su na danasnji dan ili prije
        dat_danas = datetime.date.today()  # danasnji datum
        # danasnji datum plus 1 dan da je lakse za brisat iz baze
        dns_dat = dat_danas + datetime.timedelta(days=1)
        dat_danas1 = dns_dat.strftime("%d-%M-%Y")
        vrijeme_dns = datetime.datetime.now()

        conn = sqlite3.connect("rezervacije.db")
        cursor = conn.cursor()
        # brisanje rezervacija prije 12h
        if vrijeme_dns.hour > 12:
            query = "DELETE FROM infoGosti WHERE odl_fld < ?"
            cursor.execute(query, (dat_danas1,))
            conn.commit()
        else:
            pass

        self.prikaz_podataka()

    """---------------------------------AZURIRANJE CIJENA-----------------------------------------------"""

    def azuCijena(self):
        self.edit_root = Toplevel()
        self.edit_root.title("Ažuriranje")
        self.edit_root.geometry("350x450+1300+200")
        photo = PhotoImage(file="image.png")
        self.edit_root.iconphoto(False, photo)
        self.edit_root.configure(bg="#333333")
        # global kat_sobe

        kat = []
        query1 = "SELECT kategorija FROM cijenikSoba"
        db_table = self.baza_pokreni(query1)
        for n in db_table:
            kat.append(n)
        Label(
            self.edit_root, text="Vrsta sobe", bg="#333333", fg="#FFFFFF", pady=5
        ).grid(row=1, column=0)
        kat_sobe = ttk.Combobox(self.edit_root, state="readonly")
        kat_sobe["values"] = kat
        kat_sobe.grid(row=1, column=1, ipadx="35")

        Label(
            self.edit_root, text="Nova cijena sobe", bg="#333333", fg="#FFFFFF", pady=5
        ).grid(row=2, column=0)
        cijena_fld = Entry(self.edit_root)
        cijena_fld.grid(row=2, column=1, ipadx="35")

        submit1 = ttk.Button(
            self.edit_root,
            text="SPREMI",
            command=lambda: self.azuFukcija(cijena_fld.get(), kat_sobe.get()),
        )
        submit1.grid(row=3, column=1)

    def azuFukcija(self, cijena_fld, kat_sobe):
        # broj_rez = kat_sobe.get()
        query = "UPDATE cijenikSoba SET kat_cijena = ? " "WHERE kategorija = ?"
        parameters = (
            cijena_fld,
            kat_sobe,
        )
        self.baza_pokreni(query, parameters)
        self.edit_root.destroy()

    """---------------------------------DODAVANJE BROJEVA SOBA---------------------------------------"""

    def dodajSobe(
        self, kateg, soba
    ):  # IZBORNIK SLOBODNIH SOBA KOJE SE UPDATEA NA UNOS SVAKE SOBE I UPDATE S ODABIROM KATEGORIJE
        con = sqlite3.connect("rezervacije.db")
        cursor = con.execute("SELECT {} FROM kategorijeSoba".format(kateg.get()))
        brojevi = cursor.fetchall()

        query1 = "SELECT br_sobe FROM infoGosti"
        db_table = self.baza_pokreni(query1)
        kat = []
        for n in db_table:
            kat.append(n)
        sobe_slob = np.setdiff1d((brojevi), kat).tolist()
        soba["values"] = sobe_slob

    def loginScreen(self):
        root.destroy()
        newroot = Tk()
        app = Autentifikacija(newroot)
        newroot.mainloop()

    def cijene_sobe(self, kat_fld):
        # NAUCIO KAKO POVUCI CIJELI STUPAC IZ BAZE DA IZBACI REZULTAT ZA RACUNANJE REZULTATA
        # NITI NA STACKOVERFLOW NISAM NASAO KAKO IZVUCI SAMO JEDAN RED S OBZIROM NA ODABIR
        # NAPRAVLJENO NA OVAJ NACIN TAKO DA POSTOJI MOGUCNOST UPDATEANJA CIJENE SOBA PA AUTOMATSKI VUCE TRENUTNE CIJENE
        kat_sobe = kat_fld.get()

        con = sqlite3.connect("rezervacije.db")
        # zarez tako da ne bude tuple
        cursor = con.execute(
            "SELECT kat_cijena FROM cijenikSoba WHERE kategorija = ?", (kat_sobe,)
        )
        return int(cursor.fetchone()[0])

    def cijene_sobe1(
        self, kat_fld
    ):  # DODAO ISTU FUNKCIJU SAMO S MALO PRMJENA ZA EDITAT INFORMACIJE JER NIJE RADILO
        # ISPRAVNO I DODAO cijena_ukupno1
        # NAUCIO KAKO POVUCI CIJELI STUPAC IZ BAZE DA IZBACI REZULTAT ZA RACUNANJE REZULTATA
        # NITI NA STACKOVERFLOW NISAM NASAO KAKO IZVUCI SAMO JEDAN RED S OBZIROM NA ODABIR
        # NAPRAVLJENO NA OVAJ NACIN TAKO DA POSTOJI MOGUCNOST UPDATEANJA CIJENE SOBA PA AUTOMATSKI VUCE TRENUTNE CIJENE
        # kat_sobe = kat_fld.get()

        con = sqlite3.connect("rezervacije.db")
        cursor = con.execute(
            "SELECT kat_cijena FROM cijenikSoba WHERE kategorija = ?", (kat_fld,)
        )
        return int(cursor.fetchone()[0])

    def cijena_ukupno(
        self, kat_fld, dol_dat, odl_dat
    ):  # DODAO SAM kat_fld, dol_dat, odl_dat TAKO DA OVAJ FUNCTION
        # MOZE KORISTITI I DRUGE MOETODE KAO NPR AZURIRANJE
        self.razlika_datum = odl_dat.get_date() - dol_dat.get_date()
        self.ukupno_cijena = (int(self.cijene_sobe(kat_fld))) * abs(
            int(self.razlika_datum.days)
        )
        # abs jer za vece datume daje neg vrijednost

        return str(self.ukupno_cijena)

    def cijena_ukupno1(
        self, kat_fld, dol_dat, odl_dat
    ):  # DODAO SAM kat_fld, dol_dat, odl_dat TAKO DA OVAJ FUNCTION
        # MOZE KORISTITI I DRUGE MOETODE KAO NPR AZURIRANJE
        datum1 = datetime.datetime.strptime(dol_dat, "%d-%M-%Y").date()
        datum2 = datetime.datetime.strptime(odl_dat, "%d-%M-%Y").date()
        self.razlika_datum = datum2 - datum1
        self.ukupno_cijena = int(self.cijene_sobe1(kat_fld)) * abs(
            int(self.razlika_datum.days)
        )

        return str(self.ukupno_cijena)

    def baza_pokreni(self, query, parameters=()):
        with sqlite3.connect(self.ime_db) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def prikaz_podataka(self):
        elem = self.tree.get_children()
        for n in elem:
            self.tree.delete(n)
        query = "SELECT * FROM infoGosti"
        pod_baza = self.baza_pokreni(query)
        for data in pod_baza:
            self.tree.insert(
                "",
                END,
                text=data[0],
                values=(data[0], data[1], data[2], data[4], data[5], data[9]),
            )

    def provjera(self):
        return (
            len(self.ime_field.get()) != 0
            and len(self.prezime_field.get()) != 0
            and len(self.datRod_field.get()) != 0
            and len(self.email_field.get()) != 0
            and len(self.kat_field.get()) != 0
            and len(self.dol_field.get()) != 0
            and len(self.odl_field.get()) != 0
            and len(self.adresa_field.get()) != 0
            and len(self.soba_field.get()) != 0
            and len(self.lezaj_field.get()) != 0
            and len(self.pet_field.get()) != 0
        )

    def dodaj_podatke(self, kat_fld, dol_dat, odl_dat):
        dat_danas = datetime.date.today()
        if self.provjera():
            # provjera da dolazak mora biti danas i odlazak vise od danas
            if (dat_danas == self.dol_field.get_date()) and (
                dat_danas < self.odl_field.get_date()
            ):
                query = "INSERT INTO infoGosti VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?)"
                parameters = (
                    self.ime_field.get().capitalize(),
                    self.prezime_field.get().capitalize(),
                    self.datRod_field.get(),
                    self.dol_field.get(),
                    self.odl_field.get(),
                    self.email_field.get(),
                    self.adresa_field.get().capitalize(),
                    self.kat_field.get(),
                    str(self.soba_field.get()),
                    self.cijena_ukupno(kat_fld, dol_dat, odl_dat),
                    self.lezaj_field.get(),
                    self.pet_field.get(),
                )
                self.baza_pokreni(query, parameters)
                self.message["text"] = "Gost {} {} dodan!".format(
                    self.ime_field.get(), self.prezime_field.get()
                )
                self.root.after(
                    2000, lambda: self.message.grid_forget()
                )  # BRISANJE PORUKE NAKON 2 SEC
                self.message.grid(row=12, column=1)
                """Brisanje vrijednosti polja nakon unosa"""
                self.ime_field.delete(0, END)
                self.prezime_field.delete(0, END)
                self.datRod_field.delete(0, END)
                self.dol_field.delete(0, END)
                self.odl_field.delete(0, END)
                self.email_field.delete(0, END)
                self.adresa_field.delete(0, END)
                self.soba_field.set(
                    ""
                )  # NAKON UNOSA COMBOBOX POSTANE PRAZAN TAKO DA VISE NE PISE BROJ SOBE
                self.lezaj_field.set("")
                self.pet_field.set("")

            else:
                messagebox.showinfo("Pogrešan unos.", "Dolazak mora biti današnji dan!")

        else:
            messagebox.showinfo(
                "Pogrešan unos.", "Niste unijeli vrijednosti u sva polja!"
            )

        self.prikaz_podataka()

    def brisanje_podataka(self):
        # brisanje prijasnjeg teksta
        self.message["text"] = ""

        try:
            self.tree.item(self.tree.selection())["values"][1]

        except IndexError as e:
            self.message["text"] = "Molim odaberite polje za izbrisati!"
            return

        self.message["text"] = ""

        brRez = self.tree.item(self.tree.selection())["text"]
        query = "DELETE FROM infoGosti WHERE br_rez = ?"
        # zarez tkao da cita rezeracije s više znamenaka
        self.baza_pokreni(query, (brRez,))
        # brisanje poruke nakon 2 sekunde
        self.message["text"] = "Rezervacija broj {} je izbrisana!".format(brRez)
        self.root.after(2000, lambda: self.message.grid_forget())
        self.message.grid(row=12, column=1)

        self.prikaz_podataka()

    def azu_glavna(self):
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["values"][0]

        except IndexError as e:
            self.message["text"] = "Odabarite polje za ažurirati!"
            # root.after(2000, lambda: self.message.destroy())  # BRISANJE PORUKE NAKON 2 SEC
            return

        self.edit_root = Toplevel()
        self.edit_root.configure(background="#5D6D7E")
        self.edit_root.title("Ažuriranje ")
        self.edit_root.geometry("650x750+600+200")
        photo = PhotoImage(file="image.png")
        self.edit_root.iconphoto(False, photo)

        broj_rez = self.tree.item(self.tree.selection())["values"][0]
        query = "SELECT * FROM infoGosti WHERE br_rez = ?"
        # OVDJE NAUCIO KAKO KORISTITI TREE SELECTION ZA UZET VRIJEDNOSTI IZ BAZE PODATAKA
        rezStr = str(broj_rez)

        db_table = self.baza_pokreni(query, (rezStr,))
        for data in db_table:
            rodenje = datetime.datetime.strptime(data[3], "%d-%m-%Y").date()
            dolazak = datetime.datetime.strptime(data[4], "%d-%m-%Y").date()
            odlazak = datetime.datetime.strptime(data[5], "%d-%m-%Y").date()

            ttk.Label(self.edit_root, text="Ime").grid(row=1, column=0)
            ime_field1 = Entry(
                self.edit_root, textvariable=StringVar(self.edit_root, value=data[1])
            )
            ime_field1.grid(row=1, column=1, ipadx="100")
            ime_field1.focus()

            ttk.Label(self.edit_root, text="Prezime").grid(row=2, column=0)
            prezime_field1 = Entry(
                self.edit_root, textvariable=StringVar(self.edit_root, value=data[2])
            )
            prezime_field1.grid(row=2, column=1, ipadx="100")

            ttk.Label(self.edit_root, text="Datum Rođenja").grid(row=3, column=0)
            datRod_field1 = DateEntry(
                self.edit_root, selectmode="day", date_pattern="dd-MM-yyyy"
            )
            datRod_field1.set_date(rodenje)
            datRod_field1.grid(row=3, column=1, ipadx="100")

            ttk.Label(self.edit_root, text="Dolazak").grid(row=4, column=0)
            dol_field1 = Entry(
                self.edit_root,
                textvariable=StringVar(self.edit_root, value=data[4]),
                state="readonly",
            )
            # dol_field1.set_date(dolazak)
            dol_field1.grid(row=4, column=1, ipadx="100")

            ttk.Label(self.edit_root, text="Odlazak").grid(row=5, column=0)
            odl_field1 = DateEntry(
                self.edit_root, selectmode="day", date_pattern="dd-MM-yyyy"
            )
            odl_field1.set_date(odlazak)
            odl_field1.grid(row=5, column=1, ipadx="100")

            ttk.Label(self.edit_root, text="Email").grid(row=6, column=0)
            email_field1 = Entry(
                self.edit_root, textvariable=StringVar(self.edit_root, value=data[6])
            )
            email_field1.grid(row=6, column=1, ipadx="100")

            ttk.Label(self.edit_root, text="Addresa").grid(row=7, column=0)
            adresa_field1 = Entry(
                self.edit_root, textvariable=StringVar(self.edit_root, value=data[7])
            )
            adresa_field1.grid(row=7, column=1, ipadx="100")

            kat = []
            query = "SELECT kategorija FROM cijenikSoba"
            db_table = self.baza_pokreni(query)
            for n in db_table:
                kat.append(n)

            ttk.Label(self.edit_root, text="Vrsta sobe").grid(row=8, column=0)
            kat_field1 = ttk.Combobox(self.edit_root, state="readonly")
            kat_field1["values"] = kat
            # kat_field1.current(data[8])    # NE MOGU POVUCI TRENUTNU KATEGORIJU SOBE IZ BAZE PA SM STAVIO JOS JEDAN ENTRY DI PISE
            kat_field1.grid(row=8, column=1, ipadx="55")
            kat_field0 = Entry(
                self.edit_root,
                textvariable=StringVar(self.edit_root, value=data[8]),
                state="readonly",
            )
            kat_field0.grid(row=8, column=3, padx=5)

            ttk.Label(self.edit_root, text="Broj sobe").grid(row=9, column=0)
            soba_field1 = ttk.Combobox(
                self.edit_root,
                state="readonly",
                postcommand=lambda: self.dodajSobe(kat_field1, soba_field1),
            )
            soba_field1.grid(row=9, column=1, ipadx="55")
            soba_field0 = Entry(
                self.edit_root,
                textvariable=StringVar(self.edit_root, value=data[9]),
                state="readonly",
            )
            soba_field0.grid(row=9, column=3)

            ttk.Label(self.edit_root, text="Dodatnji ležaj").grid(row=10, column=0)
            lezaj_field1 = ttk.Combobox(self.edit_root, state="readonly")
            lezaj_field1["values"] = ("DA", "NE")
            Entry(
                self.edit_root,
                textvariable=StringVar(self.edit_root, value=data[11]),
                state="readonly",
            ).grid(row=10, column=3)
            lezaj_field1.grid(row=10, column=1, ipadx="100")

            ttk.Label(self.edit_root, text="Ljubimac u sobi").grid(row=11, column=0)
            pet_field1 = ttk.Combobox(self.edit_root, state="readonly")
            pet_field1["values"] = ("DA", "NE")
            Entry(
                self.edit_root,
                textvariable=StringVar(self.edit_root, value=data[12]),
                state="readonly",
            ).grid(row=11, column=3)
            pet_field1.grid(row=11, column=1, ipadx="100")
            # provjera ako gost ostaje u istoj sobi
            if len(kat_field1.get()) == 0:
                kat_field1 = kat_field0
                soba_field1 = soba_field0

            submit1 = ttk.Button(
                self.edit_root,
                text="SPREMI",
                width=7,
                command=lambda: self.azu_podatke(
                    ime_field1.get(),
                    prezime_field1.get(),
                    datRod_field1.get(),
                    dol_field1.get(),
                    odl_field1.get(),
                    email_field1.get(),
                    adresa_field1.get(),
                    kat_field1.get(),
                    soba_field1.get(),
                    lezaj_field1.get(),
                    pet_field1.get(),
                ),
            )
            submit1.place(x=150, y=300)

        self.edit_root.mainloop()

    def azu_podatke(
        self,
        ime_field1,
        prezime_field1,
        datRod_field1,
        dol_field1,
        odl_field1,
        email_field1,
        adresa_field1,
        kat_field1,
        soba_field1,
        lezaj_field1,
        pet_field1,
    ):
        # NAUCIO KAKO AZURIRATI SAMO DOREDENE VRIJEDNOSTI POLJA S OBZIROM KOJA REZERVACIJA JE SELECTANA
        broj_rez = self.tree.item(self.tree.selection())["values"][0]
        query = (
            "UPDATE infoGosti SET ime_fld=?, prez_fld=?, dat_rod=?, dol_fld=?, odl_fld=?, mail_fld=?, adr_fld=?, kat_sobe=?, "
            "br_sobe=?, cijena_uk=?, lezaj_fld=?, ljub_fld=? WHERE br_rez = ?"
        )
        parameters = (
            ime_field1.capitalize(),
            prezime_field1.capitalize(),
            datRod_field1,
            dol_field1,
            odl_field1,
            email_field1,
            adresa_field1.capitalize(),
            kat_field1,
            str(soba_field1),
            self.cijena_ukupno1(kat_field1, dol_field1, odl_field1),
            lezaj_field1,
            pet_field1,
            broj_rez,
        )
        self.baza_pokreni(query, parameters)
        self.edit_root.destroy()

        self.message["text"] = "Informacije o gostu {} {} su uspješno ažurirane".format(
            ime_field1, prezime_field1
        )
        self.root.after(2000, lambda: self.message.grid_forget())
        self.message.grid(row=12, column=1)
        self.prikaz_podataka()

    """---------------------------------------------------------------------------------------"""

    def oProg(self):
        messagebox.showinfo(
            "Hotel app",
            "Aplikacija za vođenje evidencije gosti u hotelu.\nNapravio: Ivan Senković",
        )

    def reset(self):
        self.ime_field.delete(0, "end")
        self.prezime_field.delete(0, "end")
        self.datRod_field.delete(0, "end")
        self.email_field.delete(0, "end")
        self.adresa_field.delete(0, "end")

    def izdaj_racun(self):
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["values"][0]

        except IndexError as e:
            self.message["text"] = "Odaberite rezervaciju za izdati račun!"
            return

        broj_rez = self.tree.item(self.tree.selection())["values"][0]
        query = "SELECT * FROM infoGosti WHERE br_rez = ?"
        # OVDJE NAUCIO KAKO KORISTITI TREE SELECTION ZA UZET VRIJEDNOSTI IZ BAZE PODATAKA
        rezStr = str(broj_rez)

        db_table = self.baza_pokreni(query, (rezStr,))
        for data in db_table:

            if data[11] == "DA":
                lezaj_cijena = 30
                lez_kol = 1
            else:
                lezaj_cijena = 0
                lez_kol = 0
            if data[12] == "DA":
                pet_cijena = 30
                pet_kol = 1
            else:
                pet_cijena = 0
                pet_kol = 0

            # drawString(50, h - 130, "Ime:")
            tableData1 = [
                ["Ime gosta", "", "", str(data[1] + " " + data[2])],
                ["Broj sobe", "", "", data[9]],
            ]
            style1 = TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("SPAN", (2, 1), (-2, -1)),
                    ("SPAN", (2, 0), (-2, 0)),
                    ("BOTTOMPADDING", (0, 1), (-1, -1), 15),
                ]
            )

            datum1 = datetime.datetime.strptime(data[4], "%d-%M-%Y").date()
            datum2 = datetime.datetime.strptime(data[5], "%d-%M-%Y").date()
            razlika = datum2 - datum1
            raz = abs(int(razlika.days))
            tableData = [
                ["Usluga", "Kolicina", "Cijena", "Ukupna Cijena"],
                ["Smještaj", raz, int(data[10] / raz), data[10]],
                [
                    "Dodatni ležaj: " + str(data[11]),
                    lez_kol,
                    lezaj_cijena,
                    lezaj_cijena,
                ],
                ["Ljbimac u sobi: " + str(data[12]), pet_kol, pet_cijena, pet_cijena],
                ["", "", "", ""],
                [
                    "UKUPNO",
                    "",
                    "",
                    "=   " + str(data[10] + lezaj_cijena + pet_cijena) + " €",
                ],
                [
                    "",
                    "",
                    "",
                    "=   " + str((data[10] + lezaj_cijena + pet_cijena) * 7.5) + " kn",
                ],
                ["Potpis", "", "", "__________________"],
            ]

            docu = SimpleDocTemplate("invoice{}.pdf".format(broj_rez), pagesize=A4)
            styles = getSampleStyleSheet()
            doc_style = styles["Heading2"]
            doc_style.alignment = 1
            title = Paragraph("Broj rezervacije: " + str(data[0]), doc_style)

            style = TableStyle(
                [
                    ("BOX", (0, 5), (-1, -1), 2, colors.black),
                    ("BOX", (0, 7), (-1, -2), 1, colors.red),
                    ("GRID", (0, 0), (3, 3), 1, colors.chocolate),
                    ("BACKGROUND", (0, 0), (3, 0), colors.darkgray),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("BACKGROUND", (0, 1), (-1, -5), colors.lightgrey),
                ]
            )
            self.message["text"] = "Račun za gosta {} {} izdan!".format(
                data[1], data[2]
            )
            self.root.after(2000, lambda: self.message.grid_forget())
            self.message.grid(row=12, column=1)

            table1 = Table(tableData1, style=style1)
            table = Table(tableData, style=style)
            docu.build([title, table1, table])


if __name__ == "__main__":

    root = Tk()
    app = StartPage(root)
    root.mainloop()
