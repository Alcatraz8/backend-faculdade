import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "passwd": "318269",
    "database": "mydb",
}

connection = mysql.connector.connect(**db_config)
print("banco de dados conectado com sucesso")


@app.route("/pedido", methods=['POST'])
def fazer_pedido():
    dados_json = request.get_json()

    if (
            "produto_id" not in dados_json
            or "nome_produto" not in dados_json
            or "quantidade_produto" not in dados_json
            or "tamanho_produto" not in dados_json
            or "preco_produto" not in dados_json
            or "valor_total" not in dados_json
    ):
        return jsonify({"erro": "Campos inválidos"})

    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO pedido (produto_id, nome_produto, quantidade_produto, tamanho_produto, preco_produto, valor_total) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (
                dados_json["produto_id"],
                dados_json["nome_produto"],
                dados_json["quantidade_produto"],
                dados_json["tamanho_produto"],
                dados_json["preco_produto"],
                dados_json["valor_total"],
            )
            cursor.execute(query, values)
            connection.commit()
            return jsonify({"mensagem": "Produto adicionado com sucesso"})
    except Exception as e:
        return jsonify({"erro": f"Erro ao adicionar produto: {str(e)}"})


@app.route("/protese", methods=['GET'])
def get_proteses():
    return jsonify(proteses=select_from_protese())


@app.route("/produtos", methods=['GET'])
def get_produtos():
    return jsonify(produtos=select_from_produto())


@app.route("/pedidos", methods=['GET'])
def get_pedidos():
    return jsonify(pedidos=select_from_pedidos())


def select_from_protese():
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM protese")
        records = cursor.fetchall()
        print("Total number of rows in protese is: ", cursor.rowcount)

        print("\nPrinting each protese record")

        listaProtese = []

        for row in records:
            listaProtese.append(
                {
                    "id_protese": row[0],
                    "nome": row[1],
                    "descricao": row[2],
                    "valor": row[3],
                },
            )

        return listaProtese
    except Exception as e:
        return jsonify({"erro": f"Erro ao obter dados de protese: {str(e)}"})
    finally:
        if connection.is_connected():
            cursor.close()


def select_from_pedidos():
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM pedido")
        records = cursor.fetchall()
        print("Total number of rows in pedido is: ", cursor.rowcount)

        print("\nPrinting each pedido record")

        listaPedido = []

        for row in records:
            listaPedido.append(
                {
                    "produto_id": row[0],
                    "nome_produto": row[1],
                    "quantidade_produto": row[2],
                    "tamanho_produto": row[3],
                    "preco_produto": row[4],
                    "valor_total": row[5],
                },
            )

        return listaPedido
    except Exception as e:
        return jsonify({"erro": f"Erro ao obter dados de protese: {str(e)}"})
    finally:
        if connection.is_connected():
            cursor.close()


def select_from_produto():
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM produto")
        records = cursor.fetchall()
        print("Total number of rows in produto is: ", cursor.rowcount)

        print("\nPrinting each produto record")

        listaProdutos = []

        for row in records:
            listaProdutos.append(
                {
                    "idproduto": row[0],
                    "nome": row[1],
                    "valor": row[2],
                    "peso": row[3],
                    "descricao": row[4],
                    "tamanho": row[5],
                    "quantidade": row[6],
                    "urlimg": row[7],
                },
            )

        return listaProdutos
    except Exception as e:
        return jsonify({"erro": f"Erro ao obter dados de produto: {str(e)}"})
    finally:
        if connection.is_connected():
            cursor.close()


if __name__ == "__main__":
    app.run(port=3000, host='0.0.0.0')
