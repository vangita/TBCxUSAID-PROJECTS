import random
from faker import Faker
from db_setup import Author, Book, author_book_relationship

fake = Faker()

def insert_authors(session):
    authors = [Author(first_name=fake.first_name(),
                      last_name=fake.last_name(),
                      birth_date=fake.date_between(start_date='-65y', end_date='-25y').isoformat(),
                      birthplace=fake.city())
               for _ in range(500)]
    session.add_all(authors)
    session.commit()


def insert_books(session):
    books = [Book(title=fake.text(max_nb_chars=20),
                  category_name=fake.word(),
                  page_count=fake.random_int(min=100, max=1000),
                  issue_date=fake.date_this_century().isoformat())
             for _ in range(1000)]
    session.add_all(books)
    session.commit()

def insert_writes(session):
    for i in range(1000):
        author_id = random.randint(1, 500)
        session.execute(author_book_relationship.insert().values(author_id=author_id, book_id=i))
    session.commit()
