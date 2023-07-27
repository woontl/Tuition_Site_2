import pytest
from flaskblog import create_app
from flaskblog.models import User, Homework, Questionbank, Question, Working, Activity

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

@pytest.fixture(scope='module')
def new_user():
    user = User(username='Bob', email='Bob@test.com', password='123', image_file='default.jpg', account_type='user', grade='10')
    return user

@pytest.fixture(scope='module')
def new_homework():
    homework = Homework(title='HW_title', student_id='1', deadline='1/1/11') 
    return homework

@pytest.fixture(scope='module')
def new_questionbank():
    questionbank = Questionbank(img='imgXX', grade='10', topics='topic1', difficulty='Hard', answer='answer1',) 
    return questionbank

@pytest.fixture(scope='module')
def new_question():
    question = Question(title='title1', homework_id='1', questionbank_id='1', grade='10', topics='topic1', difficulty='Hard', qn_img='img1', qn_answer='answer1') 
    return question

@pytest.fixture(scope='module')
def new_working():
    working = Working(homework_id='1', question_id='1', workings='working1', final_ans='ans1', point='1', right_wrong='0;0;0') 
    return working

@pytest.fixture(scope='module')
def new_activity():
    activity = Activity(description='desc1', student_id='1') 
    return activity