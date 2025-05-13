from flask import Flask, request, jsonify, render_template, redirect, url_for
from flasgger import Swagger
import psycopg2
from psycopg2 import DatabaseError

app = Flask(__name__)
swagger = Swagger(app)

try:
    conn = psycopg2.connect(
        dbname="qwe",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )
    conn.autocommit = True
    print("Подключение к базе данных успешно!")
except DatabaseError as e:
    print(f"Ошибка подключения к базе данных: {e}")
    exit()

cur = conn.cursor()

@app.route('/add_game', methods=['POST'])
def add_game():
    data = request.json
    name = data.get("name")
    price = data.get("price")
    quantity = data.get("quantity")

    if not name or price is None or quantity is None:
        return jsonify({"error": "Некорректные данные"}), 400

    try:
        cur.execute(
            "INSERT INTO games (name, price, quantity) VALUES (%s, %s, %s)",
            (name, float(price), int(quantity))
        )
        return jsonify({"message": "Данные сохранены!"}), 200
    except Exception as e:
        print(f"Ошибка при вставке: {e}")
        return jsonify({"error": "Ошибка при сохранении данных"}), 500

@app.route('/get_games', methods=['GET'])
def get_games():
    try:
        cur.execute("SELECT name, price, quantity FROM games ORDER BY name")
        rows = cur.fetchall()
        games = [{"name": r[0], "price": r[1], "quantity": r[2]} for r in rows]
        return jsonify(games), 200
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return jsonify({"error": "Ошибка при получении данных"}), 500

@app.route('/update_game', methods=['PUT'])
def update_game():
    data = request.json
    name = data.get("name")
    price = data.get("price")
    quantity = data.get("quantity")

    if not name or price is None or quantity is None:
        return jsonify({"error": "Некорректные данные"}), 400

    try:
        cur.execute(
            "UPDATE games SET price = %s, quantity = %s WHERE name = %s",
            (float(price), int(quantity), name)
        )
        if cur.rowcount == 0:
            return jsonify({"error": "Игра не найдена"}), 404
        return jsonify({"message": "Игра обновлена"}), 200
    except Exception as e:
        print(f"Ошибка при обновлении: {e}")
        return jsonify({"error": "Ошибка при обновлении"}), 500

@app.route('/delete_game', methods=['DELETE'])
def delete_game():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Название игры не указано"}), 400

    try:
        cur.execute("DELETE FROM games WHERE name = %s", (name,))
        if cur.rowcount == 0:
            return jsonify({"error": "Игра не найдена"}), 404
        return jsonify({"message": "Игра удалена"}), 200
    except Exception as e:
        print(f"Ошибка при удалении: {e}")
        return jsonify({"error": "Ошибка при удалении"}), 500

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Здесь будет логика для проверки логина и пароля
        if username != "admin" or password != "password":  # Пример проверки
            return render_template('login.html', error="Неверное имя пользователя или пароль")

        return f'Добро пожаловать, {username}!'
    return render_template('login.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)