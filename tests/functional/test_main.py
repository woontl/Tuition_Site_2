def test_main_home_page(test_client):

    response = test_client.get('/home')
    assert response.status_code == 200
    assert b"Dashboard" in response.data
    assert b"Latest Homework" in response.data
    assert b"Latest Class Notes" in response.data
    assert b"Activities" in response.data
    assert b"Home" in response.data
    assert b"Login" in response.data
    assert b"Register" in response.data
    
def test_main_about_page(test_client):

    response = test_client.get('/about')
    assert response.status_code == 200
    assert b"About" in response.data