from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///dogs.db')
Base = declarative_base()

filler = Table('doggy_courses', Base.metadata,
        Column('dogs_id',Integer, ForeignKey("dogs.id")),
        Column('courses_id',Integer, ForeignKey("courses.id"))
)


class Person(Base):
    
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement = True)
    name = Column("name", String)
    l_name = Column("l_name", String)
    email = Column("email", String)
    dogs = relationship("Dogs", back_populates="owner")
        
    def __repr__(self):
        return f'{self.id:<3}{self.name:<15}{self.l_name:<15} {self.email:>12}'

class Dogs(Base):
    
    __tablename__ = 'dogs'
    id = Column(Integer, primary_key=True, autoincrement = True)
    name = Column("name", String)
    age = Column("age", Integer)
    size_id = Column(Integer, ForeignKey("size.id"))
    person_id = Column(Integer, ForeignKey("person.id"))
    size = relationship("Size", back_populates = 'dogs')
    owner = relationship("Person", back_populates="dogs")
    courses = relationship("Courses",secondary=filler, back_populates = "dogs")
     
    def __repr__(self):
        return f'{self.name}'
   
class Courses(Base):
    
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, autoincrement = True)
    discipline = Column("discipline", String)
    dogs = relationship("Dogs",secondary=filler, back_populates= "courses")
    
     
    def __repr__(self):
        return f'{self.id:<3}{self.discipline}'     

class Size(Base):
    
    __tablename__ = 'size'
    id = Column(Integer, primary_key=True, autoincrement = True)
    size = Column("size", String)
    dogs = relationship('Dogs', back_populates='size')
    
        
    def __repr__(self):
        return f'{self.id:<3}{self.size}'     

Base.metadata.create_all(engine)
