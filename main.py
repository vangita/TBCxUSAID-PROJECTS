import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from db_setup import create_database, Book,Author ,author_book_relationship
from data_generator import insert_authors, insert_books ,insert_writes
from queries import (get_book_with_most_pages, get_average_pages, get_youngest_author,
                     get_authors_without_books, get_authors_with_more_than_three_books)

def is_table_empty(session, table):
    count = session.query(func.count(table.id)).scalar()
    return count == 0


def main():
    create_database()

    engine = create_engine('sqlite:///BooksAndAuthors.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    if is_table_empty(session, Author):
        insert_authors(session)
    if is_table_empty(session, Book):
        insert_books(session)

    if session.query(author_book_relationship).count()==0:
        insert_writes(session)

    books_with_most_pages = get_book_with_most_pages(session)
    print("Books with the most pages:")
    for book in books_with_most_pages:
        print(f"({book.id}, {book.title}, {book.category_name}, "
              f"{book.page_count}, {book.issue_date})")

    average_pages = get_average_pages(session)
    print("\nAverage number of pages:\n", average_pages)

    youngest_author = get_youngest_author(session)
    print("\nYoungest author:\n", f"{youngest_author.first_name} {youngest_author.last_name} born in {youngest_author.birth_date}")

    print("\nAuthors without books:")
    authors_without_books = get_authors_without_books(session)
    for author in authors_without_books:
        print(f"{author.first_name} {author.last_name}")

    authors_with_many_books = get_authors_with_more_than_three_books(session)
    print("\nAuthors with more than 3 books:")
    for author in authors_with_many_books:
        print(f"{author.first_name} {author.last_name} - {author[2]} books")

    session.close()


if __name__ == '__main__':
    main()
