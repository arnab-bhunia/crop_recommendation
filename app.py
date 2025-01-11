from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils.history_data import log_user_activity, get_user_history
import requests
from utils.crop_data import crop_data
from utils.data_tree import get_states_by_region, get_crop_types_by_state, get_crops_by_type
from utils.user_data import users

app = Flask(__name__)
app.secret_key = "9339956616"  # secure key

# Sample user data 
"""users = {
    "arnab": "123",
    "nayan": "111",
       }"""

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

#signup funtionality
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password == confirm_password:
            users[username] = password
            return redirect(url_for('login'))
        else:
            return 'Passwords do not match'
    return render_template('signup.html')

#login functionality
@app.route('/login', methods=['GET','POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in users and users[username] == password:
        session['username'] = username
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('home'))
   
    
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    # Fetch user data (replace with actual logic)
    current_user = {
        "username": session['username'],
        "history": ["Crop Recommendation: Rice", "Market Price Check: Wheat"]  # Example history
    }
    
    return render_template('dashboard.html', currentUser =current_user)


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    return render_template('input.html')



@app.route('/region_selection')
def region_selection():
    return render_template('region_selection.html')



@app.route('/state_selection/<region>')
def state_selection(region):
    states = get_states_by_region(region)
    return render_template('state_selection.html', region=region, states=states)


@app.route('/crop_type_selection/<state>')
def crop_type_selection(state):
    crop_types = get_crop_types_by_state(state)
    return render_template('crop_type_selection.html', state=state, crop_types=crop_types)



@app.route('/recommendations_r/<state>/<crop_type>')
def recommendations_r(state, crop_type):
    crops = get_crops_by_type(state, crop_type)
    return render_template('recommendations.html', state=state, crop_type=crop_type, crops=crops)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')


@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    username = session['username']
    history = get_user_history(username)
    return render_template('history.html', history=history)




'''@app.route('/market-prices')
def market_prices():
    api_url = "http://127.0.0.1:5000/request?commodity=Rice&state=State&market=West Bengal"  # Replace with actual API URL
    response = requests.get(api_url)
    if response.status_code == 200:
        prices = response.json()
        return render_template('market_prices.html', prices=prices)
    else:
        flash("Unable to fetch market prices at the moment.", "error")
        return redirect(url_for('dashboard'))'''




# Route for crop recommendations
@app.route('/recommendations', methods=['POST'])
def recommendations():
    # Extract input from the form
    soil_type = request.form.get('soil_type')
    temperature = request.form.get('temperature')
    rainfall = request.form.get('rainfall')
    pH = request.form.get('pH')

    # Check if form inputs are valid
    if not (soil_type and temperature and rainfall and pH):
        flash('Please provide all inputs for recommendations.', 'error')
        return redirect(url_for('dashboard'))

    # Simulate crop recommendations (replace with your ML logic or algorithm)
    recommended_crops = crop_recommendation(soil_type, float(temperature), float(rainfall), float(pH))
    
    return render_template('recommendations.html', crops=recommended_crops)

def crop_recommendation(soil_type, temperature, rainfall, pH):
    crops_data = {
        "Rice": {"soil_type": "Loamy", "temperature": (20, 30), "rainfall": (1000, 1500), "pH": (6, 7.5)},
        "Wheat": {"soil_type": "Clayey", "temperature": (10, 25), "rainfall": (450, 650), "pH": (6, 7)},
        "Corn": {"soil_type": "Sandy", "temperature": (18, 27), "rainfall": (500, 750), "pH": (5.5, 7)},
        "Sugarcane": {"soil_type": "Clayey", "temperature": (20, 35), "rainfall": (1500, 2500), "pH": (6.5, 7.5)},
        "Cotton": {"soil_type": "Loamy", "temperature": (25, 35), "rainfall": (700, 1200), "pH": (5.8, 7)},
        "Soybean": {"soil_type": "Clayey", "temperature": (20, 30), "rainfall": (600, 1000), "pH": (6, 7)},
        "Potato": {"soil_type": "Sandy", "temperature": (15, 20), "rainfall": (500, 800), "pH": (5.5, 6.5)},
        "Tomato": {"soil_type": "Loamy", "temperature": (20, 27), "rainfall": (600, 1200), "pH": (6, 6.8)},
        "Onion": {"soil_type": "Sandy", "temperature": (12, 25), "rainfall": (500, 750), "pH": (6, 7)},
        "Carrot": {"soil_type": "Sandy", "temperature": (15, 20), "rainfall": (700, 900), "pH": (6, 6.8)},
        "Barley": {"soil_type": "Loamy", "temperature": (12, 22), "rainfall": (400, 600), "pH": (6, 7)},
        "Peas": {"soil_type": "Clayey", "temperature": (13, 18), "rainfall": (600, 1000), "pH": (6, 7.5)},
        "Lentil": {"soil_type": "Sandy", "temperature": (18, 30), "rainfall": (300, 600), "pH": (6, 7)},
        "Chickpea": {"soil_type": "Clayey", "temperature": (20, 25), "rainfall": (400, 600), "pH": (6, 7)},
        "Banana": {"soil_type": "Loamy", "temperature": (25, 35), "rainfall": (1500, 2500), "pH": (6, 7)},
        "Pineapple": {"soil_type": "Sandy", "temperature": (20, 30), "rainfall": (1200, 1500), "pH": (5, 6)},
        "Coffee": {"soil_type": "Loamy", "temperature": (20, 30), "rainfall": (1000, 2000), "pH": (6, 6.5)},
        "Tea": {"soil_type": "Clayey", "temperature": (18, 30), "rainfall": (1500, 3000), "pH": (4.5, 5.5)},
        "Mustard": {"soil_type": "Sandy", "temperature": (10, 25), "rainfall": (400, 500), "pH": (5.5, 7)},
        "Groundnut": {"soil_type": "Sandy", "temperature": (25, 30), "rainfall": (500, 1000), "pH": (6, 7)},
        "Coconut": {"soil_type": "Sandy", "temperature": (27, 35), "rainfall": (1500, 2500), "pH": (5.2, 8)},
        "Sunflower": {"soil_type": "Loamy", "temperature": (20, 25), "rainfall": (600, 1000), "pH": (6, 7.5)},
        "Sorghum": {"soil_type": "Loamy", "temperature": (25, 30), "rainfall": (400, 800), "pH": (5.8, 7)},
        "Millet": {"soil_type": "Sandy", "temperature": (20, 30), "rainfall": (300, 600), "pH": (5.5, 6.5)},
        "Cabbage": {"soil_type": "Loamy", "temperature": (15, 20), "rainfall": (600, 1000), "pH": (6.5, 7)},
        "Cauliflower": {"soil_type": "Loamy", "temperature": (15, 20), "rainfall": (500, 800), "pH": (6, 7)},
        "Pepper": {"soil_type": "Loamy", "temperature": (20, 30), "rainfall": (600, 1000), "pH": (6, 6.8)},
        "Okra": {"soil_type": "Sandy", "temperature": (25, 30), "rainfall": (600, 800), "pH": (6, 6.8)},
        "Spinach": {"soil_type": "Loamy", "temperature": (15, 20), "rainfall": (400, 600), "pH": (6, 7.5)},
        "Strawberry": {"soil_type": "Loamy", "temperature": (10, 20), "rainfall": (600, 800), "pH": (5.5, 6.5)},
    }

    # List to store suitable crops
    suitable_crops = []

    # Iterate through the crops data to find suitable crops
    for crop, conditions in crops_data.items():
        if (
            soil_type == conditions["soil_type"]
            and conditions["temperature"][0] <= temperature <= conditions["temperature"][1]
            and conditions["rainfall"][0] <= rainfall <= conditions["rainfall"][1]
            and conditions["pH"][0] <= pH <= conditions["pH"][1]
        ):
            suitable_crops.append(crop)
            
        activity = {
        "soil_type": soil_type,
        "temperature": temperature,
        "rainfall": rainfall,
        "pH": pH,
        "recommendations":suitable_crops
    }
    username = session['username']
    log_user_activity(username, activity)
    # Return the suitable crops or a message if none are found
    return suitable_crops if suitable_crops else ["No suitable crops found. Please adjust the parameters."]


@app.route('/crop/<crop_name>')
def crop_details(crop_name):
    if crop_name in crop_data:
        crop_info = crop_data[crop_name]
        return render_template('crop_details.html', crop_name=crop_name, crop_data=crop_info)
    else:
        return "Crop details not available, We will update shortly", 404



# Route for logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
