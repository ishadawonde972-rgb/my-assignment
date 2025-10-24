


GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Fantasy", "Biography", "History")


books = {}
# members: list of dicts with keys: 'member_id', 'name', 'email', 'borrowed_books'
members = []


def add_book(isbn, title, author, genre, total_copies):

    # Validate inputs simply
    if not isbn or not title or not author:
        return False
    if genre not in GENRES:
        return False
    if isbn in books:
        # ISBN must be unique
        return False
    try:
        total = int(total_copies)
    except (ValueError, TypeError):
        return False
    if total < 1:
        return False


    books[isbn] = {
        "title": title,
        "author": author,
        "genre": genre,
        "total_copies": total,
        "available_copies": total,
    }
    return True


def add_member(member_id, name, email):

    if not member_id or not name or not email:
        return False
    # Check uniqueness of member_id
    for m in members:
        if m["member_id"] == member_id:
            return False
    members.append({
        "member_id": member_id,
        "name": name,
        "email": email,
        "borrowed_books": []
    })
    return True


def _find_member(member_id):

    for m in members:
        if m["member_id"] == member_id:
            return m
    return None


def search_books(query, by="title"):

    results = []
    q = str(query).lower()
    if by not in ("title", "author"):
        by = "title"
    for isbn, info in books.items():
        field = info.get(by, "").lower()
        if q in field:
            # copy and include isbn
            r = info.copy()
            r["isbn"] = isbn
            results.append(r)
    return results


def update_book(isbn, title=None, author=None, genre=None, total_copies=None):

    if isbn not in books:
        return False
    book = books[isbn]
    if genre is not None and genre not in GENRES:
        return False
    if title is not None:
        book["title"] = title
    if author is not None:
        book["author"] = author
    if genre is not None:
        book["genre"] = genre
    if total_copies is not None:
        try:
            new_total = int(total_copies)
        except (ValueError, TypeError):
            return False
        if new_total < 0:
            return False
        # Adjust available_copies relative to change in total
        diff = new_total - book["total_copies"]
        book["total_copies"] = new_total
        book["available_copies"] = book.get("available_copies", 0) + diff
        if book["available_copies"] < 0:
            # cannot make available copies negative
            book["available_copies"] = 0
    return True


def update_member(member_id, name=None, email=None):

    m = _find_member(member_id)
    if not m:
        return False
    if name is not None:
        m["name"] = name
    if email is not None:
        m["email"] = email
    return True


def delete_book(isbn):

    if isbn not in books:
        return False
    book = books[isbn]
    if book.get("available_copies", 0) != book.get("total_copies", 0):
        # there are borrowed copies
        return False
    del books[isbn]
    return True


def delete_member(member_id):

    for i, m in enumerate(members):
        if m["member_id"] == member_id:
            if m.get("borrowed_books"):
                if len(m["borrowed_books"]) > 0:
                    return False
            # safe to remove
            members.pop(i)
            return True
    return False


def borrow_book(isbn, member_id):

    if isbn not in books:
        return False
    book = books[isbn]
    if book.get("available_copies", 0) <= 0:
        return False
    m = _find_member(member_id)
    if not m:
        return False
    if len(m.get("borrowed_books", [])) >= 3:
        return False
    # proceed with borrow
    book["available_copies"] -= 1
    m["borrowed_books"].append(isbn)
    return True


def return_book(isbn, member_id):

    if isbn not in books:
        return False
    m = _find_member(member_id)
    if not m:
        return False
    if isbn not in m.get("borrowed_books", []):
        return False

    m["borrowed_books"].remove(isbn)
    books[isbn]["available_copies"] += 1
    # ensure available_copies does not exceed total_copies
    if books[isbn]["available_copies"] > books[isbn]["total_copies"]:
        books[isbn]["available_copies"] = books[isbn]["total_copies"]
    return True
