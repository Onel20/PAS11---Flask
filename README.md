# Flask Encyclopedia Web Application

A web-based encyclopedia platform built with Flask that allows users to create, read, and interact with articles on various subjects.

## Features

- **User Authentication**
  - User registration and login
  - Secure password hashing
  - Password change functionality

- **Article Management**
  - Create and publish articles
  - Edit existing articles
  - View articles with author information
  - Browse articles by subject

- **Comments System**
  - Add comments to articles
  - Edit your own comments
  - View all comments on articles

- **Responsive Design**
  - Modern Bootstrap 5 interface
  - Mobile-friendly layout
  - Clean and intuitive navigation

## Prerequisites

Before running this application, make sure you have:

- Python 3.8 or higher
- MySQL Server 8.0 or higher
- Git (for cloning the repository)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Onel20/PAS11---Flask.git
   cd PAS11---Flask
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     venv/Scripts/activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the MySQL database:
   ```sql
   CREATE DATABASE ensiklopedia;
   USE ensiklopedia;

   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(255) NOT NULL UNIQUE,
       password VARCHAR(255) NOT NULL
   );

   CREATE TABLE articles (
       id INT AUTO_INCREMENT PRIMARY KEY,
       title VARCHAR(255) NOT NULL,
       content TEXT NOT NULL,
       subject VARCHAR(255) NOT NULL,
       author_id INT NOT NULL,
       FOREIGN KEY (author_id) REFERENCES users(id)
   );

   CREATE TABLE comments (
       id INT AUTO_INCREMENT PRIMARY KEY,
       article_id INT NOT NULL,
       user_id INT NOT NULL,
       comment_text TEXT NOT NULL,
       FOREIGN KEY (article_id) REFERENCES articles(id),
       FOREIGN KEY (user_id) REFERENCES users(id)
   );
   ```

## Configuration

1. Update the database configuration in `app/models/user_model.py`, `article_model.py`, and `comment_model.py`:
   ```python
   self.conn = mysql.connector.connect(
       host="localhost",
       database="ensiklopedia",
       user="your_username",
       password="your_password"
   )
   ```

## Running the Application

1. Start the Flask application:
   ```bash
   python run.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Registration and Login**
   - Click "Register" to create a new account
   - Use your credentials to log in

2. **Creating Articles**
   - Click "New Article" in the navigation bar
   - Fill in the title, subject, and content
   - Click "Create Article" to publish

3. **Interacting with Articles**
   - Browse articles from the home page
   - Click on an article to read it
   - Add comments if you're logged in
   - Edit your own articles and comments

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

For any queries or support, please open an issue on GitHub.
