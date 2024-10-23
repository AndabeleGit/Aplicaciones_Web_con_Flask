from flask import Flask, request, jsonify # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
db = SQLAlchemy(app)

# Crear modelo de la app

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(10), nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email':self.email,
            'phone':self.phone
        }

with app.app_context():
    db.create_all()

# Creacion de rutas 

@app.route('/contacts', methods = ['GET'])
def get_contacts(): 
    contacts = Contact.query.all()
    return jsonify({'contacts': [contact.serialize() for contact in contacts]})

@app.route('/contacts', methods = ['POST'])
def create_contacts():
    data = request.get_json()
    contact = Contact(name = data['name'], email = data['email'], phone = data['phone'])
    db.session.add(contact)
    db.session.commit()
    return jsonify({'mensaje':'Contacto creado con exito', 'contact': contact.serialize()})

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get(id) 
    if contact is None:
        return jsonify({'mensaje': 'Contacto no encontrado'}), 404 
    return jsonify(contact.serialize())

@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get_or_404(id) 

    data = request.get_json()
    
    if 'name' in data:
        contact.name = data['name']
    if 'email' in data:
        contact.email = data['email']
    if 'phone' in data:
        contact.phone = data['phone']

    db.session.commit()

    return jsonify({'mensaje': 'Contacto actualizado con éxito', 'contact': contact.serialize()}), 201

@app.route('/contacts/<int:id>', methods = ['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)  
    if contact is None:
        return jsonify({'mensaje': 'Contacto no encontrado'}), 404 
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'mensaje': 'Contacto borrado con éxito', 'contact': contact.serialize()})