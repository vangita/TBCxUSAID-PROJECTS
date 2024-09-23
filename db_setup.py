from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship , declarative_base

Base = declarative_base()


author_book_relationship = Table('writes', Base.metadata,
Column('author_id', Integer, ForeignKey('author.id')),
    Column('book_id', Integer, ForeignKey('book.id'))
)

class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True , autoincrement=True)
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    birth_date = Column(String,nullable=False)
    birthplace = Column(String,nullable=False)

    books=relationship("Book", secondary=author_book_relationship, back_populates="authors")


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String,nullable=False)
    category_name = Column(String,nullable=False)
    page_count = Column(Integer,nullable=False)
    issue_date = Column(String,nullable=False)

    authors = relationship("Author",secondary=author_book_relationship, back_populates="books")


def create_database():
    engine = create_engine('sqlite:///BooksAndAuthors.db')
    Base.metadata.create_all(engine)
