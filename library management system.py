import csv
import mysql.connector

# Define the list of books
books = [

    ["To Kill a Mockingbird", "Harper Lee", 10, "Fiction"],
    ["1984", "George Orwell", 15, "Dystopian"],
    ["Pride and Prejudice", "Jane Austen", 12, "Romance"],
    ["The Great Gatsby", "F. Scott Fitzgerald", 8, "Classic"],
    ["The Catcher in the Rye", "J.D. Salinger", 7, "Coming of Age"],
    ["Moby-Dick", "Herman Melville", 5, "Adventure"],
    ["The Lord of the Rings", "J.R.R. Tolkien", 20, "Fantasy"],
    ["The Hobbit", "J.R.R. Tolkien", 18, "Fantasy"],
    ["Brave New World", "Aldous Huxley", 9, "Science Fiction"],
    ["The Chronicles of Narnia", "C.S. Lewis", 14, "Fantasy"],
    ["War and Peace", "Leo Tolstoy", 11, "Historical Fiction"],
    ["Crime and Punishment", "Fyodor Dostoevsky", 6, "Psychological Thriller"],
    ["The Odyssey", "Homer", 13, "Epic Poetry"],
    ["The Grapes of Wrath", "John Steinbeck", 7, "Classic"],
    ["Frankenstein", "Mary Shelley", 8, "Gothic Fiction"],
    ["The Hunger Games", "Suzanne Collins", 12, "Dystopian"],
    ["The Road", "Cormac McCarthy", 10, "Post-Apocalyptic"],
    ["The Shining", "Stephen King", 9, "Horror"],
    ["Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 25, "Fantasy"],
    ["The Da Vinci Code", "Dan Brown", 14, "Mystery"],
    ["The Alchemist", "Paulo Coelho", 11, "Philosophical Fiction"],
    ["Gone with the Wind", "Margaret Mitchell", 7, "Historical Romance"],
    ["The Hitchhiker's Guide to the Galaxy", "Douglas Adams", 15, "Science Fiction"],
    ["The Sun Also Rises", "Ernest Hemingway", 6, "Modernist"],
    ["The Stranger", "Albert Camus", 8, "Philosophical Fiction"],
    ["The Fault in Our Stars", "John Green", 10, "Young Adult"],
    ["The Girl with the Dragon Tattoo", "Stieg Larsson", 9, "Mystery"],
    ["Catch-22", "Joseph Heller", 7, "Satire"],
    ["Wuthering Heights", "Emily Brontë", 6, "Gothic Fiction"],
    ["The Picture of Dorian Gray", "Oscar Wilde", 8, "Gothic Fiction"],
    ["The Road Not Taken", "Robert Frost", 5, "Poetry"],
    ["The Old Man and the Sea", "Ernest Hemingway", 6, "Adventure"],
    ["One Hundred Years of Solitude", "Gabriel García Márquez", 11, "Magical Realism"],
    ["The Divine Comedy", "Dante Alighieri", 10, "Epic Poetry"],
    ["The Art of War", "Sun Tzu", 12, "Military Strategy"],
    ["The Adventures of Sherlock Holmes", "Arthur Conan Doyle", 14, "Mystery"],
    ["Jane Eyre", "Charlotte Brontë", 9, "Gothic Fiction"],
    ["A Tale of Two Cities", "Charles Dickens", 10, "Historical Fiction"],
    ["The Scarlet Letter", "Nathaniel Hawthorne", 7, "Historical Fiction"],
    ["The Count of Monte Cristo", "Alexandre Dumas", 11, "Adventure"],
    ["Lord of the Flies", "William Golding", 8, "Allegorical"],
    ["The Kite Runner", "Khaled Hosseini", 9, "Historical Fiction"],
    ["The Secret Garden", "Frances Hodgson Burnett", 10, "Children's Literature"],
    ["Dracula", "Bram Stoker", 7, "Gothic Fiction"],
    ["A Game of Thrones", "George R.R. Martin", 12, "Fantasy"],
    ["The Name of the Wind", "Patrick Rothfuss", 9, "Fantasy"],
    ["The Road Less Traveled", "M. Scott Peck", 6, "Psychology"],
    ["The Girl on the Train", "Paula Hawkins", 8, "Thriller"],
    ["The Silent Patient", "Alex Michaelides", 7, "Psychological Thriller"],
    ["Where the Crawdads Sing", "Delia Owens", 10, "Mystery"]

]


# Open the CSV file in write mode and write the book details
with open("book_details.csv", mode='w', newline='') as file:

    writer = csv.writer(file)
    # Write the header row
    writer.writerow(["Book Name", "Author", "Number of Copies Available", "Genre"])
    # Write the book data
    writer.writerows(books)


# Open the CSV file in write mode and create a reservations file
with open("book_reservations.csv", mode='w', newline='') as reservations_file:
    
        writer = csv.writer(reservations_file)
        writer.writerow(["Book Title", "Reserver Name"])


# Create a MySQL database 'library'
def create_database():
    
    mydb = mysql.connector.connect(
        host="Localhost",
        user="root",
        password=""
    )
    
    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS library")

    mydb.commit()
    cursor.close()
    

# Open a MySQL database connection for transactions
def create_transactions_table():
    
    try:
        mydb = mysql.connector.connect(
            host="Localhost",
            user="root",
            password="",
            database="library"
        )
        
        cursor = mydb.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
            book_title VARCHAR(255),
            borrower_name VARCHAR(255),
            borrow_date DATE,
            return_date DATE,
            fine DECIMAL(10,2)
        )''')
        
        mydb.commit()
        cursor.close()

    except mysql.connector.Error as err:
        print("Error:", err)
        print("Failed to create the transactions table. Please try again.")

            
# Open a MySQL database connection for librarians
def create_librarians_table():
    
    try:
        mydb = mysql.connector.connect(
            host="Localhost",
            user="root",
            password="",
            database="library"
        )
        
        cursor = mydb.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS librarians (
            name varchar(20),
            Age int(2),
            Phone_no int(20),
            Sex char(1)
        )''')
        
        mydb.commit()
        cursor.close()

    except mysql.connector.Error as err:
        print("Error:", err)
        print("Failed to create the librarians table. Please try again.")


