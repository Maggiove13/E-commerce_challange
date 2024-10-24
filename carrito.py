from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carrito.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Carritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable= False)
    producto_id = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    fecha_agregado = db.Column(db.DateTime, default=func.now())


@app.route('/carrito', methods=['POST'])
def agregar_al_carrito():
    data = request.get_json()
    nuevo_item = Carritos(
        user_id = data['user_id'],
        producto_id = data['producto_id'],
        cantidad = data.get('cantidad', 1)
    )
    
    print(nuevo_item)
    
    db.session.add(nuevo_item)
    db.session.commit()
    return jsonify({'user_id': nuevo_item.user_id, 
                    'id': nuevo_item.id, 
                    'producto_id': nuevo_item.producto_id,
                    'cantidad': nuevo_item.cantidad}), 201



@app.route('/carrito/<int:user_id>', methods=['GET'])
def listar_carrito(user_id):
    items = Carritos.query.filter_by(user_id = user_id).all()
    
    return jsonify([{'id': item.id, 
                    'producto_id': item.producto_id, 
                    'cantidad': item.cantidad} for item in items]), 200



@app.route('/carrito/<int:user_id>/<int:producto_id>', methods=['PUT'])
def modificar_item(user_id, producto_id):
    data = request.get_json()
    item = Carritos.query.filter_by(user_id = user_id, producto_id = producto_id).first_or_404()
    
    item.user_id = data['user_id']
    item.producto_id = data ['producto_id']
    
    if 'cantidad' in data:
        item.cantidad = data['cantidad']
        
    db.session.commit()
    
    return jsonify({
        'user_id': item.user_id,
        'id': item.id, 
        'producto_id': item.producto_id, 
        'cantidad': item.cantidad}), 200
    


@app.route('//carrito/<int:user_id>/<int:producto_id>', methods=['DELETE'])
def eliminar_item(user_id, producto_id):
    item = Carritos.query.filter_by(user_id = user_id, producto_id = producto_id).first_or_404()

    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'message': f'Item product_id: {producto_id} eliminado de tu carrito'}), 200


@app.route('/carrito/<int:user_id>/finalizar_compra', methods=['POST'])
def finalizar_compra(user_id):
    
    items = Carritos.query.filter_by(user_id=user_id).all()
    
    if not items:
        return jsonify({"error": "El carrito está vacío"}), 400
    
    # Preparar los datos para el pedido
    productos = []
    cantidades = []
    
    for item in items:
        productos.append(item.producto_id)
        cantidades.append(item.cantidad)
    
    
    productos_json = ', '.join(map(str, productos))
    cantidades_json = ', '.join(map(str, cantidades))
    
    
    pedido_data = {
        "productos": productos_json,
        "cantidad": cantidades_json,
        "fecha_compra": datetime.now().isoformat()  
    }
    
    # Enviar la solicitud POST al microservicio de pedidos
    response = requests.post('http://localhost:5003/pedidos', json=pedido_data)
    
    if response.status_code == 201:
        
        for item in items:
            db.session.delete(item)
        db.session.commit()
        
        return jsonify({"message": "Compra finalizada con éxito", "pedido": response.json()}), 201
    else:
        return jsonify({"error": "Error al crear el pedido", "details": response.json()}), response.status_code


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5002)