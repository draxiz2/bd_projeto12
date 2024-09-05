from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/add_to_cart/<int:produto_id>')
def add_to_cart(produto_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(produto_id)
    return redirect(url_for('show_cart'))

@app.route('/carrinho')
def show_cart():
    if 'cart' not in session or not session['cart']:
        return render_template('carrinho.html', produtos=[])

    cart_ids = session['cart']
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)
    query = 'SELECT * FROM PRODUTO WHERE ID_PRODUTO IN (%s)' % ','.join(['%s'] * len(cart_ids))
    cursor.execute(query, cart_ids)
    produtos = cursor.fetchall()
    connection.close()

    return render_template('carrinho.html', produtos=produtos)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nome = request.form['nome']
        valor_prod = request.form['valor_prod']
        qtd_estoque = request.form['qtd_estoque']
        cor = request.form['cor']
        tamanho = request.form['tamanho']
        marca = request.form['marca']
        tipo_tecido = request.form['tipo_tecido']
        
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO PRODUTO (VALOR_PROD, QTD_ESTOQUE, COR, TAMANHO, MARCA, TIPO_TECIDO)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (valor_prod, qtd_estoque, cor, tamanho, marca, tipo_tecido))
        connection.commit()
        connection.close()
        
        return redirect(url_for('product_list'))  # Redireciona para uma página de lista de produtos ou outra página

    return render_template('add_product.html')



@app.route('/roupas')
def roupas():
    connection = get_database_connection()
    if connection is None:
        return "Error connecting to database", 500

    cursor = connection.cursor(dictionary=True)
    
    # Fetch data from CLIENTE table
    cursor.execute("SELECT * FROM CLIENTE")
    clientes = cursor.fetchall()

    # Fetch data from PRODUTO table
    cursor.execute("SELECT * FROM PRODUTO")
    produtos = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('index.html', clientes=clientes, produtos=produtos)

def get_database_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Joao0105",
            database="ecomerce"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
