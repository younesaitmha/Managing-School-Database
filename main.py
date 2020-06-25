# coding: utf-8

from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview
from PIL import ImageTk, Image
import mysql.connector as mysql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json



#================================== GLOBAL VARIABLES =====================================
db_cursor, db_connection = None, None
varF, menuFil = None, None


def connect_to_db():
    """ function to connect to database """

    global db_cursor, db_connection
    db_connection = mysql.connect(
        host = "",
        user = "",
        passwd = "",
        database = "sql2345403"
    )
    db_cursor = db_connection.cursor()


#================================== FUNCTIONS FILIÈRE =====================================

def load_file_fl():
    """ function to upload file that contain data of classes:
        input: csv file, excel file, json file (example of json [{"nom_filiere":"DS-E"},{"nom_filiere":"DS"}])
        output: register classes don't exist
    """

    root.filename = filedialog.askopenfilename(initialdir="/",title='select file', filetypes = (("json files", "*.json"),
                                                ("csv files", "*.csv"), ("excel files", "*.xlsx")))
    path_file_fl = root.filename
    if path_file_fl[-4:] == 'json':
        with open(path_file_fl) as file_json:
            for item in json.load(file_json):
                db_cursor.execute('''INSERT IGNORE INTO Filiere (nomFiliere) VALUES (%s)''', (item['nom_filiere'],))
    elif path_file_fl[-4:] == 'xlsx':
        data = pd.read_excel(path_file_fl)
        df = pd.DataFrame(data, columns= ['nom_filiere'])
        for row in df.itertuples():
            db_cursor.execute('''INSERT IGNORE INTO Filiere (nomFiliere) VALUES (%s)''', (row.nom_filiere,))
    else:
        data = pd.read_csv(path_file_fl)
        df = pd.DataFrame(data, columns= ['nom_filiere'])
        for row in df.itertuples():
            db_cursor.execute("INSERT INTO Filiere(nomFiliere) VALUES(%s)", (row.nom_filiere,))
    messagebox.showinfo("Information", "records inserted")
    db_connection.commit()
    update_menu()

def clear_fl():
    """ function to erase the fields """

    e_fl_nom.delete(0, END)
    tv_fl.delete(*tv_fl.get_children())


def register_fl():
    """ function to register a class in database:
        input: name of class
        output: insert or not insert and errors in popups
    """

    if len(e_fl_nom.get()) == 0:
        messagebox.showerror("Information", "Some fields left blank",icon="warning")
    else:
        nom = e_fl_nom.get()
        db_cursor.execute("SELECT nomFiliere FROM Filiere WHERE nomFiliere = %s", (nom,))
        result = db_cursor.fetchall()
        reponse = None
        for item in result:
            if(item[0] == e_fl_nom.get()):
                reponse = messagebox.askokcancel("Information", "Record Already exists")
                e_fl_nom.delete(0, END)
                break
        if(reponse is None):
            db_cursor.execute("INSERT INTO Filiere(nomFiliere) VALUES(%s)", (nom,))
            db_connection.commit()
            messagebox.showinfo("Information", "Record inserted")
            e_fl_nom.delete(0, END)
            update_menu()


def show_record_fl():
    """ function to show record
        input: name of class
        output: all informations about this class if it exists
    """

    if len(e_fl_nom.get()) == 0:
        messagebox.showerror("Information", "Some fields left blank",icon="warning")
    else:
        nom = e_fl_nom.get()
        db_cursor.execute("SELECT * FROM Filiere WHERE nomFiliere = %s", (nom,))
        rows = db_cursor.fetchall()
        if len(rows) == 0:
            messagebox.showinfo("Information", "No Record exists")
        else:
            tv_fl.delete(*tv_fl.get_children())
            for row in rows:
                tv_fl.insert('', 'end', values=row)


