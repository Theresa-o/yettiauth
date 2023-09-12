from django.test import TestCase
from django.urls import reverse
from yettiuserauth.models import User
from django.middleware.csrf import get_token

class RegistrationTestCase(TestCase):
    def test_valid_registration(self):
        # Simulate a valid registration POST request
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirmation': 'password123'
        })
        
        # Check that the response redirects to the index page (successful registration)
        self.assertRedirects(response, reverse('index'))
        
        # Check that the user was created in the database
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_password_mismatch(self):
        # Simulate a registration with mismatched passwords
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirmation': 'differentpassword'
        })
        
        # Check that the response does not redirect (passwords mismatch)
        self.assertTemplateUsed(response, 'yettiuserauth/register.html')
        
        # Check that no user was created in the database
        self.assertFalse(User.objects.filter(username='newuser').exists())
    
    def test_duplicate_username(self):
        # Create a user with the same username in the database
        User.objects.create_user(username='existinguser', password='password123')
        
        # Simulate a registration with a duplicate username
        response = self.client.post(reverse('register'), {
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirmation': 'password123'
        })
        
        # Check that the response does not redirect (username already taken)
        self.assertTemplateUsed(response, 'yettiuserauth/register.html')
        
        # Check that no new user was created in the database
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())

class LoginLogoutTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_valid_login(self):
        # Simulate a valid login POST request
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })
        
        # Check that the response redirects to the index page (successful login)
        self.assertRedirects(response, reverse('index'))
        
        # Check that the user is authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_invalid_login(self):
        # Simulate an invalid login with incorrect password
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'incorrectpassword',
        })
        
        # Check that the response does not redirect (invalid login)
        self.assertTemplateUsed(response, 'yettiuserauth/login.html')
        
        # Check that the user is not authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_invalid_login_nonexistent_user(self):
            # Simulate an invalid login with a non-existent user
            response = self.client.post(reverse('login'), {
                'username': 'nonexistentuser',
                'password': 'testpassword',
            })
            
            # Check that the response does not redirect (invalid login)
            self.assertTemplateUsed(response, 'yettiuserauth/login.html')
            
            # Check that the user is not authenticated
            self.assertFalse(response.wsgi_request.user.is_authenticated)
            
            # Check that the response contains an error message
            self.assertContains(response, "Invalid username and/or password.")
    
    def test_logout(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        
        # Simulate a logout POST request
        response = self.client.post(reverse('logout'))
        
        # Check that the response redirects to the index page (successful logout)
        self.assertRedirects(response, reverse('index'))
        
        # Check that the user is not authenticated after logout
        self.assertFalse(response.wsgi_request.user.is_authenticated)

class TaskManagementViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
    
    def test_authenticated_access(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        
        # Simulate accessing the protected view
        response = self.client.get(reverse('index'))
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
    
    def test_unauthorized_access(self):
        # Simulate accessing the protected view without logging in
        response = self.client.get(reverse('index'))
        
        # Check that the response status code is 302 (redirect to login page)
        self.assertEqual(response.status_code, 302)
        
        # Check that the user is redirected to the login page
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('index'))

class SecurityTestCase(TestCase):
    def test_session_fixation_attack(self):
        # Create a user
        user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        
        # Store the session ID
        original_session_id = self.client.session.session_key
        
        # Log out the user
        self.client.logout()
        
        # Verify that the session ID changes after logout
        self.client.login(username='testuser', password='testpassword')
        new_session_id = self.client.session.session_key
        
        # Check that the session ID has changed
        self.assertNotEqual(original_session_id, new_session_id)

class SecurityTestCase(TestCase):
    def test_csrf_attack(self):
        # Simulate a GET request to a view that requires CSRF protection
        response = self.client.get(reverse('some_protected_view'))
        
        # Extract the CSRF token from the response content
        csrf_token = get_token(response.wsgi_request)
        
        # Simulate a malicious POST request without including the CSRF token
        malicious_response = self.client.post(reverse('some_protected_view'), {
            'malicious_data': 'value',
        }, HTTP_REFERER=reverse('some_protected_view'))
        
        # Check that the malicious POST request is denied with a 403 Forbidden status
        self.assertEqual(malicious_response.status_code, 403)

