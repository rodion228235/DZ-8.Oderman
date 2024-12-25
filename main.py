from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Ініціалізація бази даних
def init_db():
    conn = sqlite3.connect('orderman.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS menu_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT NOT NULL,
                        price REAL NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# Головна сторінка з меню
@app.route('/')
def menu():
    conn = sqlite3.connect('orderman.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items")
    items = cursor.fetchall()
    conn.close()
    return render_template('menu.html', items=items)

# Додавання нової страви
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])

        conn = sqlite3.connect('orderman.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO menu_items (name, description, price) VALUES (?, ?, ?)", (name, description, price))
        conn.commit()
        conn.close()

        return redirect(url_for('menu'))

    return render_template('add_item.html')

# Редагування страви
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    conn = sqlite3.connect('orderman.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])

        cursor.execute("UPDATE menu_items SET name = ?, description = ?, price = ? WHERE id = ?", (name, description, price, item_id))
        conn.commit()
        conn.close()
        return redirect(url_for('menu'))

    cursor.execute("SELECT * FROM menu_items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    return render_template('edit_item.html', item=item)

# Видалення страви
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = sqlite3.connect('orderman.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('menu'))

if __name__ == '__main__':
    app.run(debug=True)
