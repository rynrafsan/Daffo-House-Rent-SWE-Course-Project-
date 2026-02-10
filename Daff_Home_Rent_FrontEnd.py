# ==========================================
# FRONTEND TEMPLATES (HTML/CSS/JS)
# ==========================================

base_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daffo House Rent | DIU</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <!-- Classy Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
    
    <style>
        body { font-family: 'Lato', sans-serif; }
        h1, h2, h3, h4, .brand-font { font-family: 'Playfair Display', serif; }
        .gold-accent { color: #d4af37; }
        .bg-navy { background-color: #0f172a; } /* Slate 900 */
        .btn-gold { 
            background-color: #d4af37; 
            color: white; 
            transition: all 0.3s;
        }
        .btn-gold:hover { 
            background-color: #b5952f; 
            transform: translateY(-1px);
        }
        /* Custom Select Arrow */
        select {
            -webkit-appearance: none;
            -moz-appearance: none;
            background-image: url("data:image/svg+xml;utf8,<svg fill='gray' height='24' viewBox='0 0 24 24' width='24' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/><path d='M0 0h24v24H0z' fill='none'/></svg>");
            background-repeat: no-repeat;
            background-position-x: 98%;
            background-position-y: 50%;
        }
    </style>
</head>
<body class="bg-stone-50 text-slate-800 font-sans flex flex-col min-h-screen">

    <!-- Navigation -->
    <nav class="bg-navy text-white shadow-xl sticky top-0 z-50 border-b-2 border-[#d4af37]">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-20">
                <!-- Decent Logo -->
                <a href="{{ url_for('home') }}" class="flex items-center space-x-3 group">
                    <div class="relative w-12 h-12 flex items-center justify-center bg-white rounded-lg shadow-lg border-2 border-[#d4af37]">
                        <i class="fas fa-home text-navy text-xl absolute mb-1"></i>
                        <i class="fas fa-graduation-cap text-[#d4af37] text-2xl absolute -mt-4 -mr-4 transform rotate-12"></i>
                    </div>
                    <div class="flex flex-col">
                        <span class="brand-font font-bold text-2xl tracking-wide group-hover:text-[#d4af37] transition-colors leading-none mt-1">Daffo House</span>
                        <span class="text-[10px] text-[#d4af37] uppercase tracking-[0.2em] font-bold">Rent & Residence</span>
                    </div>
                </a>
                
                <!-- Menu -->
                <div class="hidden md:flex space-x-6 items-center">
                    <a href="{{ url_for('home') }}" class="hover:text-[#d4af37] text-sm uppercase font-medium tracking-wider">Home</a>
                    <a href="{{ url_for('about') }}" class="hover:text-[#d4af37] text-sm uppercase font-medium tracking-wider">About Team</a>
                    <a href="{{ url_for('add_property') }}" class="hover:text-[#d4af37] text-sm uppercase font-medium tracking-wider">List Property</a>
                    
                    {% if session.get('user') %}
                        <div class="flex items-center gap-4 ml-4 pl-4 border-l border-slate-700">
                             <a href="{{ url_for('profile') }}" class="flex items-center gap-2 hover:text-[#d4af37] transition group">
                                <div class="w-8 h-8 rounded-full bg-[#d4af37] text-navy flex items-center justify-center font-bold text-xs">
                                    {{ session.get('user')['name'][0] }}
                                </div>
                                <span class="text-sm font-bold group-hover:underline">Profile</span>
                            </a>
                            <a href="{{ url_for('logout') }}" class="text-gray-400 hover:text-white transition text-xs uppercase font-bold"><i class="fas fa-sign-out-alt"></i></a>
                        </div>
                    {% else %}
                        <div class="flex items-center gap-3 ml-4">
                            <a href="{{ url_for('login') }}" class="text-white hover:text-[#d4af37] px-3 py-2 text-sm uppercase font-medium tracking-wider">Log In</a>
                            <a href="{{ url_for('register') }}" class="btn-gold px-5 py-2 rounded shadow text-sm uppercase font-bold tracking-wider">Register</a>
                        </div>
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
                <h3 class="text-xl text-white mb-4 brand-font">Daffo House Rent</h3>
                <p class="text-sm leading-relaxed text-gray-400">
                    Trusted accommodation solutions for DIU students. 
                    Built with love in Dhaka, Bangladesh.
                </p>
            </div>
            <div>
                <h3 class="text-xl text-white mb-4 brand-font">Campus Links</h3>
                <ul class="space-y-2 text-sm">
                    <li><a href="#" class="hover:text-[#d4af37]">DIU Portal</a></li>
                    <li><a href="#" class="hover:text-[#d4af37]">Smart City Map</a></li>
                    <li><a href="#" class="hover:text-[#d4af37]">Transport Schedule</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-xl text-white mb-4 brand-font">Contact Us</h3>
                <p class="text-sm"><i class="fas fa-map-marker-alt mr-2 gold-accent"></i> Daffodil Smart City, Ashulia</p>
                <p class="text-sm mt-2"><i class="fas fa-phone mr-2 gold-accent"></i> +880 1711 000000</p>
                <p class="text-sm mt-2"><i class="fas fa-envelope mr-2 gold-accent"></i> support@daffohouse.bd</p>
            </div>
        </div>
        <div class="text-center mt-8 pt-8 border-t border-slate-700 text-xs text-gray-500">
            &copy; 2025 Daffo House Rent. All rights reserved.
        </div>
    </footer>
</body>
</html>
"""

home_content = """
{% extends "base" %}
{% block content %}
<!-- Hero Section -->
<div class="relative bg-navy pt-20 pb-28 mb-12 overflow-hidden">
    <!-- Dhaka Skyline Overlay -->
    <div class="absolute inset-0 opacity-20 bg-[url('https://images.unsplash.com/photo-1628525881478-43d9a044b76c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80')] bg-cover bg-center"></div>
    <div class="relative max-w-5xl mx-auto px-4 text-center">
        <h1 class="text-4xl md:text-6xl font-bold text-white mb-6 tracking-tight leading-tight">
            Find Your Home Near <br/><span class="text-[#d4af37] italic">Daffodil Smart City</span>
        </h1>
        <p class="text-lg text-gray-200 mb-10 font-light max-w-2xl mx-auto">
            Verified hostels, flats, and bachelor messes for DIU students.
        </p>
        
        <!-- Advanced Search Filter Box -->
        <div class="bg-white p-4 rounded-xl shadow-2xl max-w-4xl mx-auto border-t-4 border-[#d4af37]">
            <form action="/" method="GET" class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
                
                <!-- Keyword/Location -->
                <div class="col-span-1 md:col-span-1 text-left">
                    <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Location</label>
                    <div class="relative">
                        <i class="fas fa-map-marker-alt absolute left-3 top-3 text-gray-400"></i>
                        <input type="text" name="q" placeholder="Ashulia, Mirpur..." value="{{ request.args.get('q', '') }}" 
                               class="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#d4af37] outline-none transition">
                    </div>
                </div>

                <!-- Type Filter -->
                <div class="col-span-1 text-left">
                    <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Property Type</label>
                    <div class="relative">
                        <i class="fas fa-home absolute left-3 top-3 text-gray-400"></i>
                        <select name="type" class="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#d4af37] outline-none transition cursor-pointer">
                            <option value="All" {% if request.args.get('type') == 'All' %}selected{% endif %}>All Types</option>
                            <option value="Flat" {% if request.args.get('type') == 'Flat' %}selected{% endif %}>Family Flat</option>
                            <option value="Hostel" {% if request.args.get('type') == 'Hostel' %}selected{% endif %}>Hostel</option>
                            <option value="Bachelor" {% if request.args.get('type') == 'Bachelor' %}selected{% endif %}>Bachelor Mess</option>
                            <option value="Sublet" {% if request.args.get('type') == 'Sublet' %}selected{% endif %}>Sublet / Other</option>
                        </select>
                    </div>
                </div>

                <!-- Price Filter -->
                <div class="col-span-1 text-left">
                    <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Max Price (BDT)</label>
                    <div class="relative">
                        <span class="absolute left-3 top-2 text-gray-400 font-bold">৳</span>
                        <input type="number" name="max_price" placeholder="Any" value="{{ request.args.get('max_price', '') }}"
                               class="w-full pl-8 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#d4af37] outline-none transition">
                    </div>
                </div>

                <!-- Submit Button -->
                <div class="col-span-1">
                    <button type="submit" class="w-full bg-[#d4af37] text-white font-bold py-2.5 rounded-lg hover:bg-[#b5952f] transition shadow-md uppercase tracking-wider">
                        Search
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

<div class="max-w-7xl mx-auto px-4 mb-16">
    <div class="flex flex-col md:flex-row justify-between items-end mb-8 border-b border-gray-200 pb-4">
        <div>
            <h2 class="text-3xl font-bold text-navy">Latest Listings</h2>
            <p class="text-gray-500 mt-1">Safe and student-friendly environments in Dhaka.</p>
        </div>
        <div class="mt-4 md:mt-0">
             {% if request.args.get('q') or request.args.get('type') != 'All' %}
                <span class="text-gray-600 mr-2 text-sm">Showing filtered results</span>
                <a href="/" class="text-[#d4af37] hover:underline font-bold text-sm">Clear All Filters</a>
            {% endif %}
        </div>
    </div>

    {% if properties|length == 0 %}
        <div class="text-center py-20 bg-white rounded-lg shadow border border-gray-100">
            <i class="fas fa-search-location text-gray-300 text-6xl mb-4"></i>
            <h3 class="text-xl font-bold text-gray-600">No properties found</h3>
            <p class="text-gray-500 mt-2">Try adjusting your filters or price range.</p>
            <a href="/" class="mt-4 inline-block text-[#d4af37] font-bold">View all listings</a>
        </div>
    {% else %}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
            {% for prop in properties %}
            <div class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 group border border-gray-100 flex flex-col">
                <div class="h-64 relative overflow-hidden">
                    <img src="{{ prop.image }}" alt="{{ prop.title }}" class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700">
                    <span class="absolute top-4 right-4 bg-navy/90 text-[#d4af37] text-xs font-bold px-3 py-1 rounded shadow uppercase tracking-wider">{{ prop.type }}</span>
                </div>
                <div class="p-8 flex-1 flex flex-col">
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="text-xl font-bold text-navy group-hover:text-[#d4af37] transition-colors">{{ prop.title }}</h3>
                    </div>
                    <div class="flex items-center text-gray-500 text-sm mb-4">
                        <i class="fas fa-map-marker-alt mr-2 text-[#d4af37]"></i> {{ prop.location }}
                    </div>
                    <p class="text-gray-600 mb-6 font-light leading-relaxed flex-1 text-sm">{{ prop.description }}</p>
                    
                    <div class="border-t border-gray-100 pt-6 flex justify-between items-center mt-auto">
                        <div class="text-2xl font-bold text-navy">৳{{ prop.price }}<span class="text-sm text-gray-400 font-normal">/mo</span></div>
                        <button class="text-[#d4af37] font-bold text-sm uppercase tracking-wide hover:text-[#b5952f]">Details <i class="fas fa-arrow-right ml-1"></i></button>
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
    <h1 class="text-4xl font-bold">About Us</h1>
    <p class="text-gray-300 mt-2 max-w-2xl mx-auto">Proudly developed by DIU Students for DIU Students.</p>
</div>
<div class="max-w-6xl mx-auto px-4 py-16">
    <!-- Mission -->
    <div class="bg-white rounded-xl shadow-xl p-10 border-t-4 border-[#d4af37] mb-16">
        <h2 class="text-3xl font-bold text-navy mb-6">Our Mission</h2>
        <p class="text-gray-700 leading-relaxed text-lg">
            Daffodil International University is growing fast, and with the shift to the Smart City in Ashulia, 
            finding accommodation has become a challenge. <strong>Daffo House Rent</strong> was created to solve this problem by 
            connecting students with trusted local landlords in Bangladesh.
        </p>
    </div>

    <!-- The Team -->
    <h2 class="text-3xl font-bold text-navy mb-10 text-center">Meet the Developers</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        
        <!-- Wahid -->
        <div class="bg-white p-6 rounded-lg shadow-md text-center hover:-translate-y-2 transition duration-300">
            <div class="w-24 h-24 bg-gray-200 rounded-full mx-auto mb-4 overflow-hidden">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Wahid" alt="Wahid">
            </div>
            <h3 class="font-bold text-xl text-navy">Wahid</h3>
            <p class="text-[#d4af37] text-sm uppercase tracking-wider font-bold">Backend Lead</p>
            <p class="text-gray-500 text-xs mt-2">Ensuring secure data handling and fast server response.</p>
        </div>

        <!-- Adiba -->
        <div class="bg-white p-6 rounded-lg shadow-md text-center hover:-translate-y-2 transition duration-300">
            <div class="w-24 h-24 bg-gray-200 rounded-full mx-auto mb-4 overflow-hidden">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Adiba" alt="Adiba">
            </div>
            <h3 class="font-bold text-xl text-navy">Adiba</h3>
            <p class="text-[#d4af37] text-sm uppercase tracking-wider font-bold">UI/UX Designer</p>
            <p class="text-gray-500 text-xs mt-2">Crafting the classy and user-friendly interface for students.</p>
        </div>

        <!-- Samira -->
        <div class="bg-white p-6 rounded-lg shadow-md text-center hover:-translate-y-2 transition duration-300">
            <div class="w-24 h-24 bg-gray-200 rounded-full mx-auto mb-4 overflow-hidden">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Samira" alt="Samira">
            </div>
            <h3 class="font-bold text-xl text-navy">Samira</h3>
            <p class="text-[#d4af37] text-sm uppercase tracking-wider font-bold">Quality Assurance</p>
            <p class="text-gray-500 text-xs mt-2">Testing features to ensure a bug-free experience.</p>
        </div>

        <!-- Rayan -->
        <div class="bg-white p-6 rounded-lg shadow-md text-center hover:-translate-y-2 transition duration-300">
            <div class="w-24 h-24 bg-gray-200 rounded-full mx-auto mb-4 overflow-hidden">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Rayan" alt="Rayan">
            </div>
            <h3 class="font-bold text-xl text-navy">Rayan</h3>
            <p class="text-[#d4af37] text-sm uppercase tracking-wider font-bold">Project Manager</p>
            <p class="text-gray-500 text-xs mt-2">Coordinating the team and gathering requirements.</p>
        </div>

        <!-- Nikita -->
        <div class="bg-white p-6 rounded-lg shadow-md text-center hover:-translate-y-2 transition duration-300">
            <div class="w-24 h-24 bg-gray-200 rounded-full mx-auto mb-4 overflow-hidden">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Nikita" alt="Nikita">
            </div>
            <h3 class="font-bold text-xl text-navy">Nikita</h3>
            <p class="text-[#d4af37] text-sm uppercase tracking-wider font-bold">Frontend Developer</p>
            <p class="text-gray-500 text-xs mt-2">Implementing responsive designs and interactive features.</p>
        </div>

    </div>
</div>
{% endblock %}
"""

profile_content = """
{% extends "base" %}
{% block content %}
<div class="bg-navy h-48 w-full"></div> <!-- Header Spacer -->
<div class="max-w-5xl mx-auto px-4 -mt-24 pb-16">
    <div class="bg-white rounded-xl shadow-2xl overflow-hidden flex flex-col md:flex-row border-t-4 border-[#d4af37]">
        
        <!-- Sidebar / User Info -->
        <div class="md:w-1/3 bg-slate-50 p-8 text-center border-r border-gray-100">
            <div class="w-40 h-40 rounded-full border-4 border-white shadow-lg mx-auto overflow-hidden mb-6 bg-white">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={{ session.get('user')['name'] }}" alt="Profile Avatar" class="w-full h-full">
            </div>
            <h2 class="text-2xl font-bold text-navy font-serif">{{ session.get('user')['name'] }}</h2>
            <p class="text-[#d4af37] font-bold text-sm uppercase tracking-wider mt-1">Verified Student</p>
            <p class="text-gray-500 text-sm mt-2">{{ session.get('user')['email'] }}</p>
            
            <div class="mt-8 space-y-3">
                <button class="w-full bg-navy text-white py-2 rounded shadow hover:bg-slate-800 transition text-sm font-bold">Edit Profile</button>
                <a href="{{ url_for('logout') }}" class="block w-full border border-red-200 text-red-500 py-2 rounded hover:bg-red-50 transition text-sm font-bold">Log Out</a>
            </div>
        </div>

        <!-- Details Section -->
        <div class="md:w-2/3 p-10">
            <h3 class="text-2xl font-bold text-navy mb-6 border-b pb-4">Student Information</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
                <div>
                    <span class="block text-xs font-bold text-gray-400 uppercase tracking-widest">Student ID</span>
                    <span class="text-lg font-bold text-gray-800">{{ session.get('user')['student_id'] }}</span>
                </div>
                <div>
                    <span class="block text-xs font-bold text-gray-400 uppercase tracking-widest">University</span>
                    <span class="text-lg font-bold text-gray-800">Daffodil Int. University</span>
                </div>
                <div>
                    <span class="block text-xs font-bold text-gray-400 uppercase tracking-widest">Phone</span>
                    <span class="text-lg font-bold text-gray-800">+880 17XX XXXXXX</span>
                </div>
                <div>
                    <span class="block text-xs font-bold text-gray-400 uppercase tracking-widest">Account Status</span>
                    <span class="inline-block bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-bold uppercase mt-1">Active</span>
                </div>
            </div>

            <h3 class="text-xl font-bold text-navy mb-4">My Activity</h3>
            <div class="bg-blue-50 border border-blue-100 rounded-lg p-4 flex items-center">
                <div class="bg-blue-100 p-3 rounded-full text-blue-600 mr-4">
                    <i class="fas fa-history"></i>
                </div>
                <div>
                    <p class="text-gray-800 font-bold text-sm">No recent bookings</p>
                    <p class="text-gray-500 text-xs">You haven't requested any properties yet.</p>
                </div>
            </div>

        </div>
    </div>
</div>
{% endblock %}
"""

register_content = """
{% extends "base" %}
{% block content %}
<div class="max-w-md mx-auto px-4 py-16">
    <div class="bg-white rounded-xl shadow-2xl overflow-hidden border-t-4 border-[#d4af37]">
        <div class="bg-navy py-6 px-8">
            <h2 class="text-2xl font-bold text-white text-center">Student Registration</h2>
            <p class="text-gray-400 text-center text-sm mt-1">Join the DIU Housing Community</p>
        </div>
        <div class="p-8">
            <form method="POST" action="{{ url_for('register') }}" class="space-y-4">
                <div>
                    <label class="block text-xs font-bold text-gray-700 mb-1 uppercase tracking-wider">Full Name</label>
                    <input type="text" name="name" required class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border" placeholder="e.g. Wahid Ahmed">
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-700 mb-1 uppercase tracking-wider">Email Address</label>
                    <input type="email" name="email" required class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border" placeholder="id@diu.edu.bd">
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-700 mb-1 uppercase tracking-wider">Student ID</label>
                    <input type="text" name="student_id" required class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border" placeholder="e.g. 191-15-XXXX">
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-700 mb-1 uppercase tracking-wider">Password</label>
                    <input type="password" name="password" required class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border">
                </div>
                <button type="submit" class="w-full btn-gold text-white py-3 rounded-lg font-bold uppercase tracking-widest mt-4">
                    Create Account
                </button>
            </form>
            <div class="mt-6 text-center text-sm text-gray-500">
                Already have an account? <a href="{{ url_for('login') }}" class="text-[#d4af37] font-bold hover:underline">Log In</a>
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
    <div class="bg-white rounded-xl shadow-2xl overflow-hidden border-t-4 border-[#d4af37]">
        <div class="bg-navy py-6 px-8">
            <h2 class="text-2xl font-bold text-white text-center">Member Login</h2>
            <p class="text-gray-400 text-center text-sm mt-1">Access your dashboard</p>
        </div>
        <div class="p-8">
            <form method="POST" action="{{ url_for('login') }}" class="space-y-6">
                <div>
                    <label class="block text-xs font-bold text-gray-700 mb-1 uppercase tracking-wider">Email Address</label>
                    <input type="email" name="email" required class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border">
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-700 mb-1 uppercase tracking-wider">Password</label>
                    <input type="password" name="password" required class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border">
                </div>
                <button type="submit" class="w-full bg-navy text-white py-3 rounded-lg font-bold hover:bg-slate-800 transition-colors uppercase tracking-widest border border-transparent hover:border-[#d4af37]">
                    Sign In
                </button>
            </form>
            <div class="mt-6 text-center text-sm text-gray-500">
                Don't have an account? <a href="{{ url_for('register') }}" class="text-[#d4af37] font-bold hover:underline">Register Now</a>
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
        <h2 class="text-3xl font-bold text-navy mb-8 text-center">List a Property in Dhaka</h2>
        <form method="POST" action="{{ url_for('add_property') }}" class="space-y-6">
            <div>
                <label class="block text-sm font-bold text-gray-700 mb-1">Property Title</label>
                <input type="text" name="title" required class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border" placeholder="e.g. Bachelor Flat in Uttara">
            </div>
            <div class="grid grid-cols-2 gap-6">
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-1">Price (BDT/mo)</label>
                    <input type="number" name="price" required class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border" placeholder="5000">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-1">Type</label>
                    <select name="type" class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border">
                        <option value="Flat">Family Flat</option>
                        <option value="Hostel">Hostel</option>
                        <option value="Bachelor">Bachelor Mess</option>
                        <option value="Sublet">Sublet / Other</option>
                    </select>
                </div>
            </div>
            <div>
                <label class="block text-sm font-bold text-gray-700 mb-1">Location (Dhaka)</label>
                <input type="text" name="location" required class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border" placeholder="e.g. Ashulia Model Town">
            </div>
            <div>
                <label class="block text-sm font-bold text-gray-700 mb-1">Bedrooms/Seats</label>
                <input type="text" name="bedrooms" value="1" class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border">
            </div>
            <div>
                <label class="block text-sm font-bold text-gray-700 mb-1">Description</label>
                <textarea name="description" rows="4" class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-[#d4af37] focus:border-[#d4af37] p-3 border" placeholder="Describe facilities like gas, water, internet..."></textarea>
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