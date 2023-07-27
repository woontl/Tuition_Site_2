    
def test_DB_new_user(new_user):
    """
    GIVEN a user model
    WHEN a new user is created
    THEN check the fields are defined correctly
    """
    assert new_user.username == 'Bob'
    assert new_user.email == 'Bob@test.com'
    assert new_user.password == '123'
    assert new_user.image_file == 'default.jpg'
    assert new_user.account_type == 'user'
    assert new_user.grade =='10'
    
def test_DB_new_homework(new_homework):
    """
    GIVEN a homework model
    WHEN a new homework is created
    THEN check the fields are defined correctly
    """
    assert new_homework.title == 'HW_title'
    assert new_homework.student_id == '1'
    assert new_homework.deadline== '1/1/11'

def test_DB_new_questionbank(new_questionbank):
    """
    GIVEN a questionbank model
    WHEN a new questionbank is created
    THEN check the fields are defined correctly
    """
    assert new_questionbank.img == 'imgXX'
    assert new_questionbank.grade == '10'
    assert new_questionbank.topics == 'topic1'
    assert new_questionbank.difficulty == 'Hard'
    assert new_questionbank.answer == 'answer1'
    
def test_DB_new_question(new_question):
    """
    GIVEN a question model
    WHEN a new question is created
    THEN check the fields are defined correctly
    """
    assert new_question.title == 'title1'
    assert new_question.homework_id == '1'
    assert new_question.questionbank_id == '1'
    assert new_question.grade == '10'
    assert new_question.topics == 'topic1'
    assert new_question.difficulty == 'Hard'
    assert new_question.qn_img == 'img1'
    assert new_question.qn_answer == 'answer1'
    
def test_DB_new_working(new_working):
    """
    GIVEN a working model
    WHEN a new working is created
    THEN check the fields are defined correctly
    """
    assert new_working.homework_id == '1'
    assert new_working.question_id == '1'
    assert new_working.workings == 'working1'
    assert new_working.final_ans == 'ans1'
    assert new_working.point == '1'
    assert new_working.right_wrong == '0;0;0'

def test_DB_new_activity(new_activity):
    """
    GIVEN a activity model
    WHEN a new activity is created
    THEN check the fields are defined correctly
    """
    assert new_activity.description == 'desc1'
    assert new_activity.student_id == '1'