# Define the library password
library_password="Library123"


# Define the maximum number of incorrect password attempts
max_pw_attempts = 3


# Function to validate librarian password
def validate_librarian_password():
    password_attempts = 0
    
    while password_attempts < max_pw_attempts:
        password = input("Enter the librarian password: ")
        
        if password == library_password:
            return True  # Password is correct, allow access
        else:
            print("Incorrect password. Please try again.")
            password_attempts += 1
    
    print("Too many incorrect password attempts.")
    return False  # Deny access after reaching maximum attempts


# Function to display books in the library
def display_books():

    print("Books in the library:")
    with open("book_details.csv", "r", newline="\r\n") as file:
        books=csv.reader(file)
        next(books)  # Skip the header row
        for book in books:
            print(book[0] + " by " + book[1] + ". Genre: " + book[3] + ". Copies available: " + book[2])


# Function to search for books
def search_books():

    query = input("Enter a search term (title or author): ")
    results = []

    with open("book_details.csv", "r", newline="\r\n") as file:
        books=csv.reader(file)
        next(books)  # Skip the header row

        for book in books:
            if query.lower() in book[0].lower() or query.lower() in book[1].lower():
                results.append(book)
        if results:
            for book in results:
                print(book[0] + " by " + book[1] + ". Genre: " + book[3] + ". Copies available: " + book[2])
        else:
            print("No results found.")


