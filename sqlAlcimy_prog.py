from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)

#create a db and connect to the sqlitAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_contacts.sqlite3'
app.config['SECRET_KEY'] = "random string"
 
db = SQLAlchemy(app)
 
# my model (create a table)
class Contact(db.Model):
    id = db.Column('contact_id', db.Integer, primary_key = True)
    name = db.Column(db.String(15))
 
    def __init__(self, name):
        self.name = name

@app.route("/")
def home():
    return '<h1>please type your request in the URL'

@app.route("/data/<ind>")
@app.route("/data/")
def contacts(ind =-1):
    # one contact with the match query
    if int(ind) > -1:
        contact=Contact.query.get(int(ind))
        return {"name":contact.name,"id":contact.id}   
    
    # all contact with the match query
    res=[]
    for contact in Contact.query.all():
        res.append({"name":contact.name,"id":contact.id})
    return res
 
#add contact with the match query
@app.route("/add/", methods=['POST'])
def add_student():
    request_data = request.get_json()
    name= request_data["name"]
 
    newContact= Contact(name)
    db.session.add (newContact)
    db.session.commit()
    return "a new rcord was create"
 
#delete cintact with the match query
@app.route("/del/<ind>", methods=['DELETE'])
def del_student(ind=-1):
        contact=Contact.query.get(int(ind))
        if contact:
            db.session.delete(contact)
            db.session.commit()
            return f"student del {contact.name}"
        return f"no such student"
 
#update contact with the match query
@app.route("/upd/<ind>", methods=['PUT'])
def upd_student(ind=-1):
    if int(ind) > -1:
        data = request.json
        uname = (data["name"])
        contact=Contact.query.get(int(ind))
        if contact:
            contact.name=uname
            db.session.commit()
            return "student update"
        return "or karzia"

#End- the comment with gives the option to open the db & table
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
 
