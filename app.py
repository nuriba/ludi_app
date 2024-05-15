from flask import Flask, render_template, jsonify
import json
import os
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

# Load data from JSON files
def load_data():
    with open('data/users.json', 'r') as f:
        users = json.load(f)['users']
        
    with open('data/simulations.json', 'r') as f:
        simulations = json.load(f)['simulations']
        
    return users, simulations

users, simulations = load_data()

# Calculate the number of users per company
def calculate_user_counts(users):
    company_user_counts = defaultdict(int)
    for user in users:
        company_user_counts[user['simulation_name']] += 1
    return company_user_counts

# Calculate daily growth of total users
def calculate_daily_growth(users):
    daily_growth = defaultdict(int)
    for user in users:
        date = datetime.fromordinal(int(user['signup_datetime']) + 366)  # Convert Excel date to datetime
        date_str = date.strftime('%Y-%m-%d')
        daily_growth[date_str] += 1
    
    sorted_dates = sorted(daily_growth.keys())
    cumulative_growth = []
    total_users = 0
    for date in sorted_dates:
        total_users += daily_growth[date]
        cumulative_growth.append({"date": date, "count": total_users})
        
    return cumulative_growth

company_user_counts = calculate_user_counts(users)
daily_growth = calculate_daily_growth(users)

@app.route('/')
def index():
    return render_template('index.html', company_user_counts=company_user_counts)

@app.route('/growth')
def growth():
    return jsonify(daily_growth)


if __name__ == '__main__':
    app.run(debug=True)