# Function to borrow books and store transactions in MySQL
def borrow_books():

    borrower = input("Enter your name: ")
    borrow_date = input("Enter the borrowing date (YYYY-MM-DD): ")

    while True:
        
        # Continue borrowing books until the user types 'done'
        title = input("Enter the title of the book to borrow (or type 'done' to finish): ")
        if title.lower() == 'done':
            break

        # Check if the user has a reservation for the specified book
        with open("book_reservations.csv", mode='r', newline='') as reservations_file:
            reservations = csv.reader(reservations_file)
            
            for reservation in reservations:
                
                if reservation[0].lower() == title.lower() and reservation[1].lower() == borrower.lower():
                    print("You have a reservation for the book", title + ".")
                    proceed = input("Do you want to borrow it? (yes/no): ")
                    if proceed.lower() != 'yes':
                        break  # Exit the loop if the user chooses not to proceed with the reservation
                    
                    # Remove the reservation since the user is borrowing the book
                    with open("book_reservations.csv", mode='w', newline='') as updated_reservations_file:
                        writer = csv.writer(updated_reservations_file)
                        for r in reservations:
                            if r != reservation:
                                writer.writerow(r)
                    break  # Exit the loop after processing the specified book
        
        # Open the CSV file in read and write mode
        with open("book_details.csv", "r+", newline="\r\n") as file:
            books = list(csv.reader(file))
            found = False  # Flag to track whether the book is found in the library
            
            for book in books:
                
                if book[0].lower() == title.lower():
                    found = True
                    
                    # Check if there are available copies of the book
                    if int(book[2]) > 0:
                        # Decrease the available copies of the book
                        book[2] = str(int(book[2]) - 1)

                        # Connect to the MySQL database for storing transactions
                        mycon = mysql.connector.connect(
                            host="Localhost",
                            user="root",
                            password="",
                            database="library"
                        )
                        
                        cursor = mycon.cursor()

                        # Insert the transaction into the 'transactions' table
                        cursor.execute("INSERT INTO transactions (book_title, borrower_name, borrow_date) VALUES (%s, %s, %s)",
                                       (title, borrower, borrow_date))
                        
                        mycon.commit()
                        cursor.close()

                        print("Book", title, "borrowed successfully.")
                    else:
                        print("Sorry, no available copies of", title, "left.")
                        
                    break  # Exit the loop after processing the specified book

            # If the book is not found in the library, print a message
            if not found:
                print("Sorry, the book", title, "is not available in the library.")

            # Update the CSV file with the new book data outside the for loop
            file.seek(0)
            writer = csv.writer(file)
            writer.writerows(books)  # Writing all books, including the updated one


# Function to display the user's borrowed books
def display_user_borrowed_books():
    
    borrower_name = input("Enter your name: ")
    
    mycon = mysql.connector.connect(
        host="Localhost",
        user="root",
        password="",
        database="library"
    )

    cursor = mycon.cursor()
    cursor.execute("SELECT book_title, borrow_date FROM transactions WHERE borrower_name = %s AND return_date IS NULL", (borrower_name,))
    borrowed_books = cursor.fetchall()

    if cursor.rowcount > 0:
        print("\nYOUR BORROWED BOOKS:")
        print("Book Title | Borrow Date")
        for book in borrowed_books:
            print(book[0] + " | " + str(book[1]))
    else:
        print("You haven't borrowed any books.")

    cursor.close()
    mycon.close()


# Function to suggest books based on genre
def suggest_books_based_on_genre():
    target_genre = input("Enter a genre to get book suggestions: ")
    suggested_books = []

    with open("book_details.csv", "r", newline="\r\n") as file:
        books = csv.reader(file)
        next(books)  # Skip the header row

        for book in books:
            if book[3].lower() == target_genre.lower():
                suggested_books.append(book)

    if suggested_books:
        print("Suggested books in the", target_genre, "genre:")
        for book in suggested_books:
            print(book[0] + " by " + book[1] + ". Copies available: " + book[2])
    else:
        print("No books found in the", target_genre, "genre.")


