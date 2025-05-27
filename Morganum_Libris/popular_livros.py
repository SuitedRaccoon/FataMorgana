# popular_livros.py

import requests
import MySQLdb
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

def fetch_subject_works(subject, limit, offset):
    url = f'https://openlibrary.org/subjects/{subject}.json?limit={limit}&offset={offset}'
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json().get('works', [])

def main():
    # 1. Connect to MySQL
    db = MySQLdb.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        passwd=MYSQL_PASSWORD,
        db=MYSQL_DB,
        charset='utf8mb4'
    )
    cur = db.cursor()
    
    # 2. Expand your subject list
    subjects = [
        'science', 'fantasy', 'romance', 'history', 'philosophy',
        'mystery', 'thriller', 'biography', 'children', 'poetry',
        'adventure', 'humor'
    ]
    
    # 3. Parameters: 3 pages of 100 works each → up to 300 books per subject
    per_page = 100
    pages = 3

    seen_isbns = set()
    inserted = 0
    ignored = 0
    errors = 0

    for subj in subjects:
        for page in range(pages):
            offset = page * per_page
            try:
                works = fetch_subject_works(subj, per_page, offset)
            except Exception as e:
                print(f"[ERROR] fetching {subj} page {page}: {e}")
                continue

            if not works:
                break  # no more works on further pages

            for w in works:
                # 4. Determine an ISBN-like key
                isbn = (w.get('cover_edition_key') or
                        (w.get('edition_key') or [''])[0]).strip()
                if not isbn or isbn in seen_isbns:
                    continue
                seen_isbns.add(isbn)

                title   = w.get('title', '').strip()
                authors = w.get('authors', [])
                author  = (authors[0].get('name') if authors else 'Unknown').strip()
                year    = w.get('first_publish_year')
                genre   = subj

                # 5. Insert or ignore
                try:
                    cur.execute(
                        """
                        INSERT IGNORE INTO books
                          (title, author, genre, year_published, isbn)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (title, author, genre, year, isbn)
                    )

                    if cur.rowcount == 1:
                        inserted += 1
                        print(f"[+INSERT] {title!r} ({isbn})")
                    else:
                        ignored += 1
                        # duplicates within this run are unlikely now
                    db.commit()

                except Exception as e:
                    errors += 1
                    db.rollback()
                    print(f"[ERROR] Inserting {title!r} ({isbn}): {e}")

    # 6. Summary
    cur.close()
    db.close()
    print("\n=== POPULATION SUMMARY ===")
    print(f"Subjects scanned    : {len(subjects)}")
    print(f"Pages per subject   : {pages} × {per_page} works")
    print(f"Unique keys seen    : {len(seen_isbns)}")
    print(f"Books successfully inserted : {inserted}")
    print(f"Rows ignored (duplicates)   : {ignored}")
    print(f"Errors during insert         : {errors}")

if __name__ == '__main__':
    main()