def delete_fl():
    """ function to delete a class in database:
        input: name of class
        output: pupup to inform that the class deleted, if it exists. if not another popup inform that not exist
    """

    global menuFil
    if len(e_fl_nom.get()) == 0:
        messagebox.showerror("Information", "Some fields left blank",icon="warning")
    else:
        nom = e_fl_nom.get()
        db_cursor.execute("SELECT * FROM Filiere WHERE nomFiliere = %s", (nom,))
        rows = db_cursor.fetchall()
        if len(rows) == 0:
            messagebox.askokcancel("Information", "No Record exists")
        else:
            result = messagebox.askquestion('Confirmation', 'Are you sure you want to delete this record?', icon="warning")
            if result == 'yes':
                db_cursor.execute("DELETE FROM Filiere WHERE nomFiliere = %s", (nom,))
                db_connection.commit()
                messagebox.showinfo("Information","Record Deleted")
                update_menu()
            e_fl_nom.delete(0, END)


def show_all_fl():
    """ function to show the table of classes
        input: no input
        output: table of classes in database
    """

    db_cursor.execute("SELECT * FROM Filiere")
    rows = db_cursor.fetchall()
    if len(rows) == 0:
        messagebox.showinfo("Information", "No Record exists")
    else:
        tv_fl.delete(*tv_fl.get_children())
        for row in rows:
            tv_fl.insert('', 'end', values=row)


def update_fl():
    """ function to update a record
        input: name of class
        output: updated the record if exist, if not register it or cancel depend on the choice of the user
    """

    if len(e_fl_nom.get()) == 0:
        messagebox.showerror("Information", "Some fields left blank",icon="warning")
    else:
        db_cursor.execute("SELECT * FROM Filiere WHERE nomFiliere = %s", (e_fl_nom.get(),))
        result = db_cursor.fetchone()
        if result == None:
            r = messagebox.askyesno("Information", "No Record exists with this name!\n do you want to register it?")
            if r == 1:
                db_cursor.execute("INSERT INTO Filiere(nomFiliere) VALUES(%s)", (e_fl_nom.get(),))
                messagebox.showinfo("Information", "Record inserted")
                db_connection.commit()
        else:
            top = Toplevel(root)
            Label(top, text="enter the new name of the class:",width=22,height=2,fg="#018754",font=("Calibri",16)).pack(padx=10)
            e = Entry(top)
            e.focus()
            e.pack(padx=8)
            def ok():
                if e.get() != '':
                    db_cursor.execute("UPDATE Filiere SET nomFiliere = %s WHERE idFiliere=%s", (e.get(),result[0]))
                    messagebox.showinfo("Info","Record Updated")
                    db_connection.commit()
                    top.destroy()
                else:
                    messagebox.showerror("Information", "the field left blank",icon="warning")
            b = Button(top, text="Submit", width=9,height=2,fg="#018754",bg="#C4DCCE",font=("Calibri",15),command=ok)
            b.pack(padx=4, pady=4)
        e_fl_nom.delete(0, END)
        update_menu()