#Function to generate a report on popular books
def popular_books():
    
    mycon = mysql.connector.connect(
        host="Localhost",
        user="root",
        password="",
        database="library"
    )

    cursor = mycon.cursor()
    cursor.execute("SELECT book_title, COUNT(*) as borrow_count FROM transactions GROUP BY book_title ORDER BY borrow_count DESC")
    popular_books = cursor.fetchall()

    if cursor.rowcount > 0:
        print("\nPopular Books:")
        print("Rank | Book Title | Borrow Count")
        rank = 1
        for book in popular_books[:10]:
            print(str(rank) + ". " + book[0] + " | " + str(book[1]) + " times borrowed")
            rank += 1

    else:
        print("No transaction records found.")

    cursor.close()
    mycon.close()
          

# Function to return books with fine collection
def return_books():
    
    # Collect borrower's name and return date
    borrower = input("Enter the borrower's name: ")
    return_date = input("Enter the returning date (YYYY-MM-DD): ")

    while True:
        
        title = input("Enter the title of the book to return (or type 'done' to finish): ")
        if title.lower() == 'done':
            break

        mycon = mysql.connector.connect(
            host="Localhost",
            user="root",
            password="",
            database="library"
        )
        
        cursor = mycon.cursor()

        # Check if the book is borrowed by the specified borrower and return it
        cursor.execute("SELECT borrow_date FROM transactions WHERE book_title=%s AND borrower_name=%s AND return_date IS NULL",
                       (title, borrower))
        borrow_date_row = cursor.fetchone()

        if borrow_date_row:
            
            # Extract the borrow date from the database result
            borrow_date = borrow_date_row[0]
            
            # Calculate the fine based on the specified conditions
            return_year, return_month, return_day = int(return_date[:4]), int(return_date[5:7]), int(return_date[8:])
            borrow_year, borrow_month, borrow_day = int(borrow_date.year), int(borrow_date.month), int(borrow_date.day)

            fine_days = (return_year - borrow_year) * 365 + (return_month - borrow_month) * 30 + (return_day - borrow_day)
            fine = max(fine_days - 30, 0) * 50  # Calculate the fine (50 rupees per day, after 30 days)

            # Update the transactions table with the return date and fine
            cursor.execute("UPDATE transactions SET return_date=%s, fine=%s WHERE book_title=%s AND borrower_name=%s AND return_date IS NULL",
                           (return_date, fine, title, borrower))
            mycon.commit()

            affected_rows = cursor.rowcount
            
            if affected_rows > 0:

                # Book returned successfully, print a message if there is a fine
                if fine > 0:
                    print("Book", title, "returned successfully. You were late by", fine_days - 30, "day(s) hence you need to pay a fine of", fine, "rupees.")
                else:
                    print("Book", title, "returned successfully.")

                # Update the book details in the CSV file
                with open("book_details.csv", "r+", newline="\r\n") as file:
                    books = list(csv.reader(file))
                    for book in books:
                        if book[0] == title:
                            book[2] = str(int(book[2]) + 1)  # Increase available copies

                    file.seek(0)
                    writer = csv.writer(file)
                    writer.writerows(books)
                    
            else:
                print("Book", title, "has already been returned.")
                
        else:
            # Book not found in the borrowing records
            print("Book", title, "not found in the borrowing records for the specified borrower.")

        cursor.close()
        mycon.close()

#Allows users to reserve a book for future borrowing
def reserve_book():
    
    reserver_name = input("Enter your name: ")
    book_title = input("Enter the title of the book to reserve: ")

    # Check if the book is available
    with open("book_details.csv", mode='r+', newline='') as details_file:
        
        details = csv.reader(details_file)
        next(details)  # Skip header
        
        for book in details:
            
            if book[0] == book_title and int(book[2]) > 0:
                
                # Reserve the book
                with open("book_reservations.csv", mode='a', newline='') as reservations_file:
                    reservations_file.seek(0)
                    writer = csv.writer(reservations_file)
                    writer.writerow([book_title, reserver_name])

                # Update available copies in book_details.csv
                book[2] = str(int(book[2]) - 1)
                details_file.seek(0)
                writer = csv.writer(details_file)
                writer.writerows(details)
                
                print("The book", book_title, "has been reserved for", reserver_name + ".")
                return

        else:
            print("Sorry, the book", book_title, "is not available for reservation.")

                
