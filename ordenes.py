from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pedidos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Lista de productos en formato JSON o similar
    productos = db.Column(db.String(255), nullable=False)
    # Cantidades de cada producto
    cantidad = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(50), default='pendiente')  # Estado del pedido
    fecha_compra = db.Column(db.String(50), nullable=False)  # Fecha de compra


@app.route('/pedidos', methods=['POST'])
def crear_pedido():
    data = request.get_json()
    nuevo_pedido = Pedido(
        productos=data['productos'],
        cantidad=data['cantidad'],
        estado=data.get('estado', 'pendiente'),
        fecha_compra=data['fecha_compra']
    )

    db.session.add(nuevo_pedido)
    db.session.commit()
    return jsonify({'id': nuevo_pedido.id, 'estado': nuevo_pedido.estado}), 201


@app.route('/pedidos', methods=['GET'])
def listar_pedidos():
    pedidos = Pedido.query.all()
    return jsonify([{'id': p.id, 'productos': p.productos, 'cantidad': p.cantidad, 'estado': p.estado, 'fecha_compra': p.fecha_compra} for p in pedidos]), 200


@app.route('/pedidos/<int:id>', methods=['PUT'])
def actualizar_pedido(id):
    data = request.get_json()
    pedido = Pedido.query.get_or_404(id)
    pedido.estado = data.get('estado', pedido.estado)
    db.session.commit()
    return jsonify({'id': pedido.id, 'estado': pedido.estado}), 200


@app.route('/pedidos/<int:id>', methods=['DELETE'])
def eliminar_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    db.session.delete(pedido)
    db.session.commit()
    return jsonify({'message': f'Item {id} eliminado del carrito'}), 200
