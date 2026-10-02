def crear_cliente(client):
    return client.post(
        "/api/clientes",
        json={"nombre": "Ana", "correo": "ana@example.com"},
    ).json


def crear_producto(client):
    return client.post(
        "/api/productos",
        json={"nombre": "Mouse", "precio": 125.50, "stock": 10, "activo": True},
    ).json


def test_crear_pedido_descuenta_stock(client):
    cliente = crear_cliente(client)
    producto = crear_producto(client)

    response = client.post(
        "/api/pedidos",
        json={
            "cliente_id": cliente["id"],
            "producto_id": producto["id"],
            "cantidad": 2,
        },
    )
    assert response.status_code == 201
    assert response.json["cantidad"] == 2

    producto_actualizado = client.get(f'/api/productos/{producto["id"]}').json
    assert producto_actualizado["stock"] == 8
