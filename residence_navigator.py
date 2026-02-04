import datetime
from flask import Flask, render_template_string, request, redirect, url_for, flash, session

# ==========================================
# CONFIGURATION & SETUP
# ==========================================
app = Flask(__name__)
app.secret_key = 'super_secret_key_for_session'

# ==========================================
# MOCK DATABASE (In-Memory)
# ==========================================
properties = [
    {
        "id": 1,
        "title": "Luxury Student Studio",
        "price": 550,
        "location": "Daffodil Road, Block A",
        "type": "Studio",
        "bedrooms": 1,
        "description": "A refined studio apartment with modern amenities, perfect for focused studies. Walking distance to campus.",
        "image": "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 2,
        "title": "Elegant 3-Bed Apartment",
        "price": 300,
        "location": "Downtown Heritage Area",
        "type": "Apartment",
        "bedrooms": 3,
        "description": "Spacious living with vintage charm. Ideal for a group of students looking for a premium shared space.",
        "image": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 3,
        "title": "The Scholar's Loft",
        "price": 420,
        "location": "Academic District",
        "type": "Apartment",
        "bedrooms": 2,
        "description": "Modern minimalist design with high-speed internet and study corners.",
        "image": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=600&q=80"
    }
]

# ==========================================
# FRONTEND TEMPLATE (HTML/TAILWIND)
# ==========================================
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daffo House Rent</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <!-- Classy Fonts: Playfair Display (Serif) for Headings, Lato (Sans) for Body -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
    
    <style>
        body { font-family: 'Lato', sans-serif; }
        h1, h2, h3, h4, .brand-font { font-family: 'Playfair Display', serif; }
        .gold-accent { color: #d4af37; }
        .bg-navy { background-color: #0f172a; } /* Slate 900 */
    </style>
</head>
<body class="bg-stone-50 text-slate-800 font-sans flex flex-col min-h-screen">

    <!-- Navigation -->
    <nav class="bg-navy text-white shadow-xl sticky top-0 z-50 border-b-2 border-[#d4af37]">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-20">
                <!-- Logo / Brand -->
                <a href="{{ url_for('home') }}" class="flex items-center space-x-3 group">
                    <div class="bg-white p-2 rounded-full border border-[#d4af37]">
                        <i class="fas fa-home text-navy text-lg"></i>
                    </div>
                    <span class="brand-font font-bold text-2xl tracking-wide group-hover:text-[#d4af37] transition-colors">Daffo House Rent</span>
                </a>
                
                <!-- Desktop Menu -->
                <div class="hidden md:flex space-x-6 items-center">
                    <a href="{{ url_for('home') }}" class="hover:text-[#d4af37] transition-colors text-sm uppercase tracking-wider font-medium">Home</a>
                    <a href="{{ url_for('about') }}" class="hover:text-[#d4af37] transition-colors text-sm uppercase tracking-wider font-medium">About Us</a>
                    <a href="{{ url_for('add_property') }}" class="hover:text-[#d4af37] transition-colors text-sm uppercase tracking-wider font-medium">List Property</a>
                    
                    {% if session.get('user') %}
                        <a href="{{ url_for('profile') }}" class="hover:text-[#d4af37] transition-colors text-sm uppercase tracking-wider font-medium">Profile</a>
                        <a href="{{ url_for('logout') }}" class="border border-[#d4af37] text-[#d4af37] px-4 py-2 rounded hover:bg-[#d4af37] hover:text-white transition-all text-sm uppercase tracking-wider">Log Out</a>
                    {% else %}
                         <a href="{{ url_for('login') }}" class="bg-[#d4af37] text-white px-5 py-2 rounded shadow hover:bg-[#b5952f] transition-all text-sm uppercase tracking-wider font-bold">Log In</a>
                    {% endif %}
                </div>
            </div>
        </div>
    </nav>

    <!-- Flash Messages -->
    <div class="max-w-7xl mx-auto px-4 mt-6 w-full">
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="p-4 mb-4 text-sm text-white rounded shadow-lg {{ 'bg-emerald-600' if category == 'success' else 'bg-red-600' }}" role="alert">
                {{ message }}
              </div>
            {% endfor %}
          {% endif %}
        {% endwith %}
    </div>

    <!-- Main Content -->
    <main class="flex-grow">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-navy text-gray-300 py-10 mt-12 border-t-4 border-[#d4af37]">
        <div class="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-8 text-center md:text-left">
            <div>
                <h3 class="text-xl text-white mb-4">Daffo House Rent</h3>
                <p class="text-sm leading-relaxed">Providing premium student accommodation with reliability and class. Your comfort is our priority.</p>
            </div>
            <div>
                <h3 class="text-xl text-white mb-4">Quick Links</h3>
                <ul class="space-y-2 text-sm">
                    <li><a href="{{ url_for('home') }}" class="hover:text-[#d4af37]">Home</a></li>
                    <li><a href="{{ url_for('about') }}" class="hover:text-[#d4af37]">About Us</a></li>
                    <li><a href="{{ url_for('login') }}" class="hover:text-[#d4af37]">Login</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-xl text-white mb-4">Contact</h3>
                <p class="text-sm"><i class="fas fa-envelope mr-2 gold-accent"></i> info@daffohouse.com</p>
                <p class="text-sm mt-2"><i class="fas fa-phone mr-2 gold-accent"></i> +880 1234 567890</p>
            </div>
        </div>
        <div class="text-center mt-8 pt-8 border-t border-slate-700 text-xs text-gray-500">
            &copy; 2025 Daffo House Rent. All rights reserved.
        </div>
    </footer>
</body>
</html>
"""

# ==========================================
# PAGE CONTENT BLOCKS
# ==========================================

home_content = """
{% extends "base" %}
{% block content %}
<!-- Hero Section -->
<div class="relative bg-navy py-24 mb-12 overflow-hidden">
    <div class="absolute inset-0 opacity-20 bg-[url('https://images.unsplash.com/photo-1460317442991-0ec209397118?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80')] bg-cover bg-center"></div>
    <div class="relative max-w-4xl mx-auto px-4 text-center">
        <h1 class="text-4xl md:text-6xl font-bold text-white mb-6 tracking-tight leading-tight">
            Refined Living for <span class="text-[#d4af37] italic">Aspiring Students</span>
        </h1>
        <p class="text-lg md:text-xl text-gray-200 mb-10 font-light">
            Discover a curated selection of hostels and apartments near Daffodil University.
        </p>
        
        <!-- Search Box -->
        <div class="bg-white p-2 rounded-lg shadow-2xl max-w-2xl mx-auto flex">
            <input type="text" placeholder="Search by location or keyword..." class="flex-grow px-4 py-3 outline-none text-gray-700 rounded-l-lg" name="q" form="searchForm">
            <button type="submit" form="searchForm" class="bg-[#d4af37] text-white px-8 py-3 rounded-md hover:bg-[#b5952f] transition-colors font-bold uppercase tracking-wide">
                Find Home
            </button>
        </div>
        <form id="searchForm" action="/" method="GET"></form>
    </div>
</div>

<div class="max-w-7xl mx-auto px-4 mb-16">
    <div class="flex flex-col md:flex-row justify-between items-end mb-8 border-b border-gray-200 pb-4">
        <div>
            <h2 class="text-3xl font-bold text-navy">Exclusive Listings</h2>
            <p class="text-gray-500 mt-1">Handpicked properties for comfort and convenience.</p>
        </div>
        <div class="mt-4 md:mt-0">
             {% if request.args.get('q') %}
                <span class="text-gray-600 mr-2">Showing results for "{{ request.args.get('q') }}"</span>
                <a href="/" class="text-[#d4af37] hover:underline font-bold">Clear Search</a>
            {% endif %}
        </div>
    </div>

    {% if properties|length == 0 %}
        <div class="text-center py-20 bg-white rounded-lg shadow border border-gray-100">
            <i class="fas fa-search text-gray-300 text-5xl mb-4"></i>
            <p class="text-gray-500 text-xl font-serif">No properties found matching your criteria.</p>
        </div>
    {% else %}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
            {% for prop in properties %}
            <div class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 group border border-gray-100 flex flex-col">
                <div class="h-64 relative overflow-hidden">
                    <img src="{{ prop.image }}" alt="{{ prop.title }}" class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700">
                    <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    <span class="absolute top-4 right-4 bg-white/90 backdrop-blur text-navy text-xs font-bold px-3 py-1 rounded shadow uppercase tracking-wider">{{ prop.type }}</span>
                </div>
                <div class="p-8 flex-1 flex flex-col">
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="text-xl font-bold text-navy group-hover:text-[#d4af37] transition-colors">{{ prop.title }}</h3>
                    </div>
                    <div class="flex items-center text-gray-500 text-sm mb-4">
                        <i class="fas fa-map-marker-alt mr-2 text-[#d4af37]"></i> {{ prop.location }}
                    </div>
                    <p class="text-gray-600 mb-6 font-light leading-relaxed flex-1">{{ prop.description }}</p>
                    
                    <div class="border-t border-gray-100 pt-6 flex justify-between items-center mt-auto">
                        <div class="text-2xl font-bold text-navy">${{ prop.price }}<span class="text-sm text-gray-400 font-normal">/mo</span></div>
                        <div class="flex items-center gap-4">
                             <span class="text-sm text-gray-500"><i class="fas fa-bed"></i> {{ prop.bedrooms }}</span>
                             <button class="text-[#d4af37] font-bold text-sm uppercase tracking-wide hover:text-[#b5952f]">Details <i class="fas fa-arrow-right ml-1"></i></button>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    {% endif %}
</div>
{% endblock %}
"""

about_content = """
{% extends "base" %}
{% block content %}
<div class="bg-navy py-16 text-center text-white">
    <h1 class="text-4xl font-bold">About Daffo House Rent</h1>
    <p class="text-gray-300 mt-2 max-w-2xl mx-auto">Connecting students with their home away from home.</p>
</div>
<div class="max-w-4xl mx-auto px-4 py-16">
    <div class="bg-white rounded-xl shadow-xl p-10 border-t-4 border-[#d4af37]">
        <h2 class="text-3xl font-bold text-navy mb-6">Our Mission</h2>
        <p class="text-gray-700 leading-relaxed mb-6 text-lg">
            At <strong>Daffo House Rent</strong>, we understand that finding the right accommodation is crucial for academic success. 
            We are dedicated to providing a premium, hassle-free platform for students of Daffodil University to find safe, 
            affordable, and high-quality housing.
        </p>
        <p class="text-gray-700 leading-relaxed mb-8 text-lg">
            Whether you are looking for a quiet studio to focus on your research or a shared apartment to build lifelong friendships, 
            our verified listings ensure you find exactly what you need.
        </p>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-center mt-12">
            <div class="p-4">
                <div class="w-16 h-16 bg-stone-100 rounded-full flex items-center justify-center mx-auto mb-4 text-[#d4af37]">
                    <i class="fas fa-shield-alt text-2xl"></i>
                </div>
                <h3 class="font-bold text-navy">Secure Booking</h3>
            </div>
             <div class="p-4">
                <div class="w-16 h-16 bg-stone-100 rounded-full flex items-center justify-center mx-auto mb-4 text-[#d4af37]">
                    <i class="fas fa-check-circle text-2xl"></i>
                </div>
                <h3 class="font-bold text-navy">Verified Owners</h3>
            </div>
             <div class="p-4">
                <div class="w-16 h-16 bg-stone-100 rounded-full flex items-center justify-center mx-auto mb-4 text-[#d4af37]">
                    <i class="fas fa-headset text-2xl"></i>
                </div>
                <h3 class="font-bold text-navy">24/7 Support</h3>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

login_content = """
{% extends "base" %}
{% block content %}
<div class="max-w-md mx-auto px-4 py-16">
    <div class="bg-white rounded-xl shadow-2xl overflow-hidden">
        <div class="bg-navy py-6 px-8 border-b border-[#d4af37]">
            <h2 class="text-2xl font-bold text-white text-center">Member Login</h2>
            <p class="text-gray-400 text-center text-sm mt-1">Access your dashboard</p>
        </div>
        <div class="p-8">
            <form method="POST" action="{{ url_for('login') }}" class="space-y-6">
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-1 uppercase tracking-wider">Email Address</label>
                    <input type="email" name="email" required class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-1 uppercase tracking-wider">Password</label>
                    <input type="password" name="password" required class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border">
                </div>
                <div class="flex items-center justify-between">
                    <label class="flex items-center">
                        <input type="checkbox" class="text-[#d4af37] focus:ring-[#d4af37] rounded">
                        <span class="ml-2 text-sm text-gray-600">Remember me</span>
                    </label>
                    <a href="#" class="text-sm text-[#d4af37] hover:underline">Forgot password?</a>
                </div>
                <button type="submit" class="w-full bg-navy text-white py-3 rounded-lg font-bold hover:bg-slate-800 transition-colors uppercase tracking-widest border border-transparent hover:border-[#d4af37]">
                    Sign In
                </button>
            </form>
            <div class="mt-6 text-center text-sm text-gray-500">
                Don't have an account? <a href="#" class="text-[#d4af37] font-bold hover:underline">Register Now</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

profile_content = """
{% extends "base" %}
{% block content %}
<div class="max-w-4xl mx-auto px-4 py-12">
    <div class="bg-white rounded-xl shadow-xl overflow-hidden flex flex-col md:flex-row">
        <!-- Sidebar -->
        <div class="bg-navy p-8 md:w-1/3 text-center md:text-left border-r-4 border-[#d4af37]">
            <div class="w-32 h-32 rounded-full bg-gray-300 mx-auto md:mx-0 mb-4 overflow-hidden border-4 border-white">
                <img src="https://i.pravatar.cc/300" alt="Profile" class="w-full h-full object-cover">
            </div>
            <h2 class="text-2xl font-bold text-white">{{ session.get('user', {}).get('name', 'Student User') }}</h2>
            <p class="text-[#d4af37] mb-6">Verified Student</p>
            
            <nav class="space-y-2">
                <a href="#" class="block text-white bg-white/10 px-4 py-2 rounded">My Profile</a>
                <a href="#" class="block text-gray-400 hover:text-white px-4 py-2 transition">My Bookings</a>
                <a href="#" class="block text-gray-400 hover:text-white px-4 py-2 transition">Settings</a>
            </nav>
        </div>
        
        <!-- Main Details -->
        <div class="p-8 md:w-2/3">
            <h3 class="text-2xl font-bold text-navy mb-6 border-b pb-2">Profile Details</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="block text-xs font-bold text-gray-500 uppercase">Full Name</label>
                    <p class="text-lg font-medium text-gray-900">{{ session.get('user', {}).get('name', 'John Doe') }}</p>
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-500 uppercase">Email</label>
                    <p class="text-lg font-medium text-gray-900">{{ session.get('user', {}).get('email', 'john@example.com') }}</p>
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-500 uppercase">Phone</label>
                    <p class="text-lg font-medium text-gray-900">+880 1XXX XXXXXX</p>
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-500 uppercase">University ID</label>
                    <p class="text-lg font-medium text-gray-900">191-XX-XXXX</p>
                </div>
            </div>

            <div class="mt-8">
                <h4 class="font-bold text-navy mb-4">Recent Activity</h4>
                <div class="bg-stone-50 p-4 rounded border border-gray-200">
                    <p class="text-sm text-gray-600">You viewed <strong>Luxury Student Studio</strong>.</p>
                    <span class="text-xs text-gray-400">2 hours ago</span>
                </div>
            </div>
            
            <div class="mt-8 flex justify-end">
                <a href="{{ url_for('logout') }}" class="text-red-600 font-bold hover:underline">Log Out</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

add_content = """
{% extends "base" %}
{% block content %}
<div class="max-w-3xl mx-auto px-4 py-12">
    <div class="bg-white rounded-xl shadow-xl border-t-4 border-[#d4af37] p-10">
        <h2 class="text-3xl font-bold text-navy mb-8 text-center">List a Property</h2>
        <form method="POST" action="{{ url_for('add_property') }}" class="space-y-6">
            <div>
                <label class="block text-sm font-bold text-gray-700 mb-1">Property Title</label>
                <input type="text" name="title" required class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border" placeholder="e.g. Sunny Apartment near Main Campus">
            </div>
            <div class="grid grid-cols-2 gap-6">
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-1">Price ($/mo)</label>
                    <input type="number" name="price" required class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border" placeholder="500">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-1">Type</label>
                    <select name="type" class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border">
                        <option>Apartment</option>
                        <option>Studio</option>
                        <option>Hostel</option>
                        <option>Shared Flat</option>
                    </select>
                </div>
            </div>
            <div>
                <label class="block text-sm font-bold text-gray-700 mb-1">Location</label>
                <input type="text" name="location" required class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border" placeholder="Address or Area">
            </div>
            <div>
                <label class="block text-sm font-bold text-gray-700 mb-1">Bedrooms</label>
                <input type="number" name="bedrooms" value="1" class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border">
            </div>
            <div>
                <label class="block text-sm font-bold text-gray-700 mb-1">Description</label>
                <textarea name="description" rows="4" class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border" placeholder="Describe the amenities, rules, and nearby facilities..."></textarea>
            </div>
            <div class="flex justify-end pt-6 gap-4">
                <a href="{{ url_for('home') }}" class="px-6 py-3 text-sm font-bold text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition">Cancel</a>
                <button type="submit" class="px-8 py-3 text-sm font-bold text-white bg-navy rounded-lg hover:bg-slate-800 transition shadow-lg border-b-4 border-[#d4af37]">Publish Listing</button>
            </div>
        </form>
    </div>
</div>
{% endblock %}
"""

# ==========================================
# ROUTES
# ==========================================

def render_page(content_block, **kwargs):
    """Helper to merge content block into base template"""
    full_template = html_template.replace('{% block content %}{% endblock %}', content_block)
    full_template = full_template.replace('{% extends "base" %}', '')
    return render_template_string(full_template, **kwargs)

@app.route('/')
def home():
    query = request.args.get('q', '').lower()
    if query:
        filtered_props = [p for p in properties if query in p['title'].lower() or query in p['location'].lower()]
    else:
        filtered_props = properties
    return render_page(home_content, properties=filtered_props, request=request, session=session)

@app.route('/about')
def about():
    return render_page(about_content, session=session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Mock Login
        email = request.form.get('email')
        # Simulate user data
        session['user'] = {'name': 'John Student', 'email': email}
        flash('Welcome back! You have successfully logged in.', 'success')
        return redirect(url_for('profile'))
    return render_page(login_content, session=session)

@app.route('/profile')
def profile():
    if not session.get('user'):
        flash('Please log in to view your profile.', 'error')
        return redirect(url_for('login'))
    return render_page(profile_content, session=session)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        new_prop = {
            "id": len(properties) + 1,
            "title": request.form['title'],
            "price": request.form['price'],
            "location": request.form['location'],
            "type": request.form['type'],
            "bedrooms": request.form['bedrooms'],
            "description": request.form['description'],
            "image": "https://placehold.co/600x400?text=New+Listing"
        }
        properties.append(new_prop)
        flash('Property listed successfully!', 'success')
        return redirect(url_for('home'))
    return render_page(add_content, session=session)

if __name__ == '__main__':
    print("Starting Daffo House Rent on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)