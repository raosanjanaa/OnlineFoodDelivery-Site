from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'delishdash_secret_key_2026'  # Change this in production

# Sample Menu Data (In real project, use Database)
MENU_ITEMS = [
    {
        "id": 1,
        "name": "Veg Biryani",
        "description": "Fragrant basmati rice cooked with fresh vegetables and aromatic spices",
        "price": 219,
        "image_url": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800",  # Proper Veg Biryani
        "category": "indian"
    },
    {
        "id": 2,
        "name": "Cheeseburger with Fries",
        "description": "Juicy beef patty with melted cheese, fresh veggies & crispy fries",
        "price": 189,
        "image_url": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800",
        "category": "burger"
    },
    {
        "id": 3,
        "name": "Paneer Butter Masala",
        "description": "Cottage cheese cubes simmered in rich creamy tomato gravy",
        "price": 229,
        "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=800",
        "category": "indian"
    },
    {
        "id": 4,
        "name": "Veg Avocado Bowl",
        "description": "Healthy quinoa bowl with avocado, grilled vegetables & tahini dressing",
        "price": 279,
        "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800",
        "category": "healthy"
    },
    {
        "id": 5,
        "name": "Veg Fried Rice",
        "description": "Stir-fried rice with fresh vegetables, spring onions and soy sauce",
        "price": 179,
        "image_url": "https://images.unsplash.com/photo-1603138461772-6e9b0c3e5e4e?w=800",
        "category": "indian"
    },
    {
        "id": 6,
        "name": "Mushroom Masala",
        "description": "Fresh mushrooms cooked in spicy onion-tomato gravy",
        "price": 199,
        "image_url": "https://images.unsplash.com/photo-1630409357623-0b5e2b9f8f3f?w=800",
        "category": "indian"
    }
]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            # For demo - in real app, check against database
            session['user'] = username
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('menu'))
        else:
            flash('Please enter username and password', 'error')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # In real app, save user to database
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/menu')
def menu():
    if 'user' not in session:
        flash('Please login to view menu', 'warning')
        return redirect(url_for('login'))
    
    return render_template('menu.html', menu_items=MENU_ITEMS)

@app.route('/order', methods=['GET', 'POST'])
def order():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # For demo, we generate a random order ID
    import random
    order_id = f"DD{random.randint(100000, 999999)}"
    
    # In real app, you would calculate total from cart stored in session or DB
    total = 598  # Demo total
    
    return render_template('order.html', 
                         order_id=order_id, 
                         total=total)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))

# Error handlers (Optional but recommended)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

if __name__ == '__main__':
    app.run(debug=True)

    

