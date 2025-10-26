from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """Author model representing authors in the library system."""
    
    # Table columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date)
    
    # Relationship with books (one author can have many books)
    books = db.relationship('Book', backref='author', lazy=True)
    
    def __repr__(self):
        """String representation for debugging."""
        return f'<Author {self.id}: {self.name}>'
    
    def __str__(self):
        """Human-readable string representation."""
        return f'{self.name} (ID: {self.id})'


class Book(db.Model):
    """Book model representing books in the library system."""
    
    # Table columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer)
    
    # Foreign key to link with Author
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    
    def __repr__(self):
        """String representation for debugging."""
        return f'<Book {self.id}: {self.title} (ISBN: {self.isbn})>'
    
    def __str__(self):
        """Human-readable string representation."""
        return f'{self.title} by {self.author.name if self.author else "Unknown Author"}'


# Create tables - run this once to create the database tables
# You can uncomment and run the following code to create tables:
#
# if __name__ == "__main__":
#     from app import app
#     with app.app_context():
#         db.create_all()
#         print("Database tables created successfully!")