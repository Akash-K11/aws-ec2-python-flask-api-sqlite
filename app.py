from flask import Flask, request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


def add_user_to_database(data):

    sql = """
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)    """
    cursor.execute(sql)
    conn.commit()

    sql = """
    INSERT INTO users (name, id)
    VALUES (?, ?)
    """
    cursor.execute(sql, (data["name"], data["id"]))
    conn.commit()


def get_user_from_database():
    sql = """
    SELECT name FROM users where id > 5
    """
    cursor.execute(sql)
    response = cursor.fetchall()
    names = []
    for name in response:
        names.append(name[0])
    return names


@app.route('/adduser', methods=['POST'])
def add_user():
    data = request.get_json()
    try:
        add_user_to_database(data)
    except Exception as e:
        print(e)
    return {"names_with_id_above_5": get_user_from_database()}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
