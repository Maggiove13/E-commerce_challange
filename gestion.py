from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(255))
    categoria = db.Column(db.String(50))

@app.route('/productos', methods=['POST'])
def agregar_producto():
    data = request.get_json()
    nuevo_producto = Producto(
        nombre=data['nombre'],
        precio=data['precio'],
        descripcion=data.get('descripcion', ''),
        categoria=data.get('categoria', '')
    )
    
    db.session.add(nuevo_producto)
    db.session.commit()
    
    return jsonify({'id': nuevo_producto.id, 'nombre': nuevo_producto.nombre}), 201



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001)