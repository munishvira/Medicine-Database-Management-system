import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from string import ascii_uppercase as alphabet

class DB:
	def __init__(self):
		self.conn = sqlite3.connect("medicine.db")
		self.cur = self.conn.cursor()
		self.cur.execute("CREATE TABLE IF NOT EXISTS medicine (id INTEGER PRIMARY KEY,Drug_name TEXT, Company TEXT, units INTEGER,Disease TEXT)")
		self.conn.commit()

	def __del__(self):
		self.conn.close()

	def view(self):
		self.cur.execute("SELECT * FROM medicine")
		rows = self.cur.fetchall()
		return rows

	def insert(self, Drug_name, Company, units, Disease):
		self.cur.execute("INSERT INTO medicine VALUES      (NULL,?,?,?,?)", (Drug_name, Company, units, Disease))
		self.conn.commit()

	def update(self, id, Drug_name, Company, units, Disease):
			self.cur.execute("UPDATE medicine SET Drug_name=?, Company=?, units=?, Disease=? WHERE id=?", (Drug_name, Company, units, Disease, id))
			self.conn.commit()
			self.view()

	def update1(self, id, units):
		self.cur.execute("UPDATE medicine SET units=? WHERE id=?", (units,id))
		self.conn.commit()
		self.view()

	def delete(self, id):
		self.cur.execute("DELETE FROM medicine WHERE id=?", (id,))
		self.conn.commit()
		self.view()

	def search(self, Drug_name="", Company="", units="", Disease=""):
		self.cur.execute("SELECT * FROM medicine WHERE Drug_name=? OR Company=? OR units=? OR Disease=?", (Drug_name, Company, units, Disease))
		rows = self.cur.fetchall()
		return rows

db = DB()
def get_selected_row(event):
	global selected_tuple
	index = list1.curselection()[0]
	selected_tuple = list1.get(index)
	e1.delete(0, END)
	e1.insert(END, selected_tuple[1])
	e2.delete(0, END)
	e2.insert(END, selected_tuple[2])
	e3.delete(0, END)
	e3.insert(END, selected_tuple[3])
	e4.delete(0, END)
	e4.insert(END, selected_tuple[4])

def get_selected_row1(event):
	global selected_tuple1
	index = list2.curselection()[0]
	selected_tuple1 = list2.get(index)
	e5.delete(0, END)
	e5.insert(END, selected_tuple1[4])
	e6.delete(0, END)
	e6.insert(END, selected_tuple1[2])

def view_command():
	list1.delete(0, END)
	for row in db.view():
		list1.insert(END, row)
		e1.delete(0, END)
		e2.delete(0, END)
		e3.delete(0, END)
		e4.delete(0, END)

def search_command():
	list1.delete(0, END)
	for row in db.search(Drug_text.get(), Company_text.get(), Units_text.get(), Disease_text.get()):
		list1.insert(END, row)
	e1.delete(0, END)
	e2.delete(0, END)
	e3.delete(0, END)
	e4.delete(0, END)


def search_medicine():
	list1.delete(0, END)
	for row in db.search(combo_text.get(),combo_text.get(),combo_text.get(),combo_text.get()):
		list1.insert(END, row)

def search_medicine1():
	list2.delete(0, END)
	for row in db.search(combo_text2.get(),combo_text2.get(),combo_text2.get(),combo_text2.get()):
		list2.insert(END, row)

def add_command():
	db.insert(Drug_text.get(), Company_text.get(), Units_text.get(), Disease_text.get())
	list1.delete(0, END)
	list1.insert(END, (Drug_text.get(), Company_text.get(), Units_text.get(), Disease_text.get()))
	e1.delete(0, END)
	e2.delete(0, END)
	e3.delete(0, END)
	e4.delete(0, END)

def delete_command():
	db.delete(selected_tuple[0])
	e1.delete(0, END)
	e2.delete(0, END)
	e3.delete(0, END)
	e4.delete(0, END)


def update_command():
	db.update(selected_tuple[0], Drug_text.get(), Company_text.get(), Units_text.get(), Disease_text.get())
	e1.delete(0, END)
	e2.delete(0, END)
	e3.delete(0, END)
	e4.delete(0, END)

