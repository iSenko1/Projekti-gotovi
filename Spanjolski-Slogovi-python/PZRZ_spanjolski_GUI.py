from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
from tkinter import filedialog
import numpy as np

# pokrenuti 'pip install tk' za pokretanje tkinter modula!!!!!
testniTekst = 'Hoy es un buen día soleado y si no comienza a llover, iré en bicicleta. Mañana va a ser un nuevo día.'
# ovaj tekst iznad se može spremiti u .txt i otvoriti u GUI

VOWELS11 = 'aáeéiíoóuúü'
VOWELS11 += VOWELS11.upper()
CONSONANTS11 = 'bcdfghjklmnñpqrstvwxyz'
CONSONANTS11 += CONSONANTS11.upper()
bilabijalni = ["pr", "br", "pl", "bl", "fr", "fl"]
velarni = ["gr", "gl", "cr", "cl"]
zubni = ["dr", "tr", "Dr", "Tr"]
NIZ32 = ["ns", "bs", "Ns", "Bs"]
PRAVILO24 = ["tl", "tt", "ll"]
JAKI = list('aeoáéóAEOÁÉÓ')
SLABI = list('iíuúüIÍUÚÜ')
AKCENT_SLABI = list('íúüaeoáéóÍÚÜAEOÁÉÓ')
VOWELS11 = set(i for i in VOWELS11)
CONSONANTS11 = set(i for i in CONSONANTS11)
BILABIJALNI = []
for i in bilabijalni:
    BILABIJALNI.append(i.capitalize())
bilabijalni += BILABIJALNI

VELARNI = []
for i in bilabijalni:
    VELARNI.append(i.capitalize())
velarni += VELARNI


def pretvorba_2 ( ulazStr ):
    izlazStr = []
    counter = 0
    '''
    --------------------------------PRAVILA 4 / 8-----------------------------------------------
    '''
    i = 0
    while i < len(ulazStr):
        # print('pretvorb3 4 / 8')
        if i + 1 >= len(ulazStr):
            break
        if ulazStr[i] in JAKI and ulazStr[i + 1] in JAKI or \
                ulazStr[i] in AKCENT_SLABI and ulazStr[i + 1] in AKCENT_SLABI:
            izlazStr.append(''.join(ulazStr[:i + 1].split()))
            izlazStr.append(''.join(ulazStr[i + 1:].split()))
            i += 2
            break
        i += 1

    if izlazStr:
        return izlazStr

    '''
    --------------------------------PRAVILO 3-----------------------------------------------
    '''
    if len(ulazStr) > 4:
        i = 0
        # print('pretvorba 3.1 / 3.2')
        while i < len(ulazStr):
            if ulazStr[i] in VOWELS11:
                counter = i + 1
                prolaz = 0
                while ulazStr[counter] in CONSONANTS11:
                    prolaz += 1
                    counter += 1
                    if counter >= len(ulazStr):
                        break
                if ulazStr[counter] in VOWELS11 and prolaz > 2:
                    if ulazStr[i + 1:i + 3] in NIZ32:
                        izlazStr.append(''.join(ulazStr[:i + 3].split()))
                        izlazStr.append(''.join(ulazStr[i + 3:].split()))
                    else:
                        izlazStr.append(''.join(ulazStr[:counter - 2].split()))
                        izlazStr.append(''.join(ulazStr[counter - 2:].split()))
                    break
                else:
                    break
            i += 1
            if counter >= len(ulazStr) or i >= len(ulazStr):
                break
        if len(izlazStr) > 1:
            return izlazStr

    '''
    --------------------------------PRAVILO 2-----------------------------------------------
    '''
    i = 0
    while i < len(ulazStr):
        # pretvorba 2.1
        if ulazStr[i] in VOWELS11 and ulazStr[i + 1:i + 3] in bilabijalni and ulazStr[i + 3] in VOWELS11:
            izlazStr.append(''.join(ulazStr[:i + 1].split()))
            izlazStr.append(''.join(ulazStr[i + 1:].split()))
            if ulazStr[i + 3:] == '':
                break
        i += 1
    if izlazStr:
        return izlazStr
    # ------------------------------------------------------------------------------------
    i = 0
    while i < len(ulazStr):
        # print('pretvorba 2.2')
        if ulazStr[i] in VOWELS11 and ulazStr[i + 1:i + 3] in velarni and ulazStr[i + 3] in VOWELS11:
            izlazStr.append(''.join(ulazStr[:i + 1].split()))
            izlazStr.append(''.join(ulazStr[i + 1:].split()))
            if ulazStr[i + 3:] == '':
                break
        i += 1
    if len(izlazStr) > 1:
        return izlazStr
    # ------------------------------------------------------------------------------------
    i = 0
    while i < len(ulazStr):
        # print('pretvorba 2.3')
        if ulazStr[i] in VOWELS11 and ulazStr[i + 1:i + 3] in zubni and ulazStr[i + 3] in VOWELS11:
            izlazStr.append(''.join(ulazStr[:i + 1].split()))
            izlazStr.append(''.join(ulazStr[i + 1:].split()))
            if ulazStr[i + 3:] == '':
                break
        i += 1
    if len(izlazStr) > 1:
        return izlazStr
    # ------------------------------------------------------------------------------------
    i = 0
    while i < len(ulazStr):
        # print('pretvorba 2.4')
        if i + 2 >= len(ulazStr):
            break
        if ulazStr[i] in VOWELS11 and ulazStr[i + 1:i + 3] in PRAVILO24:
            izlazStr.append(''.join(ulazStr[:i + 1].split()))
            izlazStr.append(''.join(ulazStr[i + 1:].split()))
        i += 1
    if izlazStr:
        return izlazStr
    i = 0
    # ------------------------------------------------------------------------------------
    while i < len(ulazStr):
        # pretvorba 2.5
        if i + 3 >= len(ulazStr):
            break

        if ulazStr[i] in VOWELS11 and ulazStr[i + 1] in CONSONANTS11 and ulazStr[i + 2] in CONSONANTS11 \
                and ulazStr[i + 3] in VOWELS11:
            izlazStr.append(''.join(ulazStr[:i + 2].split()))
            izlazStr.append(''.join(ulazStr[i + 2:].split()))
            i += 4
            continue

        if i + 3 >= len(ulazStr):
            break
        i += 1

    if izlazStr:
        return izlazStr

    '''
    --------------------------------PRAVILO 1-----------------------------------------------
    '''
    i = 0
    while True:
        if i + 2 >= len(ulazStr):
            break
        if ulazStr[i] in VOWELS11 and ulazStr[i + 1] in CONSONANTS11 and ulazStr[i + 2] in VOWELS11:
            izlazStr.append(''.join(ulazStr[:i + 1].split()))
            izlazStr.append(''.join(ulazStr[i + 1:].split()))
            i += 3
            break
        if i + 2 >= len(ulazStr):
            break
        i += 1

    if izlazStr:
        return izlazStr

    if not izlazStr:
        #   ako nema nista u listi onda samo vrati pocetni rijeci
        izlazStr = izlazStr.append(ulazStr)
        return izlazStr


