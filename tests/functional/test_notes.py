def test_notes_notes_all_page(test_client):

    response = test_client.get('/notes_all/ALL')
    assert response.status_code == 200
    assert b"Lesson Notes" in response.data
    assert b"New Note" in response.data
    
def test_notes_new_note_page(test_client):

    response = test_client.get('/notes/new')
    assert response.status_code == 200
    assert b"New Note" in response.data
    assert b"Title" in response.data
    assert b"Student" in response.data
    assert b"Post" in response.data