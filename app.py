from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'delishdash_secret_key_2026'  # Change this in production

# Sample Menu Data (In real project, use Database)
MENU_ITEMS = [
    {
        "id": 1,
        "name": "Hyderabadi Chicken Biryani",
        "description": "Fragrant basmati rice cooked with tender chicken and aromatic spices",
        "price": 249,
        "image_url": "https://images.unsplash.com/photo-1631515243349-e0cb75fb8d3a",
        "category": "indian"
    },
    {
        "id": 2,
        "name": "Margherita Pizza",
        "description": "Classic pizza with fresh mozzarella, basil, and tangy tomato sauce",
        "price": 349,
        "image_url": "https://images.unsplash.com/photo-1604382355076-e894e0e3d8d3",   # Fixed
        "category": "pizza"
    },
    {
        "id": 3,
        "name": "Cheeseburger with Fries",
        "description": "Juicy beef patty with melted cheese, fresh veggies & crispy fries",
        "price": 189,
        "image_url": "https://images.unsplash.com/photo-1568908869189-5f9c1c8f5c0f",   # Fixed
        "category": "burger"
    },
    {
        "id": 4,
        "name": "Paneer Butter Masala",
        "description": "Cottage cheese cubes in rich creamy tomato gravy",
        "price": 229,
        "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7",
        "category": "indian"
    },
    {
        "id": 5,
        "name": "Veg Avocado Bowl",
        "description": "Healthy quinoa bowl with avocado, grilled veggies & tahini dressing",
        "price": 279,
        "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
        "category": "healthy"
    },
    {
        "id": 6,
        "name": "Pepperoni Pizza",
        "description": "Spicy pepperoni with extra cheese on thin crust",
        "price": 399,
        "image_url": "https://images.unsplash.com/photo-1628840042765-356cda07504e",
        "category": "pizza"
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # In real app, add proper authentication here
        email = request.form.get('username')
        password = request.form.get('password')
        
        if email and password:  # Simple validation
            session['user'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('menu'))
        else:
            flash('Please enter email and password', 'error')
    
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

    

