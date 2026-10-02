def test_crear_y_listar_producto(client):
    response = client.post(
        "/api/productos",
        json={
            "nombre": "Teclado",
            "descripcion": "Mecánico",
            "precio": 350,
            "stock": 5,
            "activo": True,
        },
    )
    assert response.status_code == 201
    assert response.json["nombre"] == "Teclado"

    response = client.get("/api/productos")
    assert response.status_code == 200
    assert len(response.json) == 1


def test_rechaza_stock_negativo(client):
    response = client.post(
        "/api/productos",
        json={"nombre": "Mouse", "precio": 100, "stock": -1},
    )
    assert response.status_code == 400
