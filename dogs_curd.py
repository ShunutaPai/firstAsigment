from faulthandler import disable
from tabnanny import check
from turtle import width
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dogs_db import Person, Dogs, Courses, Size
from tkinter import *
import re
from PIL import ImageTk, Image


engine = create_engine('sqlite:///dogs.db')
session = sessionmaker(bind=engine)()

def add_course(discipline):
    entry = Courses(discipline=discipline)
    session.add(entry)
    session.commit()

def add_dog_size(name):
    entry = Size(size=name)
    session.add(entry)
    session.commit()

def add_person(name,l_name,email):
    entry = Person(name=name, l_name=l_name, email=email)
    session.add(entry)
    session.commit()

def add_dog(name,age,size_id,owner_id):
    entry = Dogs(name=name,
                 age=age,
                 size_id=size_id,
                 person_id=owner_id,
                 owner = session.query(Person).get(owner_id),
                 size = session.query(Size).get(size_id)
    )
    session.add(entry)
    session.commit()

def del_entry(db,nr):
    entry = session.query(db).get(nr)
    session.delete(entry)
    session.commit()
    
# add_person("Petras", "Stulpinas", "ps@gmail.com")
# add_person("Jonas", "Jonaitis", "jj@gmail.com")
# add_person("Zigmas", "Ponaitis", "zp@gmail.com")

# add_dog_size("Small")
# add_dog_size("Medium")
#add_dog_size("Large")
#add_dog_size("Undifined")

# add_dog("Shunuta",7,3, 3)
# add_dog("Pai",2,1, 2)

# add_course("Agility")
# add_course("Obiedence")
# add_course("Frisbee")

#entry_dog = session.query(Dogs).get(1)
# #entry = session.query(Courses).get(3)
# course = session.query(Courses).get(2)
# entry_dog.courses.append(course)
# session.add(entry_dog)
# session.commit()
#print(entry_dog.courses)
#[print(i.discipline) for i in entry_dog.courses]


class Pagrindinis:
    

    def __init__(self, root):
        self.root = root
        root.title("Dog register")
        root.geometry("550x350")
        root.configure(bg='lightblue')
        
        self.frame = Frame(self.root)
        self.frame.pack(side=LEFT)
        self.frame_info = Frame(self.root)
        self.frame_info.pack(side=RIGHT)

        

        self.img = ImageTk.PhotoImage(Image.open("pai.jpg"))
        self.pai = Label(self.frame, image = self.img)
        self.pai.pack(side=TOP)

        self.button_add_dog = Button(self.frame, text="Add dog", width=20, font = ('calibri', 10, 'bold'), background='green', command=self.new_window_add_dog)
        self.button_add_dog.pack()
        self.button_add_owner = Button(self.frame, text="Add Owner", width=20, font = ('calibri', 10, 'bold'), background='red', command=self.new_window_add_owner)
        self.button_add_owner.pack()
        
        self.button_show_dogs = Radiobutton(self.frame, text="Show Dogs",width=20, indicator = 0, command=self.show_dogs)
        self.button_show_dogs.pack()
        self.button_show_owners = Radiobutton(self.frame, text="Show Owners",width=20, indicator = 0, command=self.show_owners)
        self.button_show_owners.pack()

        self.button_update_screen = Button(self.frame, text="Update Screen", width=20, font = ('calibri', 10, 'bold'), background='red', command=self.screen)
        self.button_update_screen.pack()
        self.button_delete_entry = Button(self.frame, text="Delete Entry", width=20, font = ('calibri', 10, 'bold'),state = DISABLED, background='red', command=self.delete_entry)
        self.button_delete_entry.pack()
        

        self.scrollbar = Scrollbar(self.frame_info)
        self.scrollbar1 = Scrollbar(self.frame_info,orient='horizontal')
        self.l_box = Listbox(self.frame_info,width=50,height=50,font=('Arial', 12), yscrollcommand=self.scrollbar.set, xscrollcommand=self.scrollbar1.set)
        self.scrollbar.config(command=self.l_box.yview)
        self.scrollbar1.config(command=self.l_box.xview)
        self.scrollbar1.pack(side=BOTTOM, fill='x')
        self.scrollbar.pack(side=RIGHT, fill=Y)

      
        self.screen()

        
    def screen(self):
        self.l_box.delete(0, END)
        self.listas_dogs = session.query(Dogs).all()
        self.listas_owners = session.query(Person).all()
        count_dogs = len(self.listas_dogs)
        count_owners = len(self.listas_owners)
        self.l_box.insert(0,f"-----Active dogs-------->{count_dogs}")
        self.l_box.insert(1,f"-----Active owners----->{count_owners}")
        self.l_box.insert(2,"-----Dog list----------------------")
        self.l_box.insert(3,*self.listas_dogs)
        self.l_box.insert(END,"-----------Owners list-------------------Email-----------------")
        self.l_box.insert(END,*self.listas_owners)
        self.l_box.pack(side=TOP)

      

    def show_dogs(self):
        self.l_box.delete(0, END)
        self.l_box.insert(0,*self.listas_dogs)
        self.button_delete_entry['state'] = NORMAL
    
    
    def show_owners(self):
        self.l_box.delete(0, END)
        self.l_box.insert(0,*self.listas_owners)
        self.button_delete_entry['state'] = NORMAL

        
    def delete_entry(self):
        listas = session.query(Dogs).all()
        nr = listas[self.l_box.curselection()[0]].id
        del_entry(Dogs,nr)
        self.button_delete_entry['state'] = DISABLED
        self.screen()
       
    
   


        
        

    def new_window_add_dog(self):
        self.new = Toplevel(self.root)
        self.app = Add_dog(self.new)

    def new_window_add_owner(self):
        self.new = Toplevel(self.root)
        self.app = Add_owner(self.new)

