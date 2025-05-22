import json
import os

class Book:
    def __init__(self, title, author, year, isbn):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn

    def __str__(self):
        return f"'{self.title}' by {self.author} ({self.year}) - ISBN: {self.isbn}"

class Library:
    def __init__(self, filepath="library_data.json"):
        self.filepath = filepath
        self.books = []
        self.load_books()

    def load_books(self):
        """Load books from JSON file if exists"""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    data = json.load(f)
                    for item in data:
                        book = Book(item['title'], item['author'], item['year'], item['isbn'])
                        self.books.append(book)
                print(f"Loaded {len(self.books)} books from file.")
            except Exception as e:
                print(f"Error loading books: {e}")
        else:
            print("No saved library data found. Starting with an empty library.")

    def save_books(self):
        """Save books to JSON file"""
        try:
            with open(self.filepath, 'w') as f:
                json.dump([book.__dict__ for book in self.books], f, indent=4)
            print("Library data saved.")
        except Exception as e:
            print(f"Error saving books: {e}")

    def add_book(self, title, author, year, isbn):
        new_book = Book(title, author, year, isbn)
        self.books.append(new_book)
        print(f"Added book: {new_book}")

    def view_books(self):
        if not self.books:
            print("Library is empty.")
            return
        print("\nBooks in Library:")
        for idx, book in enumerate(self.books, 1):
            print(f"{idx}. {book}")

    def search_by_author(self, author_name):
        results = [book for book in self.books if author_name.lower() in book.author.lower()]
        if results:
            print(f"\nBooks by authors matching '{author_name}':")
            for book in results:
                print(book)
        else:
            print(f"No books found by author '{author_name}'.")

    def search_by_title(self, title_keyword):
        results = [book for book in self.books if title_keyword.lower() in book.title.lower()]
        if results:
            print(f"\nBooks with titles matching '{title_keyword}':")
            for book in results:
                print(book)
        else:
            print(f"No books found with title containing '{title_keyword}'.")

def main_menu():
    library = Library()

    while True:
        print("\n--- Library Management System ---")
        print("1. View all books")
        print("2. Add a new book")
        print("3. Search books by author")
        print("4. Search books by title")
        print("5. Save and Exit")
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            library.view_books()
        elif choice == '2':
            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()
            year = input("Enter publication year: ").strip()
            isbn = input("Enter ISBN: ").strip()
            if not (title and author and year and isbn):
                print("All fields are required.")
                continue
            if not year.isdigit():
                print("Year must be numeric.")
                continue
            library.add_book(title, author, int(year), isbn)
        elif choice == '3':
            author = input("Enter author name to search: ").strip()
            if author:
                library.search_by_author(author)
            else:
                print("Author name cannot be empty.")
        elif choice == '4':
            title = input("Enter title keyword to search: ").strip()
            if title:
                library.search_by_title(title)
            else:
                print("Title keyword cannot be empty.")
        elif choice == '5':
            library.save_books()
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main_menu()
