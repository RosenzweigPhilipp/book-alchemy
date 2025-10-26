import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

# Create Flask application instance
app = Flask(__name__)

# Configure database URI
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Required for flash messages

# Initialize the database with the Flask app
db.init_app(app)


@app.route('/')
def home():
    """Home page displaying all books with optional sorting and searching."""
    sort_by = request.args.get('sort', 'title')  # Default sort by title
    search_query = request.args.get('search', '').strip()  # Get search query
    
    # Start with base query
    if search_query:
        # Search in book title, author name, and ISBN
        books_query = Book.query.join(Author).filter(
            db.or_(
                Book.title.ilike(f'%{search_query}%'),
                Author.name.ilike(f'%{search_query}%'),
                Book.isbn.ilike(f'%{search_query}%')
            )
        )
    else:
        # No search, get all books
        books_query = Book.query.join(Author)
    
    # Apply sorting
    if sort_by == 'author':
        books = books_query.order_by(Author.name).all()
    elif sort_by == 'year':
        books = books_query.order_by(Book.publication_year.desc()).all()
    else:  # default to title
        books = books_query.order_by(Book.title).all()
    
    return render_template('home.html', books=books, current_sort=sort_by, search_query=search_query)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Add a new author to the database."""
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date'] if request.form['birth_date'] else None
        date_of_death = request.form['date_of_death'] if request.form['date_of_death'] else None
        
        # Convert empty strings to None for date fields
        from datetime import datetime
        if birth_date:
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        if date_of_death:
            date_of_death = datetime.strptime(date_of_death, '%Y-%m-%d').date()
        
        # Create new author
        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death
        )
        
        try:
            db.session.add(new_author)
            db.session.commit()
            flash(f'Author "{name}" has been successfully added!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding author: {str(e)}', 'error')
        
        return redirect(url_for('add_author'))
    
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Add a new book to the database."""
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']
        
        # Convert publication_year to int if provided
        if publication_year:
            publication_year = int(publication_year)
        else:
            publication_year = None
        
        # Create new book
        new_book = Book(
            isbn=isbn,
            title=title,
            publication_year=publication_year,
            author_id=int(author_id)
        )
        
        try:
            db.session.add(new_book)
            db.session.commit()
            flash(f'Book "{title}" has been successfully added!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding book: {str(e)}', 'error')
        
        return redirect(url_for('add_book'))
    
    # Get all authors for the dropdown
    authors = Author.query.order_by(Author.name).all()
    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Delete a book from the database."""
    book = Book.query.get_or_404(book_id)
    book_title = book.title
    author = book.author
    
    try:
        # Delete the book
        db.session.delete(book)
        db.session.commit()
        
        # Check if the author has any other books
        remaining_books = Book.query.filter_by(author_id=author.id).count()
        
        if remaining_books == 0:
            # Delete the author if they have no more books
            db.session.delete(author)
            db.session.commit()
            flash(f'Book "{book_title}" and its author "{author.name}" have been deleted (author had no other books).', 'success')
        else:
            flash(f'Book "{book_title}" has been successfully deleted!', 'success')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting book: {str(e)}', 'error')
    
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)