def issue_command():
	diff = selected_tuple1[3] - combo_text3.get()
	db.update1(selected_tuple1[0], diff)

window = Tk()
window.title("Drugs")
def on_closing():
	dd = db
	if messagebox.askokcancel("Quit", "Do you want to quit?"):
    		window.destroy()
    		del dd


window.protocol("WM_DELETE_WINDOW", on_closing)  # handle window closing
#window.quit()
l1 = Label(window, text="Drug_name")
l1.grid(row=0, column=0)

l2 = Label(window, text="Company")
l2.grid(row=0, column=2)

l3 = Label(window, text="Units")
l3.grid(row=1, column=0)

l4 = Label(window, text="Disease")
l4.grid(row=1, column=2)

l5 = Label(window, text="Company")
l5.grid(row=22, column=0)

l6 = Label(window, text="Disease")
l6.grid(row=22, column=2)

Drug_text = StringVar()
e1 = Entry(window, textvariable=Drug_text)
e1.grid(row=0, column=1)

Company_text = StringVar()
e2 = Entry(window, textvariable=Company_text)
e2.grid(row=0, column=3)

Units_text = StringVar()
e3 = Entry(window, textvariable=Units_text)
e3.grid(row=1, column=1)

Disease_text = StringVar()
e4 = Entry(window, textvariable=Disease_text)
e4.grid(row=1, column=3)

Company_text1 = StringVar()
e5 = Entry(window, textvariable=Company_text1)
e5.grid(row=22, column=3)

Units_text1 = StringVar()
e6 = Entry(window, textvariable=Units_text1)
e6.grid(row=22, column=1)

list1 = Listbox(window, height=6, width=35)
list1.grid(row=6, column=1, rowspan=6, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=6, column=3, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row)

b1 = Button(window, text="View all", width=12, command=view_command)
b1.grid(row=3, column=6)

b2 = Button(window, text="Search entry", width=12, command=search_command)
b2.grid(row=4, column=6)

b3 = Button(window, text="Add entry", width=12, command=add_command)
b3.grid(row=5, column=6)

b4 = Button(window, text="Update selected", width=12, command=update_command)
b4.grid(row=6, column=6)

b5 = Button(window, text="Delete selected", width=12, command=delete_command)
b5.grid(row=7, column=6)

b6 = Button(window, text="Close", width=12, command=window.destroy)
b6.grid(row=8, column=6)

conn = sqlite3.connect("medicine.db")
c = conn.cursor()
c.execute("SELECT DISTINCT Drug_name FROM medicine")
name = c.fetchall()
conn.commit()
conn.close()

combo_text = StringVar()
combo = Combobox(width = 15, textvariable=combo_text, values=name)
combo.grid(row=4, column=1)

l5 = Label(text = "Select Drug name")
l5.grid(row = 4, column = 0)
b7 = Button(window, text="Search", width=12, command=search_medicine)
b7.grid(row=4, column=3)

l6 = Label(text = "Retail:")
l6.grid(row = 19, column = 0)

l7 = Label(text = "Select medicine")
l7.grid(row = 20, column = 0)
combo_text2 = StringVar()
combo2 = Combobox(width = 15, textvariable=combo_text2, values=name)
combo2.grid(row=20,column=1)

l8 = Label(text = "Select units")
l8.grid(row = 20, column = 2)
combo_text3 = IntVar()
v = [i for i in range(1,11)]
combo3 = Combobox(width = 15, textvariable=combo_text3, values=v)
combo3.grid(row=20,column=3)

b7 = Button(window, text="Issue", width=12, command=issue_command)
b7.grid(row=20, column=7)

list2 = Listbox(window, height=6, width=35)
list2.grid(row=25, column=1, rowspan=6, columnspan=2)

sb2 = Scrollbar(window)
sb2.grid(row=25, column=3, rowspan=6)

list2.configure(yscrollcommand=sb2.set)
sb2.configure(command=list2.yview)

list2.bind('<<ListboxSelect>>', get_selected_row1)

b8 = Button(window, text="Search", width=12, command=search_medicine1)
b8.grid(row=20, column=6)


window.geometry("700x400")
window.mainloop()