#Displays the list of books reserved by users
def display_reserved_books():
    
    with open("book_reservations.csv", mode='r', newline='') as file:
        reservations = csv.reader(file)
        print("\nReserved Books:")
        for reservation in reservations:
            print(reservation[0], "reserved by", reservation[1])


#Function to update book details
def update_book_details():
    
    title = input("Enter the title of the book to update: ")
    
    with open("book_details.csv", "r+", newline="\r\n") as file:
        books = list(csv.reader(file))
        for book in books:
            
            if book[0] == title:
                new_copies = int(input("Enter the new number of copies available: "))
                book[2] = str(new_copies)
                print("Book details updated successfully.")
                break
            
        else:
            print("Book not found in the library.")
            return
        
        # Update the CSV file with the new book data
        file.seek(0)
        writer = csv.writer(file)
        writer.writerows(books)  # Writing all books, including the updated one


# Function to display transactions history
def display_transactions_history():
    
    mycon = mysql.connector.connect(
        host="Localhost",
        user="root",
        password="",
        database="library"
    )

    cursor = mycon.cursor()
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()

    if cursor.rowcount > 0:
        print("\nTRANSACTIONS HISTORY")
        print("Book Title | Borrower Name | Borrow Date | Return Date | Fine")
        for transaction in transactions:
            print(transaction[0], "|", transaction[1], "|", transaction[2], "|", transaction[3], "|", transaction[4])
    else:
        print("No transactions found.")

    cursor.close()
    mycon.close()


# Function to calculate and display total fine collected
def display_total_fine_collected():
    
    mycon = mysql.connector.connect(
        host="Localhost",
        user="root",
        password="",
        database="library"
    )

    cursor = mycon.cursor()
    cursor.execute("SELECT SUM(fine) FROM transactions")
    total_fine = cursor.fetchone()[0]

    if total_fine:
        print("\nTotal Fine Collected:", total_fine, "rupees")
    else:
        print("No fine collected.")

    cursor.close()
    mycon.close()


# Function to add a librarian
def add_librarian():

    try:
        mycon=mysql.connector.connect(
            host="Localhost",
            user="root",
            password="",
            database="library"
        )

        name = input("Enter the librarian's name:")
        Age=int(input("Enter age:"))
        Phone_no=int(input("Enter phone no:"))
        Sex=input("Enter gender(M/F):")
        cursor=mycon.cursor()
        cursor.execute("INSERT INTO librarians (name, Age, Phone_no, Sex) VALUES (%s, %s, %s, %s)",(name, Age, Phone_no, Sex,))

        mycon.commit()
        cursor.close()
        
        print("Librarian", name, "has been added.")

    except mysql.connector.Error as err:
        print("Error:", err)
        print("Failed to add librarian. Please try again.")

    finally:
        mycon.close()


#Function to delete a librarian
def remove_librarian():

    try:
        
        mycon = mysql.connector.connect(
            host="Localhost",
            user="root",
            password="",
            database="library"
        )
        
        cursor=mycon.cursor()

        name = input("Enter the librarian's name:")
        # Use the DELETE statement to delete the librarian
        cursor.execute("DELETE FROM librarians WHERE name = %s",(name,))
        mycon.commit()

        if cursor.rowcount > 0:
            print("Librarian, " ,name, "has been removed.")
        else:
            print("No librarian with the name" ,name, "found.")
            
        cursor.close()
        mycon.close()

    except mysql.connector.Error as err:
        print("Error:", err)
        print("Failed to remove librarian. Please try again.")

    finally:
        mycon.close()