def pretvorbe_sve ( rijecTest ):
    output = []
    if "ü" in rijecTest:
        output.append(rijecTest)
        return output
    n = 0
    if pretvorba_2(rijecTest):
        output = pretvorba_2(rijecTest)
        if not output:
            return rijecTest
        while n < len(output):
            if len(output[n]) > 1:
                zadnje = pretvorba_2(output[n])
                if zadnje:
                    output.pop(n)
                    for i in zadnje[::-1]:
                        output.insert(n, i)
            n += 1
            if any(pretvorba_2(x) for x in output) and n == len(output):
                n = 0
        return output
    else:
        output.append(rijecTest)
        return output


from tkinter.filedialog import askopenfilename


class App(ttk.Frame):
    def __init__ ( self, root ):
        super().__init__()
        self.root = root
        self.root.configure(background = '#6D7B8A')
        self.root.title('Spanjolski pretvorba rijeci')

        # root.overrideredirect(True)
        self.root.geometry('700x500')
        self.grid(padx = 100, pady = 30)
        # self.grid_propagate(False)

        '''---------------------------------MENU---------------------------------'''
        menubar = Menu(self.root, background = 'blue', fg = 'white')

        file = Menu(menubar, tearoff = False)
        edit = Menu(menubar, tearoff = False)

        file.add_command(label = "Otvori...", command = self.unos_csv)
        file.add_command(label = "Spremi...", command = self.spremiKao)
        file.add_separator()
        file.add_command(label = "Izlaz", command = self.root.quit)

        edit.add_command(label = "Novo", command = self.reset_polja)
        edit.add_command(label = "Izreži", command = self.irezi)
        edit.add_command(label = "Kopiraj", command = self.kopiraj)

        menubar.add_cascade(label = "Datoteka", menu = file)
        menubar.add_cascade(label = "Edit", menu = edit)

        self.root.config(menu = menubar)

        '''---------------------------------POCETNA---------------------------------'''
        ttk.Label(self.root, text = "PRETVORBA RIJEČI", style = 'Heading.TLabel').grid(row = 0, column = 1, pady = 3)

        ttk.Label(self.root, text = "Unesite riječi", padding = '5').grid(row = 1, column = 0)
        self.unos_fld = ttk.Entry(self.root)
        self.unos_fld.grid(row = 1, column = 1, ipadx = '50')

        self.txtIzlaz = Text(self.root, width = 55, height = 15, borderwidth = 3, padx = 15, pady = 10,
                             yscrollcommand = 1, state = 'disabled'
                             )
        self.txtIzlaz.grid(row = 3, columnspan = 3, sticky = 'w', padx = 20, pady = 15)

        self.poruka = ttk.Label(text = '', foreground = 'white', background = '#6D7B8A')
        self.poruka.grid(row = 4, column = 1)

        '''---------------------------------BUTTONI---------------------------------'''
        unosBtn = ttk.Button(self.root, text = "Pretvorba", style = 'TButton',
                             command = lambda: self.btnPretvorba()
                             )
        unosBtn.grid(row = 2, column = 1, ipadx = '20')

        '''---------------------------------STILOVI---------------------------------'''
        style = ttk.Style()
        style.theme_use('clam')

        # labels
        style.configure('TLabel', font = "Courier 13", foreground = '#EFEDE7', background = '#6D7B8A', anchor = "left")
        style.configure('Heading.TLabel', font = "Consolas 21", background = '#6D7B8A', foreground = '#D6AD60')
        # polja za unos
        style.configure('TEntry', fieldbackground = '#DFDEDF', foreground = '#4B0404', padding = '3 3 3 3')
        # buttoni
        style.configure('TButton', background = '#D6AD60', foreground = '#343436', width = 13, borderwidth = 1,
                        focusthickness = 1, font = ('Calibri', 11, 'bold'), focuscolor = 'none'
                        )
        style.map('TButton', background = [('active', '#E1C38B')])

    '''---------------------------------FNUKCIJE---------------------------------'''

    def btnPretvorba ( self ):
        # korisnik može i zarez koristiti i ispisati ce se kako treba!
        izlazRijec = ''
        self.txtIzlaz.configure(state = 'normal')
        self.txtIzlaz.delete('1.0', END)
        self.txtIzlaz.configure(state = 'disabled')
        unosRijec = self.unos_fld.get()

        if unosRijec:
            for rijec in unosRijec.split():
                pretIzlaz = pretvorbe_sve(rijec)
                izlazRijec += '-'.join(pretIzlaz) + ' \n'
            self.txtIzlaz.configure(state = 'normal')
            self.txtIzlaz.insert(END, izlazRijec + '\n')
            self.txtIzlaz.configure(state = 'disabled')
        else:
            messagebox.showinfo('Pogrešan unos', 'Unesite jednu ili više riječi!')

    def unos_csv ( self ):
        #   otvara tekst dokument i onda ga odmah pretvori
        izlazRijec = ''
        self.txtIzlaz.configure(state = 'normal')
        self.txtIzlaz.delete('1.0', END)
        self.txtIzlaz.configure(state = 'disabled')

        f_types = [('Text Files', "*.txt"), ('All', "*.*")]
        tekstDat = askopenfilename(title = "Otvorite txt dokument...", filetypes = f_types)
        tekstDat = open(tekstDat, encoding = 'utf-8')
        data = tekstDat.read()

        for rijec in data.split():
            pretIzlaz = pretvorbe_sve(rijec)
            izlazRijec += '-'.join(pretIzlaz) + ' \n'
        self.txtIzlaz.configure(state = 'normal')
        self.txtIzlaz.insert(END, izlazRijec)
        self.txtIzlaz.configure(state = 'disabled')
        tekstDat.close()
        # poruka o uspješnosti koja se briše nakon 3 sekunde
        self.poruka['text'] = 'Uspješno učitano!'
        self.root.after(3000, lambda: self.poruka.grid_forget())
        self.poruka.grid(row = 4, column = 1)

    def spremiKao ( self ):
        listaTxt = []
        self.txtIzlaz.configure(state = 'normal')
        for i in (self.txtIzlaz.get("1.0", END)).split():
            listaTxt.append(i)
        izlazniStr = ' '.join(listaTxt)

        try:
            path = filedialog.asksaveasfile(title = "Spremi kao...",
                                            filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
                                            ).name

        except:
            self.poruka['text'] = 'Nije spremljeno!'
            return

        with open(path, 'w', encoding = 'utf-8') as f:
            f.write(izlazniStr)
            # f.write(izlazniStr + '.txt')  ovo dodati ako je potrebno
        # poruka o uspješnosti koja se briše nakon 3 sekunde
        self.poruka['text'] = 'Datoteka uspješno spremljena!'
        self.root.after(3000, lambda: self.poruka.grid_forget())
        self.poruka.grid(row = 4, column = 1)

    def reset_polja ( self ):
        self.unos_fld.delete(0, 'end')
        self.txtIzlaz.configure(state = 'normal')
        self.txtIzlaz.delete('1.0', END)
        self.txtIzlaz.configure(state = 'disabled')

        self.poruka['text'] = 'Sva polja izbrisana!'
        self.root.after(3000, lambda: self.poruka.grid_forget())
        self.poruka.grid(row = 4, column = 1)

    def kopiraj ( self ):
        self.root.clipboard_clear()
        kopStr = self.unos_fld.get()
        self.root.clipboard_append(str(kopStr))
        self.root.update()

    def irezi ( self ):
        self.root.clipboard_clear()
        kopStr = self.unos_fld.get()
        self.root.clipboard_append(str(kopStr))
        self.unos_fld.delete(0, 'end')
        self.root.update()


root = Tk()
myapp = App(root)
myapp.mainloop()
