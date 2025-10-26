#!/usr/bin/env python3
"""Script to seed the database with sample authors and books."""

from app import app
from data_models import db, Author, Book
from datetime import date

def seed_database():
    with app.app_context():
        # Clear existing data
        Book.query.delete()
        Author.query.delete()
        
        # Add some authors
        authors_data = [
            {'name': 'J.K. Rowling', 'birth_date': date(1965, 7, 31)},
            {'name': 'George Orwell', 'birth_date': date(1903, 6, 25), 'date_of_death': date(1950, 1, 21)},
            {'name': 'Jane Austen', 'birth_date': date(1775, 12, 16), 'date_of_death': date(1817, 7, 18)},
            {'name': 'Stephen King', 'birth_date': date(1947, 9, 21)},
            {'name': 'Agatha Christie', 'birth_date': date(1890, 9, 15), 'date_of_death': date(1976, 1, 12)}
        ]
        
        for author_data in authors_data:
            author = Author(**author_data)
            db.session.add(author)
        
        db.session.commit()
        print('Authors added successfully!')
        
        # Add some books
        books_data = [
            {'isbn': '9780439708180', 'title': 'Harry Potter and the Philosopher\'s Stone', 'publication_year': 1997, 'author_id': 1},
            {'isbn': '9780451524935', 'title': '1984', 'publication_year': 1949, 'author_id': 2},
            {'isbn': '9780486284736', 'title': 'Pride and Prejudice', 'publication_year': 1813, 'author_id': 3},
            {'isbn': '9780307474278', 'title': 'The Shining', 'publication_year': 1977, 'author_id': 4},
            {'isbn': '9780062073488', 'title': 'Murder on the Orient Express', 'publication_year': 1934, 'author_id': 5},
            {'isbn': '9780439139601', 'title': 'Harry Potter and the Chamber of Secrets', 'publication_year': 1998, 'author_id': 1},
            {'isbn': '9780452284234', 'title': 'Animal Farm', 'publication_year': 1945, 'author_id': 2}
        ]
        
        for book_data in books_data:
            book = Book(**book_data)
            db.session.add(book)
        
        db.session.commit()
        print('Books added successfully!')
        
        # Display summary
        authors_count = Author.query.count()
        books_count = Book.query.count()
        print(f'Database now contains {authors_count} authors and {books_count} books.')

if __name__ == '__main__':
    seed_database()