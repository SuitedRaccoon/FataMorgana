-- Insert sample users
INSERT INTO users (username, email, password) VALUES 
('alice', 'alice@example.com', 'hashed_password1'),
('bob', 'bob@example.com', 'hashed_password2');

-- Insert sample books
INSERT INTO books (title, author, genre, year_published) VALUES
('Brave New World', 'Aldous Huxley', 'Dystopian', 1932),
('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 1937),
('Pride and Prejudice', 'Jane Austen', 'Romance', 1813),
('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 1925),
('The Road', 'Cormac McCarthy', 'Post-Apocalyptic', 2006),
('Frankenstein', 'Mary Shelley', 'Horror', 1818),
('Beloved', 'Toni Morrison', 'Historical Fiction', 1987),
('Catch-22', 'Joseph Heller', 'Satire', 1961),
('Dracula', 'Bram Stoker', 'Gothic', 1897),
('Fahrenheit 451', 'Ray Bradbury', 'Sci-Fi', 1953),
('A Game of Thrones', 'George R. R. Martin', 'Fantasy', 1996),
('The Catcher in the Rye', 'J.D. Salinger', 'Classic', 1951),
('Slaughterhouse-Five', 'Kurt Vonnegut', 'Absurdist Fiction', 1969),
('Crime and Punishment', 'Fyodor Dostoevsky', 'Philosophical Fiction', 1866),
('The Alchemist', 'Paulo Coelho', 'Adventure', 1988),
('Norwegian Wood', 'Haruki Murakami', 'Romance', 1987),
('The Brothers Karamazov', 'Fyodor Dostoevsky', 'Philosophy', 1880),
('The Picture of Dorian Gray', 'Oscar Wilde', 'Gothic', 1890),
('Les Misérables', 'Victor Hugo', 'Historical Fiction', 1862),
('The Shining', 'Stephen King', 'Horror', 1977),
('The Stranger', 'Albert Camus', 'Philosophical Fiction', 1942),
('Don Quixote', 'Miguel de Cervantes', 'Adventure', 1605),
('Moby-Dick', 'Herman Melville', 'Adventure', 1851),
('Life of Pi', 'Yann Martel', 'Fantasy', 2001),
('Gone Girl', 'Gillian Flynn', 'Thriller', 2012),
('The Martian', 'Andy Weir', 'Sci-Fi', 2011),
('Educated', 'Tara Westover', 'Memoir', 2018),
('The Book Thief', 'Markus Zusak', 'Historical Fiction', 2005),
('It', 'Stephen King', 'Horror', 1986),
('A Brief History of Time', 'Stephen Hawking', 'Science', 1988),
('Thinking, Fast and Slow', 'Daniel Kahneman', 'Psychology', 2011),
('The Power of Now', 'Eckhart Tolle', 'Spirituality', 1997),
('Atomic Habits', 'James Clear', 'Self-Help', 2018),
('The Midnight Library', 'Matt Haig', 'Fantasy', 2020),
('Siddhartha', 'Hermann Hesse', 'Philosophical Fiction', 1922),
('The Silent Patient', 'Alex Michaelides', 'Thriller', 2019),
('Where the Crawdads Sing', 'Delia Owens', 'Mystery', 2018),
('Normal People', 'Sally Rooney', 'Contemporary', 2018),
('Circe', 'Madeline Miller', 'Mythology', 2018),
('Becoming', 'Michelle Obama', 'Biography', 2018),
('The Kite Runner', 'Khaled Hosseini', 'Historical Fiction', 2003),
('The Name of the Wind', 'Patrick Rothfuss', 'Fantasy', 2007),
('Anxious People', 'Fredrik Backman', 'Comedy Drama', 2019),
('Shōgun', 'James Clavell', 'Historical Fiction', 1975),
('Cloud Atlas', 'David Mitchell', 'Speculative Fiction', 2004),
('The Vanishing Half', 'Brit Bennett', 'Contemporary', 2020),
('The Bell Jar', 'Sylvia Plath', 'Psychological Fiction', 1963),
('The Secret History', 'Donna Tartt', 'Mystery', 1992),
('The Giver', 'Lois Lowry', 'Dystopian', 1993),
('Project Hail Mary', 'Andy Weir', 'Sci-Fi', 2021);


-- Insert reading queues
INSERT INTO user_books (user_id, book_id, status, queue_position) VALUES
(1, 6, 'planned', 4),
(1, 7, 'planned', 5),
(1, 8, 'reading', 6),
(1, 9, 'reading', 7),
(1, 10, 'completed', 8),
(1, 11, 'planned', 9),
(1, 12, 'reading', 10),
(1, 13, 'reading', 11),
(1, 14, 'completed', 12),
(1, 15, 'skipped', 13),
(1, 16, 'planned', 14),
(1, 17, 'completed', 15),
(1, 18, 'skipped', 16),
(1, 19, 'planned', 17),
(1, 20, 'reading', 18),
(1, 21, 'completed', 19),
(1, 22, 'skipped', 20),
(1, 23, 'planned', 21),
(1, 24, 'planned', 22),
(1, 25, 'completed', 23),
(1, 26, 'planned', 24),
(1, 27, 'reading', 25),
(1, 28, 'reading', 26),
(1, 29, 'planned', 27),
(1, 30, 'skipped', 28),
(1, 31, 'completed', 29),
(1, 32, 'planned', 30),
(1, 33, 'reading', 31),
(1, 34, 'skipped', 32),
(1, 35, 'reading', 33);


-- Insert saved lists
INSERT INTO saved_lists (user_id, name) VALUES
(1, 'Summer Reads'),
(1, 'Top Fantasy'),
(1, 'Dystopian Musts'),
(1, 'Romance Picks'),
(1, 'Historical Gems'),
(1, 'Philosophy Stack'),
(1, 'Books to Cry With'),
(1, 'Mind Expanders'),
(1, 'Feel Good Reads'),
(1, 'Deep Dive Nonfiction');

-- Add books to lists
INSERT INTO saved_list_books (list_id, book_id) VALUES
-- Summer Reads (ID 1)
(1, 2), (1, 6), (1, 20), (1, 28), (1, 33), (1, 39),
-- Top Fantasy (ID 2)
(2, 11), (2, 24), (2, 41), (2, 42), (2, 34), (2, 35), (2, 48),
-- Dystopian Musts (ID 3)
(3, 1), (3, 10), (3, 49), (3, 50), (3, 31), (3, 29),
-- Romance Picks (ID 4)
(4, 3), (4, 16), (4, 37), (4, 36), (4, 25), (4, 19),
-- Historical Gems (ID 5)
(5, 19), (5, 27), (5, 43), (5, 44), (5, 20), (5, 40),
-- Philosophy Stack (ID 6)
(6, 14), (6, 17), (6, 21), (6, 33), (6, 38),
-- Books to Cry With (ID 7)
(7, 27), (7, 30), (7, 41), (7, 34), (7, 25), (7, 18), (7, 26),
-- Mind Expanders (ID 8)
(8, 30), (8, 31), (8, 32), (8, 45), (8, 46),
-- Feel Good Reads (ID 9)
(9, 12), (9, 35), (9, 36), (9, 28), (9, 32),
-- Deep Dive Nonfiction (ID 10)
(10, 29), (10, 30), (10, 31), (10, 32), (10, 39), (10, 40);

