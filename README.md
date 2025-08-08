Technologies Used:
Flask: Handles the web server, routing, and rendering web pages.
PyMongo: Connects and interacts with your MongoDB database.
Werkzeug Security: Hashes passwords securely before storing, and checks hashed passwords during login.

How Data is Stored:
When a user signs up (/signup route):
Your app takes the username and password from the form.
Checks if the username already exists in the MongoDB users collection.
If not, hashes the password securely using generate_password_hash().
Inserts a new document into the users collection with:
{
  "username": "<user_input>",
  "password": "<hashed_password>"
}
Redirects the user to the login page.

When a user logs in (/login route):
The app fetches the user document by username from MongoDB.
Uses check_password_hash() to compare the stored hash and the entered password.
If valid, stores the username in Flask's session to keep the user logged in.

How to Verify Data in MongoDB:
To view the stored user data in your MongoDB database, open a terminal and run:
mongosh
Then run these commands inside the Mongo shell:
use contactDB            # Switch to your app’s database

show collections        # Should show 'users' collection

db.users.find().pretty() # View all user documents with usernames and hashed passwords

<img width="1169" height="607" alt="Screenshot 2025-08-08 at 3 40 44 PM" src="https://github.com/user-attachments/assets/46a627f3-539e-4df7-ac4c-42902bd9fcbf" />



