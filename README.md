
# Yetti Authentication

A detailed authentication app with test cases


## Run Locally

Clone the project

```bash
  git clone https://github.com/Theresa-o/yettiauth.git
```

Go to the project directory

```bash
  cd proauth
```

Create a Virtual Environment 

```bash
  python -m venv venv
source venv/bin/activate OR venv\Scripts\activate  Windows
```
Install Dependencies

```bash
  pip install -r requirements.txt
```

Apply Migrations

```bash
  python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```

Access the Page

Open your web browser and navigate to http://localhost:8000/



## Features

### Authentication System Details
- The authentication system includes the following components:

- User Registration: You can access the registration page at http://localhost:8000/register/.

- User Login: You can access the login page at http://localhost:8000/login/.

- User Logout: To log out, visit http://localhost:8000/logout/.

- Secured Page: The "Hello World" page at http://localhost:8000/hello/ is only accessible to authenticated users. Unauthorized users will be redirected to the login page.

### Testing Details
The tests cover the following scenarios:

- User Registration: Tests validate that user registration works correctly, including input data validation and user account creation.

- User Login and Logout: Tests ensure that users can successfully log in and out.

- Access Control: Tests confirm that only authenticated users can access secured views, and unauthorized users are redirected to the login page.

- Error Handling: Tests cover cases such as incorrect passwords, non-existent users, and other error scenarios to ensure the authentication system handles them gracefully.

- Security Testing: The tests include security checks for potential vulnerabilities like session fixation and CSRF attacks.


## Running Tests

To run tests, run the following command

```bash
  python manage.py test
```