# Function to show librarians
def show_librarians():

    try:
        mycon=mysql.connector.connect(
            host="Localhost",
            user="root",
            password="",
            database="library"
        )

        cursor=mycon.cursor()
        cursor.execute("SELECT * FROM librarians")
        data = cursor.fetchall()

        if cursor.rowcount > 0:
            print("\nLibrarians:")
            for librarian in data:
                print("Name: " + str(librarian[0]) + ", Age: " + str(librarian[1]) + ", Phone No: " + str(librarian[2]) + ", Gender: " + str(librarian[3]))
        else:
            print("No librarian found.")

        cursor.close()
        mycon.close()

    except mysql.connector.Error as err:
        print("Error:", err)
        print("Failed to show librarian. Please try again.")

    finally:
        mycon.close()


# Function to add a book
def add_book():

    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    copies = int(input("Enter the number of copies available: "))
    genre = input("Enter the genre of the book: ")

    with open("book_details.csv", "r+", newline="\r\n") as file:
        books = list(csv.reader(file))
        books.append([title, author, copies, genre])
        print("Book", title, "by", author, "has been added with", copies, "copies.")

        # Update the CSV file with the new book data
        file.seek(0)
        writer = csv.writer(file)
        writer.writerows(books)  # Writing all books, including the updated one


# Function to remove a book
def remove_book():

    title = input("Enter the title of the book to remove: ")
    with open("book_details.csv", "r+", newline="\r\n") as file:
        books = list(csv.reader(file))
        
        # Find and remove the book from the list
        for book in books:
            if book[0] == title:
                books.remove(book)
                print("Book", title, "has been removed.")
                break
        else:
            print("Book not found in the library.")
            return

        # Update the CSV file with the new book data
        file.seek(0)
        writer = csv.writer(file)
        writer.writerows(books)  # Writing all books, including the updated one


# Function to display the librarian menu
def librarian_menu():

    while True:

        print("\nLIBRARIAN MENU")
        print("1. Add Librarian")
        print("2. Show Librarians")
        print("3. Remove Librarian")
        print("4. Add Book")
        print("5. Delete Book")
        print("6. Update Book")
        print("7. Display Transactions History")
        print("8. Display Total Fine Collected")
        print("9. Display Reserved Books")
        print("10. Quit")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_librarian()

        elif choice == 2:
            show_librarians()

        elif choice == 3:
            remove_librarian()

        elif choice == 4:
            add_book()

        elif choice == 5:
            remove_book()

        elif choice == 6:
            update_book_details()

        elif choice == 7:
            display_transactions_history()

        elif choice == 8:
            display_total_fine_collected()

        elif choice == 9:
            display_reserved_books()

        elif choice == 10:
            break

        else:
            print("Invalid choice. Please try again.")


# Function to display the user menu
def user_menu():
    
    while True:
        
        print("\nUSER MENU")
        print("1. Display Books")
        print("2. Borrow Book")
        print("3. Reserve Book")
        print("4. Return Book")
        print("5. Search Book")
        print("6. Display Popular Books")
        print("7. Display Borrowed Books")
        print("8. Suggest Books by Genre")
        print("9. Quit")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            display_books()

        elif choice == 2:
            borrow_books()

        elif choice == 3:
            reserve_book()

        elif choice == 4:
            return_books()

        elif choice == 5:
            search_books()

        elif choice == 6:
            popular_books()

        elif choice == 7:
            display_user_borrowed_books()

        elif choice == 8:
            suggest_books_based_on_genre()

        elif choice == 9:
            break

        else:
            print("Invalid choice. Please try again.")


# Start the user menu
def library_management_system():

    create_database()
    create_transactions_table()
    create_librarians_table()
    
    print("------WELCOME TO THE LIBRARY------")

    while True:
        print("1. User Menu")
        print("2. Librarian Menu")
        print("3. Exit")
        ch = int(input("Enter your choice: "))

        if ch == 1:
            user_menu()

        elif ch == 2:
            # Validate librarian password before entering the librarian menu
            if validate_librarian_password():
                librarian_menu()
            else:
                print("Access denied. Returning to the main menu.")

        elif ch == 3:
            break

        else:
            print("Invalid choice. Please try again.")

library_management_system()
