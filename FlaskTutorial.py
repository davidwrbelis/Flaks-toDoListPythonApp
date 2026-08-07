from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



#global contents########################################
app = Flask(__name__)    #creat Flask application.   app is our container object
print('app name -', app);print() #app name - <Flask 'flasktutorial'>




###SQLAlchemy###########################################
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///to_do_list.db"
db = SQLAlchemy(app) #pass in URI of the database

class DB_tasks(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    content     = db.Column(db.String(100), nullable=False)
    completed   = db.Column(db.Integer, default=0)
    do_on       = db.Column(db.String(50))
    created     = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr_(self) -> str :
        return f"Task {self.id}"




###@app.route index()###########################################
@app.route('/', methods=["POST", "GET"]) #in order to create a route to our home page we need to use a Flask decorator.  This points to our index.html page
def index(): #create a route to the index.html page #route will recieve both FORM POST an GET's

    print('inside index()');print()
    #add a task
    if request.method == "POST":
        
        print(); print('request.method == POST'); print()
        
        #contains the content (id or name attribute??) of the input box in the HTML form
        current_task = request.form['content'] 
        
        print(); print(current_task); print()
        new_task = DB_tasks(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            #refresh the homepage after the record is committed.
            return redirect("/")
        except Exception as e:
            print(f"ERROR - {e}")
            return f"ERROR - {e}"
    #see all tasks
    else:
        #if not adding a tasks then query the database result set of current tasks
        #this will occur when the page first opens has no requests have been raised
        tasks = DB_tasks.query.order_by(DB_tasks.created).all()
        print('leaving index()');print()
        return render_template('index.html', tasks=tasks) #because the @app.route opens this page the return can be a string which would output to a browser



###@app.route delete()###########################################
@app.route('/delete/<id>') #in order to create a route to our home page we need to use a Flask decorator.  This points to our index.html page
def delete(id):
    
    delete_task = DB_tasks.query.get_or_404(id)
    
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"ERROR - {e}")
        return f"ERROR - {e}"
    
 
    
###@app.route update()###########################################   
@app.route('/update/<id>', methods=["POST", "GET"]) #in order to create a route to our home page we need to use a Flask decorator.  This points to our index.html page
def update(id):
    update_task = DB_tasks.query.get_or_404(id)
    if request.method == "POST":
        print(); print('update() POST found'); print()
        
        update_task.content  = request.form['content']
       
        try:       #How does this know to update and not Insert.  All we have 
                   #all we have is a commit action.  
            # db.session.update(update_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR - {e}")
            return f"ERROR - {e}"  
    else: 
        print(); print('render update page'); print()
        return render_template('update.html', tasks=update_task)
  
      
    
##EXECUTION SECTION################################################
if __name__ in "__main__":
    
    # with app.app_context() :
    #     db.create_all()
    print('app_run() - execute the script');print()
    app.run()  #run object created by app = Flask(__name__) 
    








