from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, DateTime, Boolean, ForeignKey, Date
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship


bcrypt = Bcrypt()
db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    __tablename__ = "user"
    
    email = Column(Text, nullable=False, primary_key=True)
    name = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    active_books = Column(Integer, default=0, nullable=False)
    is_flagged = Column(Boolean, default=False, nullable=False)
    last_loggedin = Column(DateTime, nullable=False)
    
    def __init__(self, email, name, password, active_books, is_flagged, last_loggedin):
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.active_books = active_books
        self.is_flagged = is_flagged
        self.last_loggedin = last_loggedin

    def validate(self):
        if not self.email or not self.name or not self.password:
            raise ValueError("Email, name, and password are required.")
        if '@' not in self.email:
            raise ValueError("Invalid email format.")
        if self.active_books < 0:
            raise ValueError("Active books cannot be negative.")
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

class UserSchema(ma.Schema):
    class Meta:
        fields = ("email", "name", "password", "active_books", "is_flagged", "last_loggedin")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Section(db.Model):
    __tablename__ = "section"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    
    books = relationship("Book", back_populates="section", cascade="all, delete-orphan")

    def __init__(self, name, description):
        self.name = name
        self.description = description

class SectionSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description")

section_schema = SectionSchema()
sections_schema = SectionSchema(many=True)

class Book(db.Model):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    author = Column(Text, nullable=False)
    genre = Column(Text, nullable=False)
    section_id = Column(Integer, ForeignKey("section.id"), nullable=False)
    content = Column(Text, nullable=True)
    section = relationship("Section", backref="books")
    
    section = relationship("Section", back_populates="books")
    requests = relationship("RequestBook", back_populates="book", cascade="all, delete-orphan")

    def __init__(self, name, author, genre, section_id, content=None):
        self.name = name
        self.author = author
        self.genre = genre
        self.section_id = section_id
        self.content = content
        
    def validate(self):
        if not self.name or not self.author or not self.genre:
            raise ValueError("Name, author, and genre are required.")
        if self.section_id <= 0:
            raise ValueError("Invalid section ID.")
        
class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "author", "genre", "section_id", "content", "cover_photo")
        
book_schema = BookSchema()
books_schema = BookSchema(many=True)

class RequestBook(db.Model):
    __tablename__ = "request_book"
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_mail = Column(Integer, db.ForeignKey('user.email'))
    book_id = Column(Integer, db.ForeignKey('book.id'))
    is_requested = Column(Boolean, default=False, nullable=True)
    is_approved = Column(Boolean, default=False, nullable=True)
    is_rejected = Column(Boolean, default=False, nullable=True)
    is_returned = Column(Boolean, default=False, nullable=True)
    issue_date = Column(Date, nullable=True)
    return_date = Column(Date, nullable=True)
    user = relationship('User', backref='requests')
    book = relationship('Book', back_populates='requests')
    
    def validate(self):
        if not self.user_mail or not self.book_id:
            raise ValueError("User email and book ID are required.")
        if self.issue_date and self.return_date and self.issue_date > self.return_date:
            raise ValueError("Issue date cannot be later than return date.")
    
class RequestBookSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_mail", "book_id", "is_requested", "is_approved", "is_rejected", "is_returned", "issue_date", "return_date")
        
request_book_schema = RequestBookSchema()
request_books_schema = RequestBookSchema(many=True)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_mail = Column(Integer, ForeignKey('user.email'))
    book_id = Column(Integer, ForeignKey('book.id'))
    feedback = Column(Text, nullable=True)
    user = db.relationship('User', backref='feedbacks')
    book = db.relationship('Book', backref='feedbacks')
    
    def validate(self):
        if not self.user_mail or not self.book_id:
            raise ValueError("User email and book ID are required.")
        