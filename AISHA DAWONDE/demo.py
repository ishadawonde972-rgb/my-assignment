
from operations import (
    books, members, GENRES,
    add_book, add_member, search_books,
    borrow_book, return_book, update_book, update_member,
    delete_book, delete_member
)
import pprint
pp = pprint.PrettyPrinter(indent=2)

def print_state(step):
    print("\n" + "="*40)
    print(f"STATE AFTER: {step}")
    print("- Books:")
    pp.pprint(books)
    print("- Members:")
    pp.pprint(members)
    print("="*40 + "\n")

def main():
    print("Demo: Mini Library Management System ")

    # Initialize genres (already in operations.py)
    print("GENRES available:", GENRES)

    # Add books (5)
    add_book("1001", "Python Basics", "John Doe", "Non-Fiction", 3)
    add_book("1002", "Learning Java", "Jane Roe", "Non-Fiction", 2)
    add_book("1003", "Space Adventures", "A. Space", "Sci-Fi", 1)
    add_book("1004", "Fantasy World", "F. Writer", "Fantasy", 2)
    add_book("1005", "History of Town", "H. Author", "History", 1)
    print_state("Adding 5 books")

    # Add members (3)
    add_member("M001", "Alice Smith", "alice@example.com")
    add_member("M002", "Bob Jones", "bob@example.com")
    add_member("M003", "Charlie Lee", "charlie@example.com")
    print_state("Adding 3 members")

    # Search books by author
    results = search_books("john", by="author")
    print("Search by author 'john' results:")
    pp.pprint(results)

    # Borrow books
    print("Alice (M001) borrows 1001")
    borrow_book("1001", "M001")
    print_state("Alice borrowed 1001")

    print("Bob (M002) borrows 1001")
    borrow_book("1001", "M002")
    print_state("Bob borrowed 1001")

    # Try to borrow an unavailable book
    print("Try to borrow unavailable book 1003 twice")
    borrow_book("1003", "M001")
    ok = borrow_book("1003", "M002")
    print("Second borrow attempt for 1003 succeeded?" , ok)
    print_state("Tried borrowing 1003 twice")

    # Return a book
    print("Alice returns 1001")
    return_book("1001", "M001")
    print_state("Alice returned 1001")

    # Update a book and a member
    print("Updating book 1002 title and member M003 email")
    update_book("1002", title="Learning Java - 2nd Edition")
    update_member("M003", email="charlie.new@example.com")
    print_state("Updated book and member")

    # Try to delete a book with borrowed copies (should fail)
    print("Attempting to delete book 1001 (should fail if borrowed)")
    res = delete_book("1001")
    print("Delete 1001 result:", res)
    print_state("Tried delete 1001")

    # Return all borrowed books by Bob to allow deletion
    print("Returning Bob's books")
    for isbn in members[1]["borrowed_books"][:]:
        return_book(isbn, "M002")
    print_state("Returned Bob's books")

    # Now attempt delete if possible
    print("Attempting to delete book 1001 again")
    res = delete_book("1001")
    print("Delete 1001 result:", res)
    print_state("Final state")

if __name__ == "__main__":
    main()