class Add_dog:

    def __init__(self, root):
        self.root = root
        root.title("Add Dog")
        self.root.geometry("300x250")
        self.frame_top = Frame(self.root)
        self.frame_top.pack(side=TOP)
        self.frame_bot = Frame(self.root)
        self.frame_bot.pack(side=BOTTOM)

        self.label_name = Label(self.frame_top, text="Enter name")
        self.label_name.pack(side=TOP)
        self.entry_name = Entry(self.frame_top)
        self.entry_name.pack()
        self.label_age = Label(self.frame_top, text="Enter dogs age in years")
        self.label_age.pack(side=TOP)
        self.entry_age = Entry(self.frame_top)
        self.entry_age.pack()
        self.label_size = Label(self.frame_top, text="Check dogs size", font=('Arial', 12))
        self.label_size.pack(side=TOP)

        self.size = IntVar()
        self.size_check_s = Radiobutton(self.frame_top, text="Small",variable=self.size, value=1)
        self.size_check_s.pack(side=LEFT)
        self.size_check_m = Radiobutton(self.frame_top, text="Medium",variable=self.size, value=2)
        self.size_check_m.pack(side=LEFT)
        self.size_check_l = Radiobutton(self.frame_top, text="Large",variable=self.size, value=3)
        self.size_check_l.pack(side=LEFT)
        self.size_check_unknown = Radiobutton(self.frame_top, text="Unknown",variable=self.size, value=4)
        self.size_check_unknown.pack(side=LEFT)

        self.variable_name = StringVar(self.frame_top)
        self.names = self.get_names()
        self.variable_name.set("Choose owners name")
        self.pick_name = OptionMenu(root, self.variable_name, *self.names)
        self.pick_name.pack()

        self.button2 = Button(self.frame_bot, text="Confirm", width=15, font=('Arial', 12), command=self.confirm)
        self.button2.pack(side=TOP)
        self.button1 = Button(self.frame_bot, text="Exit", width=15, command=self.uzdaryti)
        self.button1.pack(side=BOTTOM)


    def get_names(self):
        self.all = session.query(Person).all()
        self.listas = []
        for self.entry in self.all:
            self.listas.append((int(self.entry.id),self.entry.name,self.entry.l_name))
        return self.listas

       
    def confirm(self):
        
        try:
            name = self.entry_name.get().capitalize()
            age = int(self.entry_age.get())
            size = self.size.get()
            owner_id = int(re.findall(r'\d+',self.variable_name.get())[0])
            add_dog(name,age,size,owner_id)
            self.entry_name.delete(0, END)
        except:
            print("Fill all entries correctly")
    
    def uzdaryti(self):
        self.root.destroy()


class Add_owner:

    def __init__(self, root):
        self.root = root
        root.title("Add Owner")
        self.root.geometry("250x200")
        self.frame = Frame(self.root)

        self.label_name = Label(self.root, text="Enter name")
        self.label_name.pack(side=TOP)
        self.entry_name = Entry(self.root)
        self.entry_name.pack()
        self.label_l_name = Label(self.root, text="Enter last name")
        self.label_l_name.pack(side=TOP)
        self.entry_l_name = Entry(self.root)
        self.entry_l_name.pack()
        self.label_email = Label(self.root, text="Enter Email")
        self.label_email.pack(side=TOP)
        self.entry_email = Entry(self.root)
        self.entry_email.pack()
        
        self.button2 = Button(self.frame, text="Confirm", width=15, font=('Arial', 12), command=self.confirm)
        self.button2.pack()
        self.button1 = Button(self.frame, text="Exit", width=15, command=self.uzdaryti)
        self.button1.pack()
        self.frame.pack()

    def uzdaryti(self):
        self.root.destroy()

    def confirm(self):
        
        try:
            name = self.entry_name.get().capitalize()
            l_name = self.entry_l_name.get().capitalize()
            email = self.entry_email.get()
            add_person(name, l_name, email)
            self.clean_entries()
        except:
            print("Fill all entries correctly")
        
    

    def clean_entries(self):
        self.entry_name.delete(0, END)
        self.entry_l_name.delete(0, END)
        self.entry_email.delete(0, END)
        
         
               

def main():
    
    root = Tk()
    app = Pagrindinis(root)
    root.mainloop()

if __name__ == '__main__':
    main()