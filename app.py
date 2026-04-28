from flask import Flask, render_template, request, redirect
import sqlite3

app=Flask(__name__)

def init_db():
    conn=sqlite3.connect("expenses.db")
    cursor=conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            category TEXT
        )''')
    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    total = sum(expense[2] for expense in expenses)
    conn.close()
    return render_template("index.html", expenses=expenses, total=total)

@app.route("/add", methods=["POST"])
def add():
    description=request.form["description"]
    amount = request.form["amount"]
    category = request.form["category"]
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (description, amount, category) VALUES (?, ?, ?)",
                   (description, amount, category))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
    