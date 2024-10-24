from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pedidos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productos = db.Column(db.String(255), nullable=False)  # Lista de productos en formato JSON o similar
    cantidad = db.Column(db.String(255), nullable=False)  # Cantidades de cada producto
    estado = db.Column(db.String(50), default='pendiente')  # Estado del pedido
    fecha_compra = db.Column(db.String(50), nullable=False)  # Fecha de compra
