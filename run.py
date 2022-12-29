from flaskblog import create_app

app = create_app()

if __name__ == '__main__': #runs app in debug mode when u run this python script
    app.run(debug=True)

# to run app via terminal, type in terminal:
# export FLASK_APP=Flask_Blog.py
# flask run