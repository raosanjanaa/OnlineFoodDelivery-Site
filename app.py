from flask import Flask, render_template, request, redirect, session
from db import users, menu, orders

app = Flask(__name__)
app.secret_key = "secret123"

# -------- INSERT MENU (RUNS ONCE) --------
if menu.count_documents({}) == 0:
    menu.insert_many([
        {"name": "Burger", "price": 120},
        {"name": "Pizza", "price": 250},
        {"name": "Pasta", "price": 180},
        {"name": "Sandwich", "price": 100}
    ])

# -------- HOME --------
@app.route("/")
def home():
    return render_template("index.html")

# -------- REGISTER --------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.find_one({"username": username}):
            return "User already exists!"

        users.insert_one({"username": username, "password": password})
        return redirect("/login")

    return render_template("register.html")

# -------- LOGIN --------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users.find_one({"username": username, "password": password})

        if user:
            session["user"] = username
            return redirect("/menu")
        else:
            return "Invalid credentials!"

    return render_template("login.html")

# -------- MENU --------
@app.route("/menu")
def view_menu():
    if "user" not in session:
        return redirect("/login")

    items = list(menu.find())
    return render_template("menu.html", items=items)

# -------- ORDER --------
@app.route("/order", methods=["POST"])
def place_order():
    if "user" not in session:
        return redirect("/login")

    selected_items = request.form.getlist("items")

    cart = []
    total = 0

    for item_name in selected_items:
        item = menu.find_one({"name": item_name})
        if item:
            cart.append(item)
            total += item["price"]

    if cart:
        orders.insert_one({
            "username": session["user"],
            "items": cart,
            "total": total
        })

    return render_template("order.html", total=total)

# -------- LOGOUT --------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# -------- RUN --------
if __name__ == "__main__":
    app.run(debug=True)
    