from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dogs_db import Person, Dogs, Courses, Size
from tkinter import *


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


# add_person("Petras", "Stulpinas", "ps@gmail.com")
# add_person("Jonas", "Jonaitis", "jj@gmail.com")
# add_person("Zigmas", "Ponaitis", "zp@gmail.com")

# add_dog_size("Small")
# add_dog_size("Medium")
# add_dog_size("Large")

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
