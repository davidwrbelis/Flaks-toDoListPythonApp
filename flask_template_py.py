from flask import Flask, render_template
# import Flask-Scss
#import SQLAlchemy


#global contents
app = Flask(__name__)    #creat Flask application.   app is our container object
print('app name -', app) #app name - <Flask 'flasktutorial'>

@app.route('/') #in order to create a route to our home page we need to use a Flask decorator.  This points to our index.html page
def index(): #create a route to the index.html page
    return render_template('index.html')

if __name__ in "__main__":
    app.run()  #run object created by app = Flask(__name__) 