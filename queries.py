from sqlalchemy import func
from db_setup import Author, Book ,author_book_relationship

def get_book_with_most_pages(session):
    max_pages = session.query(func.max(Book.page_count)).scalar()
    books = session.query(Book).filter(Book.page_count == max_pages).all()
    return books

def get_average_pages(session):
    return session.query(func.avg(Book.page_count)).scalar()

def get_youngest_author(session):
    return session.query(Author).order_by(Author.birth_date.desc()).first()


def get_authors_without_books(session):
    return session.query(Author).filter(~Author.id.in_(
        session.query(author_book_relationship.c.author_id)
    )).all()


def get_authors_with_more_than_three_books(session):
    return (session.query(Author.first_name,Author.last_name, func.count(Book.id))
            .join(author_book_relationship, Author.id==author_book_relationship.c.author_id)
            .join(Book, author_book_relationship.c.book_id==Book.id)
            .group_by(Author.id)
            .having(func.count(author_book_relationship.c.book_id) > 3)
            .limit(5)
            .all())