def statistic_fl():
    """ function to show statistics of classes
        input: table with two columns classe and number of students in each classe
        output: a pie to show distribution of students by classes
    """

    sql_query = """ SELECT Filiere.nomFiliere, COUNT(Etudiant.idEtudiant) as NumberOfStudent FROM Filiere, Etudiant
                    WHERE Etudiant.IdFiliereFK=Filiere.idFiliere GROUP BY Filiere.nomFiliere;"""
    df = pd.DataFrame(pd.read_sql_query(sql_query,db_connection), columns=['Filiere','NumberOfStudent'])

    fig, ax = plt.subplots(figsize=(11, 6), subplot_kw=dict(aspect="equal"))

    def func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return "{:.1f}%\n({:d} étudiants)".format(pct, absolute)


    wedges, texts, autotexts = ax.pie(df['NumberOfStudent'], autopct=lambda pct: func(pct, df['NumberOfStudent']),
                                    textprops=dict(color="w"))

    ax.legend(wedges, df['Filiere'],
            title="Filières",
            loc="center left",
            bbox_to_anchor=(0.95, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title("distribution of students by classes")

    plt.show()


#================================== FUNCTIONS ÉTUDIANT =====================================

def clear_et():
    """ function to erase the fields """

    e_nom.delete(0, END)
    e_prenom.delete(0, END)
    e_age.delete(0, END)
    varF.set("Filière")
    tv_et.delete(*tv_et.get_children())


def load_file_et():
    """ function to upload file that contain data of students:
        input: csv file, excel file, jason file
        output: list of students already exist
    """

    root.filename = filedialog.askopenfilename(title='select file', filetypes = (('json files', '*.json'),
                                                ('csv files', '*.csv'), ('xlsx files', '*.xlsx'))) # initialdir="/"
    path_file_et = root.filename
    db_cursor.execute('SELECT * FROM Filiere')
    rows = db_cursor.fetchall()

    if path_file_et[-4:] == 'json':
        with open(path_file_et) as file_json:
            for item in json.load(file_json):
                db_cursor.execute("SELECT idFiliere FROM Filiere WHERE nomFiliere = %s", (item['filiere'],))
                result = db_cursor.fetchone()
                if result is None:
                    db_cursor.execute("""INSERT IGNORE INTO Etudiant(nom,prenom,age,) VALUES(%s,%s,%s)""",
                                            (item['nom'], item['prenom'], str(item['age'])))
                else:
                    db_cursor.execute('''INSERT IGNORE INTO Etudiant (nom,prenom,age,IdFiliereFK) VALUES (%s,%s,%s,%s)''',
                                            (item['nom'], item['prenom'], str(item['age']), result[0]))
    elif path_file_et[-4:] == 'xlsx':
        data = pd.read_excel(path_file_et)
        df = pd.DataFrame(data, columns= ['nom', 'prenom', 'age','nom_filiere'])
        for row in df.itertuples():
            db_cursor.execute("SELECT idFiliere FROM Filiere WHERE nomFiliere = %s", (row.nom_filiere,))
            result = db_cursor.fetchone()
            if result is None:
                db_cursor.execute('''INSERT IGNORE INTO Etudiant (nom,prenom,age,) VALUES (%s,%s,%s,)''',
                                        (row.nom,row.prenom,row.age,))
            else:
                db_cursor.execute('''INSERT IGNORE INTO Etudiant (nom,prenom,age,IdFiliereFK) VALUES (%s,%s,%s,%s)''',
                                        (row.nom,row.prenom,row.age,result[0]))
    else:
        data = pd.read_csv(path_file_et)
        df = pd.DataFrame(data, columns= ['nom', 'prenom', 'age','nom_filiere'])
        for row in df.itertuples():
            db_cursor.execute("SELECT idFiliere FROM Filiere WHERE nomFiliere = %s", (row.nom_filiere,))
            result = db_cursor.fetchone()
            if result is None:
                db_cursor.execute('''INSERT IGNORE INTO Etudiant (nom,prenom,age,) VALUES (%s,%s,%s,)''',
                                        (row.nom,row.prenom,row.age,))
            else:
                db_cursor.execute('''INSERT IGNORE INTO Etudiant (nom,prenom,age,IdFiliereFK) VALUES (%s,%s,%s,%s)''',
                                        (row.nom,row.prenom,row.age,result[0]))

    db_connection.commit()
    messagebox.showinfo("Information", "records inserted")


def register_et():
    """ function to register a student in database:
        input: first name, last name, age and class of student
        output: insert or not insert and errors in popups
    """
    if e_age.get()=='' or e_nom.get() == '' or  e_prenom.get() == '' or varF.get() == 'Filière':
        messagebox.showerror('Information', 'Some fields left blank',icon="warning")
    else:
        db_cursor.execute('SELECT * FROM Filiere')
        rows = db_cursor.fetchall()
        db_cursor.execute("SELECT * FROM Etudiant WHERE nom=%s AND prenom=%s AND age=%s ",(e_nom.get(), e_prenom.get(), int(e_age.get()),))
        result = db_cursor.fetchall()
        r = 0
        for e in result:
            if(e[1]== e_age.get() and e[2]==e_prenom.get() and e_age.get()==e[3]):
                r = 1
                db_cursor.execute("SELECT nomFiliere FROM Filiere WHERE idFiliere = %s",(e[4],))
                if varF.get() == db_cursor.fetchone()[0]:
                    messagebox.askokcancel("Information","Record Already exists")
                else:
                    db_cursor.execute("SELECT idFiliere FROM Filiere WHERE nomFiliere = %s",(varF.get(),))
                    db_cursor.execute("INSERT INTO Etudiant(nom,prenom,age,IdFiliereFK) VALUES(%s,%s,%s,%s)",(e_nom.get(), e_prenom.get(), db_cursor.fetchone()[0],))
                    messagebox.askokcancel("Information","Record inserted")
                break
        if r == 0:
            db_cursor.execute("SELECT idFiliere FROM Filiere WHERE nomFiliere = %s",(varF.get(),))
            db_cursor.execute("INSERT INTO Etudiant(nom,prenom,age,IdFiliereFK) VALUES(%s,%s,%s,%s)",(e_nom.get(), e_prenom.get(), e_age.get(),db_cursor.fetchone()[0],))
            messagebox.askokcancel("Information","Record inserted")
        db_connection.commit()
        e_nom.delete(0, END)
        e_prenom.delete(0, END)
        e_age.delete(0, END)
        varF.set("Filière")


def delete_et():
    """ function to delete a student from database:
        input: (nom, prenom, age, filière) of student
        output: pupup to inform that the student deleted, if it exists. if not another popup inform that not exist
    """

    if e_nom.get() == '' or  e_prenom.get() == '' or varF.get() == 'Filière':
        messagebox.showerror('Information', 'Some fields left blank',icon="warning")
    else:
        db_cursor.execute("""SELECT * FROM Filiere WHERE idFiliere=%s""",(varF.get(),))
        l = db_cursor.fetchone()
        idf = 0 if l is None else l[0]
        if e_age.get()=='':
            if idf != 0:
                result = messagebox.askquestion('Confirmation', 'Are you sure you want to delete this record?')
                if result == 'yes':
                    db_cursor.execute("""DELETE FROM Etudiant WHERE nom = %s AND prenom = %s AND IdFiliereFK = %s""",
                                            (e_nom.get(), e_prenom.get(), idf))
                    messagebox.showinfo("Information","Record Deleted")
            else:
                result = messagebox.askquestion('Confirmation', 'Are you sure you want to delete this record?')
                if result == 'yes':
                    db_cursor.execute("""DELETE FROM Etudiant WHERE nom = %s AND prenom = %s""",(e_nom.get(), e_prenom.get(),))
                    messagebox.showinfo("Information","Record Deleted")
        else:
            if idf != 0:
                result = messagebox.askquestion('Confirmation', 'Are you sure you want to delete this record?')
                if result == 'yes':
                    db_cursor.execute("""DELETE FROM Etudiant WHERE nom = %s AND prenom = %s AND age = %s AND IdFiliereFK = %s""",
                                        (e_nom.get(), e_prenom.get(), e_age.get(), idf))
                    messagebox.showinfo("Information","Record Deleted")
            else:
                result = messagebox.askquestion('Confirmation', 'Are you sure you want to delete this record?')
                if result == 'yes':
                    db_cursor.execute("""DELETE FROM Etudiant WHERE nom = %s AND prenom = %s AND age = %s""",
                                        (e_nom.get(), e_prenom.get(), e_age.get(), ))
                    messagebox.showinfo("Information","Record Deleted")
        e_nom.delete(0, END)
        e_prenom.delete(0, END)
        e_age.delete(0, END)
        varF.set("Filière")
        db_connection.commit()


def show_all_et():
    """ function to show the table of students
        input: no input
        output: table of students in database
    """

    db_cursor.execute("SELECT * FROM Etudiant")
    rows = db_cursor.fetchall()
    if len(rows) == 0:
        messagebox.showinfo("Information", "No Record exists")
    else:
        tv_et.delete(*tv_et.get_children())
        for row in rows:
            tv_et.insert('', 'end', values = row)


def show_record_et():
    """ function to show record
        input: (nom, prenom, (filiere, age are facultatives)) of class
        output: all informations about this student if it exists
    """

    if e_nom.get() == '' or e_prenom.get() == '':
        messagebox.showerror("Information", "Some fields left blank",icon="warning")
    elif varF.get() != 'Filière' and len(e_age.get()) == 0:
        db_cursor.execute("SELECT * FROM Filiere WHERE nomFiliere = %s", (varF.get(),))
        idf = db_cursor.fetchone()
        db_cursor.execute("SELECT * FROM Etudiant WHERE nom = %s AND prenom = %s AND IdFiliereFK=%s", (e_nom.get(),e_prenom.get(),idf[0]))
        rows = db_cursor.fetchall()
        if len(rows) == 0:
            messagebox.showinfo("Information", "No Record exists")
        else:
            tv_et.delete(*tv_fl.get_children())
            for row in rows:
                tv_et.insert('', 'end', values=row)
    elif varF.get() == 'Filière' and len(e_age.get()) != 0:
        db_cursor.execute("SELECT * FROM Etudiant WHERE nom = %s AND prenom = %s AND age= %s", (e_nom.get(),e_prenom.get(),e_age.get()))
        rows = db_cursor.fetchall()
        if len(rows) == 0:
            messagebox.showinfo("Information", "No Record exists")
        else:
            tv_et.delete(*tv_fl.get_children())
            for row in rows:
                tv_et.insert('', 'end', values=row)
    elif varF.get() == 'Filière' and len(e_age.get()) == 0:
        db_cursor.execute("SELECT * FROM Etudiant WHERE nom = %s AND prenom = %s", (e_nom.get(),e_prenom.get(),))
        rows = db_cursor.fetchall()
        if len(rows) == 0:
            messagebox.showinfo("Information", "No Record exists")
        else:
            tv_et.delete(*tv_fl.get_children())
            for row in rows:
                tv_et.insert('', 'end', values=row)
    else:
        db_cursor.execute("SELECT * FROM Filiere WHERE nomFiliere = %s", (varF.get(),))
        idf = db_cursor.fetchone()
        db_cursor.execute("SELECT * FROM Etudiant WHERE nom = %s AND prenom = %s AND age= %s AND IdFiliereFK=%s",
                             (e_nom.get(),e_prenom.get(),e_age.get(),idf[0]))
        rows = db_cursor.fetchall()
        if len(rows) == 0:
            messagebox.showinfo("Information", "No Record exists")
        else:
            tv_et.delete(*tv_fl.get_children())
            for row in rows:
                tv_et.insert('', 'end', values=row)


def update_et():
    """ function to update a record
        input: (nom, prenom, (age, filière are facultative)) of student
        output: updated the record if exist, if not register it or cancel depend on the choice of the user
    """

    def top_update(id):
        top = Toplevel(root)
        top.geometry("400x350")
        top["bg"]= 'white'
        top["relief"] = "raised"
        Label(top, text="Nom : ",width=22,height=2,fg="#018754",font=("Calibri",14)).pack(padx=10)
        nom_top = Entry(top, bd=2)
        nom_top.pack(padx=8)
        nom_top.focus()
        Label(top, text="Prénom : ",width=22,height=2,fg="#018754", font=("Calibri",14)).pack(padx=12)
        prenom_top = Entry(top, bd=2)
        prenom_top.pack(padx=8)
        Label(top, text="Age : ",width=22,height=2,fg="#018754",font=("Calibri",14)).pack(padx=12)
        age_top = Entry(top, bd=2)
        age_top.pack(padx=8)
        flr = StringVar()
        fl = [
            'Data & software engineering',
            'Data Science',
            'statistique et démographie',
            'Statistique et Economie',
            'Recherche Opérationnelle',
            'Actuariat et Finance']
        db_cursor.execute("SELECT nomFiliere FROM Filiere")
        a = db_cursor.fetchall()
        if a is not None:
            fl = [i[0] for i in a]
        flr.set("Filière")
        menuFil = OptionMenu(top, flr, *fl)
        menuFil.configure(background = "#C4DCCE", activebackground = "#78B594", width = 20, height = 2)
        menuFil["menu"].configure(bg = "#78B594")
        menuFil.pack(padx=7, pady = 16)
        sub = Button
        def ok():
            if nom_top.get() != '' and prenom_top.get() != '' and age_top.get() != '' and flr.get() != '':
                db_cursor.execute("SELECT * FROM Filiere WHERE nomFiliere = %s",(flr.get(),))
                f = db_cursor.fetchone()
                db_cursor.execute("UPDATE Etudiant SET nom=%s AND prenom=%s AND age=%s AND IdFiliereFK=%s WHERE idEtudiant=%s",
                                    (str(nom_top.get()), str(prenom_top.get()), age_top.get(), f[0], id))
                db_connection.commit()
                top.destroy()
                messagebox.showinfo("Info","Record Update")
            else:
                messagebox.showerror("Information", "the field left blank",icon="warning")

        b = Button(top, text="Submit", width=8,height=2,fg="#018754",bg="#C4DCCE",font=("Calibri",15),command=ok)
        b.pack(padx=4, pady=4)

    if e_nom.get() == '' or e_prenom.get()== '':
        messagebox.showerror("Information", "Some fields left blank",icon="warning")
    else:
        db_cursor.execute("SELECT * FROM Filiere WHERE nomFiliere = %s", (varF.get(),))
        result = db_cursor.fetchone()
        if result is None:
            if e_age.get() == '':
                db_cursor.execute("SELECT idEtudiant FROM Etudiant WHERE nom = %s AND prenom = %s", (e_nom.get(),e_prenom.get()))
                row = db_cursor.fetchone()
                if row is None:
                    messagebox.showerror("Information", "This record doesn't exist!", icon="warning")
                else:
                    i = int(row[0])
                    top_update(i)
            else:
                db_cursor.execute("SELECT idEtudiant FROM Etudiant WHERE nom = %s AND prenom = %s AND age=%s", (e_nom.get(),e_prenom.get(),e_age.get()))
                row = db_cursor.fetchone()
                if row is None:
                    messagebox.showerror("Information", "This record doesn't exist!", icon="warning")
                    r = messagebox.askyesno("Confirmation","Do you want to register it?")
                    if r==1:
                        db_cursor.execute("INSERT INTO Etudiant(nom, prenom, age,) VALUES(%s,%s,%s,)", (e_nom.get(),e_prenom.get(),e_age.get()))
                        messagebox.showinfo("Information", "Record inserted")
                else:
                    i = int(row[0])
                    top_update(i)

        else:
            if e_age.get() == '':
                db_cursor.execute("SELECT idEtudiant FROM Etudiant WHERE nom = %s AND prenom = %s AND IdFiliereFK=%s", (e_nom.get(),e_prenom.get(), result[0]))
                row = db_cursor.fetchone()
                if row is None:
                    messagebox.showerror("Information", "This record doesn't exist!", icon="warning")
                else:
                    i = int(row[0])
                    top_update(i)
            else:
                db_cursor.execute("SELECT idEtudiant FROM Etudiant WHERE nom = %s AND prenom = %s AND age=%s AND IdFiliereFK=%s",
                                    (e_nom.get(),e_prenom.get(),e_age.get(),result[0]))
                row = db_cursor.fetchone()
                if row is None:
                    messagebox.showerror("Information", "This record doesn't exist!", icon="warning")
                    r = messagebox.askyesno("Confirmation","Do you want to register it?")
                    if r==1:
                        db_cursor.execute("INSERT INTO Etudiant(nom, prenom, age,IdFiliereFK) VALUES(%s,%s,%s,%s)", (e_nom.get(),e_prenom.get(),e_age.get(), result[0]))
                        db_connection.commit()
                        messagebox.showinfo("Information", "Record inserted")
                else:
                    top_update(row[0])
                    messagebox.showinfo("Info","Record Update")
    e_nom.delete(0, END)
    e_prenom.delete(0, END)
    e_age.delete(0, END)
    varF.set("Filière")



def statistic_et():
    pass
    #select = """SELECT Etudiant.nom,Etudiant.prenom,Etudiant.age,Filiere.nomFiliere from Etudiant,Filiere
                    #WHERE Etudiant.IdFiliereFK=Filiere.idFiliere AND Etudiant.nom='%s' AND Etudiant.prenom='%s'
                    #AND Etudiant.age'%s' """ %(e_nom.get(), e_prenom.get(), e_age.get())


#================================== MAIN WINDOW =====================================
root = Tk()
root.title('Étudiants & Filières')
root.geometry("1350x760")
root["bg"]= '#EEEEEE'
root["relief"] = "raised"
root.iconphoto(False, PhotoImage(file='img/logo.png'))
connect_to_db()


#================================== FRAME ÉTUDIANT =====================================
FrameEt = LabelFrame(root,text='Étudiant', width=650, height=645,bd=2,bg='#C4DCCE',font=('bold',20)).place(x=14, y=102)
sub_frameEt = LabelFrame(FrameEt,width=632,height=556,bd=2,font=('bold',20)).place(x=23, y=130)
tv_et = Treeview(sub_frameEt, columns=(1, 2, 3, 4, 5),show='headings', height=12)
tv_et.place(x=56, y=400)

tv_et.heading(1, text='id étudinat')
tv_et.column(1,anchor ='center', width=90)

tv_et.heading(2, text='nom')
tv_et.column(2,anchor ='center', width=120)

tv_et.heading(3, text='prénom')
tv_et.column(3,anchor ='center', width=120)

tv_et.heading(4, text='age')
tv_et.column(4,anchor ='center', width=95)

tv_et.heading(5, text='filière')
tv_et.column(5,anchor ='center', width=125)

scroll_et = Scrollbar(sub_frameEt, orient = VERTICAL, command = tv_et.yview)
tv_et.configure(yscroll=scroll_et.set)
scroll_et.place(x=610, y=420)


#================================== FRAME FILIÈRE =====================================
FrameFl = LabelFrame(root,text='Filière', width=650, height=645, bg='#C4DCCE',bd=2,font=('bold',20)).place(x=688, y=102)
sub_frameFl = LabelFrame(FrameFl, width=632, height=556, bd=2, font=('bold', 20)).place(x=697, y=130)

tv_fl = Treeview(sub_frameFl, columns=(1, 2),show='headings', height=12)
tv_fl.place(x=790, y=340)
tv_fl.heading(1, text='id filière')
tv_fl.column(1,anchor ='center', width=130)
tv_fl.heading(2, text='nom filière')
tv_fl.column(2,anchor ='center', width=330)
scroll_fl = Scrollbar(sub_frameFl,orient=VERTICAL,command=tv_fl.yview)
tv_fl.configure(yscroll=scroll_fl.set)
scroll_fl.place(x=1254, y=360)


#================================== HEADER =====================================
photo=PhotoImage(file = 'img/logo.png')
photoLabel=Label(root, image = photo)
photoLabel.configure(width = 90, height = 90, bg = '#EEEEEE')
photoLabel.place(x=45, y=4)

insea_grandui = Label(root, text = "Institut National de Statistique\net d'Economie Appliquée",
                        width = 20, height = 3, bg = "#EEEEEE", fg = '#018754', font = ("bold",25)).place(x=250, y=1)

younes_ait_mha = Label(root, text = "Younes Ait M'ha",width = 20, height = 3, bg = "#EEEEEE", fg ='#78B594',
                        font = ("sans-serif",25)).place(x=800, y=1)

def cancel():
    if(messagebox.askokcancel('cancel popup', 'do you want to quit the app?')):
        db_connection.commit()
        db_cursor.close()
        db_connection.close()
        root.quit()

photo2 = PhotoImage(file = r"img/exit.png")
b_exit = Button(root, width = 60, height = 55, image = photo2, bd=5, bg = '#EEEEEE', command=cancel).place(x=1230, y=18)


#================================== REGITER UI ÉTUDIANT =====================================
lab_nom = Label(root, text = "Nom :", width = 24, height = 2, bg = "#78B594").place(x=50, y=180)
lab_prenom = Label(root, text = "Prénom :", width = 24, height = 2, bg = "#C4DCCE").place(x=50, y=232)
lab_age = Label(root, text="Age :", width = 24, height = 2, bg = "#78B594").place(x=50, y=282)

varF = StringVar()
varF.set("Filière")
filiere = [
    'Data & software engineering',
    'Data Science',
    'statistique et démographie',
    'Statistique et Economie',
    'Recherche Opérationnelle',
    'Actuariat et Finance']
db_cursor.execute("SELECT nomFiliere FROM Filiere")
a = db_cursor.fetchall()
if len(a) != 0:
    filiere = [i[0] for i in a]

menuFil = OptionMenu(root, varF, *filiere)
menuFil.configure(background = "#C4DCCE", activebackground = "#78B594", width = 56, height = 2)
menuFil["menu"].configure(bg = "#78B594")
menuFil.place(x=51, y=332)

def update_menu():
    global varF, menuFil
    db_cursor.execute("SELECT nomFiliere FROM Filiere")
    a = db_cursor.fetchall()
    fl = [i[0] for i in a]
    varF.set("Filière")
    menuFil = OptionMenu(root, varF, *fl)
    menuFil.configure(background = "#C4DCCE", activebackground = "#78B594", width = 56, height = 2)
    menuFil["menu"].configure(bg = "#78B594")
    menuFil.place(x=51, y=332)

#================================== ENTRIES ÉTUDIANT =====================================
e_nom = Entry(root, width=32, borderwidth=4)
e_nom.place(x=290, y=183)
e_nom.focus()
e_prenom = Entry(root, width=32, borderwidth=4)
e_prenom.place(x=290, y=235)
e_age = Entry(root, width=32, borderwidth=4)
e_age.place(x=290, y=286)


#================================== ENTRIES FILIÈRE =====================================
e_fl_nom = Entry(root, width=32, borderwidth=4)
e_fl_nom.place(x=990, y=228)


#================================== REGISTER UI FILIÈRE =====================================
lab_nom_filière = Label(root,text="Nom filière :",width=24,height=2,bg="#78B594").place(x=740, y=225)


#================================== BUTTONS ÉTUDIANT =====================================
b_create_et = Button(FrameEt,text="Register",width=9,height=2,fg="#018754",bg="#C4DCCE",font=("Calibri",15),command=register_et).place(x=21,y=698)
b_delete_et = Button(FrameEt,text="Delete",width=9,height=2,fg="#018754",font=("Calibri",15),command=delete_et).place(x=129,y=698)
b_update_et = Button(FrameEt,text="Update",width=9,height=2,fg="#018754",font=("Calibri",15),command=update_et).place(x=237,y=698)
b_read_et = Button(FrameEt,text="Show record",width=9,height=2,fg="#018754", font=("Calibri",15),command=show_record_et).place(x=344,y=698)
b_read_all_et = Button(FrameEt,text="Show All",width=9,height=2,fg="#018754",font=("Calibri",15),command=show_all_et).place(x=453,y=698)
b_clear_et = Button(FrameEt,text="Clear",width=9,height=2,bg="#78B594",fg="#CB5853", font=("Calibri",15),command=clear_et).place(x=561,y=698)
b_load_file_et = Button(root,text="register file of data",width=18,height=2,fg="#018754",bd=2,font=("Calibri",15),command=load_file_et).place(x=170,y=135)
b_statistic_et =Button(root, text='Statistics',width=18,height=2,fg='#018754',bg='#C4DCCE',bd=2,font=("Arial",15),command=statistic_et).place(x=452,y=642)


#================================== BUTTONS FILIÈRE =====================================
b_create_fl = Button(FrameFl,text="Register",width=9,height=2,fg="#018754",bd=10,bg="#C4DCCE",font=("Calibri",15),command=register_fl).place(x=696,y=698)
b_delete_fl = Button(FrameFl,text="Delete",width=9,height=2,fg="#018754",bd=10,font=("Calibri",15),command=delete_fl).place(x=804,y=698)
b_update_fl = Button(FrameFl,text="Update",width=9,height=2,fg="#018754",bd=2,font=("Calibri",15),command=update_fl).place(x=912,y=698)
b_read_fl = Button(FrameFl,text="Show record",width=9,height=2,fg="#018754",bd=2,font=("Calibri",15), command=show_record_fl).place(x=1020,y=698)
b_read_all_fl = Button(FrameFl,text="Show All",width=9,height=2,fg="#018754",bd=2,font=("Calibri",15),command=show_all_fl).place(x=1127,y=698)
b_clear_fl = Button(FrameFl,text="Clear",width=9,height=2,bg="#78B594",fg="#CB5853",bd=2,font=("Calibri",15),command=clear_fl).place(x=1234,y=698)
b_load_file_fl = Button(root,text="register file of data",width=18,height=2,fg="#018754",bd=2,font=("Calibri",15),command=load_file_fl).place(x=890,y=158)
b_statistic_fl =Button(root, text='Statistics',width=18,height=2,fg='#018754',bg='#C4DCCE',bd=2,font=("Arial",15),command=statistic_fl).place(x=1127,y=640)


root.mainloop()
