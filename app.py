from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT,
                  amount REAL,
                  category TEXT,
                  description TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    conn.close()

    total = sum(exp[2] for exp in expenses)
    categories = {}
    for exp in expenses:
        categories[exp[3]] = categories.get(exp[3], 0) + exp[2]

    return render_template("index.html", expenses=expenses, total=total, categories=categories)

@app.route("/add", methods=["POST"])
def add():
    amount = float(request.form["amount"])
    category = request.form["category"]
    description = request.form["description"]
    date = datetime.date.today().strftime("%Y-%m-%d")

    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (date, amount, category, description) VALUES (?, ?, ?, ?)",
              (date, amount, category, description))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        description = request.form["description"]
        c.execute("UPDATE expenses SET amount=?, category=?, description=? WHERE id=?",
                  (amount, category, description, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    else:
        c.execute("SELECT * FROM expenses WHERE id=?", (id,))
        expense = c.fetchone()
        conn.close()
        return render_template("edit.html", expense=expense)

if __name__ == "__main__":
    app.run(debug=True)
