
def test_users_register_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b"Join Today" in response.data
    assert b"Username" in response.data
    assert b"Email" in response.data
    assert b"Grade" in response.data
    assert b"Password" in response.data
    assert b"Confirm Password" in response.data
    assert b"Account Type" in response.data
    assert b"Sign Up" in response.data
    assert b"Already have An Account?" in response.data
    assert b"Sign In" in response.data
    
def test_users_login_page(test_client):
    
    response = test_client.get('/login')
    assert response.status_code == 200
    # assert b"Please log in to access this page." in response.data
    assert b"Log In" in response.data
    assert b"Password" in response.data
    assert b"Remember Me" in response.data
    assert b"Login" in response.data
    assert b"Forgot Password?" in response.data
    assert b"Need An Account?" in response.data
    assert b"Sign Up Now" in response.data
    
def test_users_reset_password_page(test_client):
    
    response = test_client.get('/reset_password')
    assert response.status_code == 200
    assert b"Reset Password" in response.data
    assert b"Email" in response.data
    assert b"Request Password Reset" in response.data
    
def test_users_admin_page(test_client):
    
    response = test_client.get('/admin')
    assert response.status_code == 200
    assert b"Admin Panel" in response.data
    assert b"Username" in response.data
    assert b"Email" in response.data
    assert b"Account Type" in response.data
    assert b"Action" in response.data
    
def test_users_account_page(test_client):
    
    response = test_client.get('/account')
    assert response.status_code == 200
    assert b"Account Info" in response.data
    assert b"Username" in response.data
    assert b"Email" in response.data
    assert b"Grade" in response.data
    assert b"Update Profile Picture" in response.data
    assert b"Update" in response.data
    
def test_users_resetpassword_page(test_client):
    
    response = test_client.get('/reset_password')
    assert response.status_code == 200
    assert b"Reset Password" in response.data
    assert b"Email" in response.data
    assert b"Request Password Reset" in response.data
