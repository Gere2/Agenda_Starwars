from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, g
import mysql.connector
from config import Agenda
from fuerza import Fuerza

app = Flask(__name__)
app.secret_key = '1234'

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root1234",
        database="agenda"
    )

@app.route('/')
def index():
    # Mostrar la página principal
    return render_template('index.html')

# Rutas y funciones adicionales para añadir, modificar, consultar y eliminar Jedi/Sith
# ...
@app.route('/add', methods=['POST'])
def add_character():
    name = request.form['name']
    side = request.form['side']
    rank = request.form['rank']
    power_level = request.form['power_level']
    lightsaber_color = request.form['lightsaber_color']

    connection = get_connection()
    cursor = connection.cursor()

    if side == "jedi":
        table = "jedis"
    else:
        table = "siths"

    cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE nombre = %s", (name,))
    existing_character_count = cursor.fetchone()[0]

    if existing_character_count > 0:
        flash(f"Un personaje con el nombre '{name}' ya existe en el lado de los {side.capitalize()} .")
        return redirect(url_for('index'))

    cursor.execute(f"INSERT INTO {table} (nombre, rango, nivel_poder, color_espada) VALUES (%s, %s, %s, %s)", (name, rank, power_level, lightsaber_color))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('index'))


@app.route('/edit/<side>/<int:id>', methods=['GET', 'POST'])
def edit_character(side, id):
    connection = get_connection()
    cursor = connection.cursor()

    if side == "jedi":
        table = "jedis"
    else:
        table = "siths"

    if request.method == 'POST':
        name = request.form['name']
        rank = request.form['rank']
        power_level = request.form['power_level']

        cursor.execute(f"UPDATE {table} SET nombre=%s, rango=%s, nivel_poder=%s WHERE id=%s", (name, rank, power_level, id))
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for('index'))

    cursor.execute(f"SELECT * FROM {table} WHERE id=%s", (id,))
    character = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template('edit_character.html', character=character, side=side)
@app.route('/view/<side>/<int:id>')
def view_character(side, id):
    connection = get_connection()
    cursor = connection.cursor()

    if side == "jedi":
        table = "jedis"
    else:
        table = "siths"

    cursor.execute(f"SELECT * FROM {table} WHERE id=%s", (id,))
    character = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template('view_character.html', character=character, side=side)
@app.route('/delete/<side>/<int:id>')
def delete_character(side, id):
    connection = get_connection()
    cursor = connection.cursor()

    if side == "jedi":
        table = "jedis"
    else:
        table = "siths"

    cursor.execute(f"DELETE FROM {table} WHERE id=%s", (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('index'))
@app.route('/search', methods=['GET', 'POST'])
def search_character():
    if request.method == 'POST':
        search_type = request.form['search_type']
        search_value = request.form['search_value']
        side = request.form['side']

        connection = get_connection()
        cursor = connection.cursor()

        if side == "jedi":
            table = "jedis"
        else:
            table = "siths"

        if search_type == "name":
            cursor.execute(f"SELECT * FROM {table} WHERE nombre=%s", (search_value,))
        elif search_type == "rank":
            cursor.execute(f"SELECT * FROM {table} WHERE rango=%s", (search_value,))
        elif search_type == "power_level":
            cursor.execute(f"SELECT * FROM {table} WHERE nivel_poder=%s", (search_value,))

        characters = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('search_results.html', characters=characters, side=side)

    return render_template('search_character.html')
@app.route('/all_characters')
def all_characters():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM jedis")
    jedis = cursor.fetchall()

    cursor.execute("SELECT * FROM siths")
    siths = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('all_characters.html', jedis=jedis, siths=siths)

def get_side_input():
    while True:
        side = input("Ingresa el bando (jedi/sith): ").lower()
        if side in ["jedi", "sith"]:
            return side
        print("Bando no válido. Por favor, ingresa 'jedi' o 'sith'.")

def get_rank_input(side):
    while True:
        rank = input("Ingresa el rango: ").lower()
        if side == "jedi" and rank in ["padawan", "caballero", "maestro"]:
            return rank
        elif side == "sith" and rank in ["aprendiz", "darth", "lord"]:
            return rank
        print("Rango no válido para el bando seleccionado.")

@app.route('/change_side/<side>/<int:id>', methods=['POST'])
def change_side(side, id):
    connection = get_connection()
    cursor = connection.cursor()

    if side == "jedi":
        origin_table = "jedis"
        target_table = "siths"
    else:
        origin_table = "siths"
        target_table = "jedis"

    cursor.execute(f"INSERT INTO {target_table} (nombre, rango, nivel_poder) SELECT nombre, rango, nivel_poder FROM {origin_table} WHERE id = %s", (id,))
    cursor.execute(f"DELETE FROM {origin_table} WHERE id = %s", (id,))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
