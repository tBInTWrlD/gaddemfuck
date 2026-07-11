from app.database import Base, SessionLocal, engine
from app.models.book import Book
from app.repositories.book_repository import BookRepository

Base.metadata.create_all(bind=engine)

db = SessionLocal()

repository = BookRepository(db)

book = Book(
    title="Высоконагруженные приложения",
    author="Мартин Клеппман",
)

repository.create(book)

books = repository.get_all()

for book in books:
    print(book.id, book.title, book.author)

db.close()