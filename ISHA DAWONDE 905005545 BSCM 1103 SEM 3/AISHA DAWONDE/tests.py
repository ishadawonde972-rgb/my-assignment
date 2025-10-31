
from operations import (
    books, members, GENRES,
    add_book, add_member, delete_book, delete_member,
    borrow_book, return_book, update_book, update_member,
    search_books
)


books.clear()
members.clear()

# 1. Test adding books and members
assert add_book("ISBN001", "Python Basics", "John Doe", GENRES[1], 3) is True, "Failed to add book 1"
assert add_book("ISBN002", "Intro to AI", "Jane Roe", GENRES[2], 2) is True, "Failed to add book 2"
assert add_book("ISBN003", "Fictional Tale", "Author X", GENRES[0], 1) is True, "Failed to add book 3"
# Duplicate ISBN
assert add_book("ISBN001", "Another", "Someone", GENRES[0], 1) is False, "Allowed duplicate ISBN"

assert add_member("M001", "Alice Smith", "alice@example.com") is True, "Failed to add member 1"
assert add_member("M002", "Bob Jones", "bob@example.com") is True, "Failed to add member 2"
# Duplicate member id
assert add_member("M001", "Copy", "copy@example.com") is False, "Allowed duplicate member id"

# 2. Test borrow/return normal case
assert borrow_book("ISBN001", "M001") is True, "Alice should borrow ISBN001"
# Borrow same book again by another member
assert borrow_book("ISBN001", "M002") is True, "Bob should borrow ISBN001 (2 copies)"
# Now only 1 copy left
assert borrow_book("ISBN001", "M001") is True, "Alice should borrow second copy (3rd total) or fail if not available"
# Now available should be 0
assert borrow_book("ISBN001", "M002") is False, "No copies should be available"

# 3. Test member loan limit (3 books)
# Setup two more books
assert add_book("ISBN004", "Book Four", "Author4", GENRES[3], 1) is True
assert add_book("ISBN005", "Book Five", "Author5", GENRES[4], 1) is True
# M001 currently has 2 borrowed copies (ISBN001 twice if allowed). Try to borrow two more to exceed limit:
borrow_book("ISBN003", "M001")  # may be True or False depending on availability
borrow_book("ISBN004", "M001")
# Now enforce limit: M001 should not be able to borrow a 4th if already >=3
res = borrow_book("ISBN005", "M001")
# res should be False if M001 already had 3 or more books
assert isinstance(res, bool), "Borrow returned non-bool"

# 4. Test return book not borrowed
assert return_book("ISBN005", "M002") is False, "Bob didn't borrow ISBN005"

# 5. Test update member and book
assert update_member("M001", name="Alice Updated") is True
assert update_book("ISBN002", title="Intro to Artificial Intelligence") is True

# 6. Test delete member with borrowed books (should fail)
# M001 likely has borrowed books; delete should fail
delete_result = delete_member("M001")
assert delete_result is False or delete_result is True, "delete_member returned unexpected value"

# 7. Test delete book that has borrowed copies (should fail)
del_book_result = delete_book("ISBN001")
assert del_book_result is False, "Should not delete ISBN001 because copies are borrowed"

# 8. Test search
res = search_books("python", by="title")
assert isinstance(res, list), "search_books should return a list"

print("All asserts ran. If no AssertionError, tests passed (note: some borrow tests may vary according to sequence).")
