import datetime
from flask import Flask, render_template_string, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import socket
from frontend_templates import (
    base_template,
    home_content,
    about_content,
    register_content,
    login_content,
    profile_content,
    add_content
)

# ==========================================
# CONFIGURATION & SETUP
# ==========================================
app = Flask(__name__)
app.secret_key = 'diu_super_secret_key'

# ==========================================
# MOCK DATABASE (In-Memory)
# ==========================================

# 1. Users Database
users_db = {} 

# 2. Properties Database (Local Dhaka/Ashulia Context)
properties = [
    {
        "id": 1,
        "title": "Green Garden Hostel",
        "price": 4500,
        "location": "Daffodil Smart City, Ashulia",
        "type": "Hostel",
        "bedrooms": "Shared (2 Person)",
        "description": "Located right next to the permanent campus. High-speed wifi, 3-times meal included, and generator backup available.",
        "image": "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 2,
        "title": "Dhanmondi Lakeview Flat",
        "price": 25000,
        "location": "Road 32, Dhanmondi, Dhaka",
        "type": "Flat",
        "bedrooms": 3,
        "description": "A quiet family flat available for student groups (female only). Near the old campus area.",
        "image": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 3,
        "title": "Sobhanbag Bachelor Mess",
        "price": 3500,
        "location": "Sobhanbag, near Prince Plaza",
        "type": "Bachelor",
        "bedrooms": "1 Seat",
        "description": "Secure environment. 5 minutes walking distance from main road bus stop. Ideal for single male students.",
        "image": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 4,
        "title": "Rayan's Rooftop Studio",
        "price": 8000,
        "location": "Mirpur 10, Dhaka",
        "type": "Sublet",
        "bedrooms": 1,
        "description": "Fully furnished studio apartment (sublet) with easy metro rail access to the university.",
        "image": "https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=600&q=80"
    }
]

# ==========================================
# ROUTES
# ==========================================

def render_page(content_block, **kwargs):
    """Helper to merge content block into base template"""
    full_template = base_template.replace('{% block content %}{% endblock %}', content_block)
    full_template = full_template.replace('{% extends "base" %}', '')
    return render_template_string(full_template, **kwargs)

@app.route('/')
def home():
    # --- Filter Logic ---
    query = request.args.get('q', '').lower()
    prop_type = request.args.get('type', 'All')
    max_price = request.args.get('max_price')

    filtered_props = properties

    # 1. Filter by Text (Location or Title)
    if query:
        filtered_props = [p for p in filtered_props if query in p['title'].lower() or query in p['location'].lower()]

    # 2. Filter by Type
    if prop_type != 'All':
        filtered_props = [p for p in filtered_props if p['type'] == prop_type]
    
    # 3. Filter by Price
    if max_price:
        try:
            limit = int(max_price)
            filtered_props = [p for p in filtered_props if int(p['price']) <= limit]
        except ValueError:
            pass # Ignore invalid price inputs

    return render_page(home_content, properties=filtered_props, request=request, session=session)

@app.route('/about')
def about():
    return render_page(about_content, session=session)

@app.route('/profile')
def profile():
    if not session.get('user'):
        flash('Please log in to view your profile.', 'error')
        return redirect(url_for('login'))
    return render_page(profile_content, session=session)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        student_id = request.form.get('student_id')

        if email in users_db:
            flash('Email already registered! Please login.', 'error')
            return redirect(url_for('login'))
        
        # Save user to in-memory DB
        users_db[email] = {
            'name': name,
            'password': generate_password_hash(password),
            'student_id': student_id
        }
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_page(register_content, session=session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = users_db.get(email)
        
        if user and check_password_hash(user['password'], password):
            session['user'] = {'name': user['name'], 'email': email, 'student_id': user['student_id']}
            flash(f"Welcome back, {user['name']}!", 'success')
            return redirect(url_for('profile')) # Redirect to profile after login
        else:
            flash('Invalid email or password.', 'error')
            
    return render_page(login_content, session=session)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
def add_property():
    if not session.get('user'):
        flash('You must be logged in to list a property.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_prop = {
            "id": len(properties) + 1,
            "title": request.form['title'],
            "price": request.form['price'],
            "location": request.form['location'],
            "type": request.form['type'],
            "bedrooms": request.form['bedrooms'],
            "description": request.form['description'],
            "image": "https://placehold.co/600x400?text=New+Dhaka+Listing"
        }
        properties.append(new_prop)
        flash('Property listed successfully!', 'success')
        return redirect(url_for('home'))
    return render_page(add_content, session=session)

if __name__ == '__main__':
    print("Starting Daffo House Rent on http://127.0.0.1:5000")
    # Using 0.0.0.0 allows LAN access (same wifi)
    app.run(host='0.0.0.0', debug=True, port=5000)