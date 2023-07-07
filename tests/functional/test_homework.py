def test_homework_my_homework_page(test_client):

    response = test_client.get('/my_homework/ALL')
    assert response.status_code == 200
    assert b"All Homework" in response.data

def test_homework_new_homework_page(test_client):

    response = test_client.get('/homework/new')
    assert response.status_code == 200
    assert b"New Homework" in response.data
    assert b"Title" in response.data
    assert b"Student" in response.data
    assert b"Deadline" in response.data
    assert b"Post" in response.data
    
def test_homework_questionbank_page(test_client):

    response = test_client.get('/questionbank/ALL/ALL/ALL')
    assert response.status_code == 200
    assert b"Questionbank" in response.data
    assert b"Filters" in response.data
    assert b"Grade" in response.data
    assert b"Tags" in response.data
    assert b"Difficulty" in response.data
    assert b"Load Question" in response.data
    
def test_homework_upload_questionbank_page(test_client):

    response = test_client.get('/upload_questionbank')
    assert response.status_code == 200
    assert b"New Upload" in response.data
    assert b"Click to Upload Question Image" in response.data
    assert b"Grade" in response.data
    assert b"Tags" in response.data
    assert b"Difficulty" in response.data
    assert b"Answer" in response.data
    assert b"Part A:" in response.data
    assert b"Upload" in response.data
    
    