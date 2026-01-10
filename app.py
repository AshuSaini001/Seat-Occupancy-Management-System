import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Get the folder where this script is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Join it with the filename
SEAT_FILE = os.path.join(BASE_DIR, "seats.txt")

# Define the file path relative to the script location
# This replaces the hardcoded F:/ path so it works on any computer
SEAT_FILE = "seats.txt"

# --- HELPER FUNCTIONS (Based on your original code) ---

def load_seats():
    """Loads seat data from the text file."""
    if not os.path.exists(SEAT_FILE):
        # Create a default 5x5 grid if file doesn't exist
        default_seats = [[0]*5 for _ in range(5)]
        save_seats(default_seats)
        return default_seats

    try:
        with open(SEAT_FILE, "r") as f:
            return [list(map(int, line.strip().split())) for line in f]
    except Exception as e:
        print(f"Error loading file: {e}")
        return []

def save_seats(seats):
    """Saves seat data to the text file."""
    with open(SEAT_FILE, "w") as f:
        for row in seats:
            f.write(" ".join(map(str, row)) + "\n")

def count_seats(seats):
    """Returns occupied and vacant counts."""
    total_occupied = sum(row.count(1) for row in seats)
    total_vacant = sum(row.count(0) for row in seats)
    return total_occupied, total_vacant

# --- FLASK ROUTES ---

@app.route('/')
def index():
    """Main page: displays the seat map and stats."""
    seats = load_seats()
    occupied, vacant = count_seats(seats)
    return render_template('index.html', seats=seats, occupied=occupied, vacant=vacant)

@app.route('/toggle/<int:row>/<int:col>')
def toggle_seat(row, col):
    """Changes a seat from Vacant to Occupied or vice versa."""
    seats = load_seats()
    
    # Check bounds
    if 0 <= row < len(seats) and 0 <= col < len(seats[0]):
        # Toggle: If 0 becomes 1, if 1 becomes 0
        seats[row][col] = 1 if seats[row][col] == 0 else 0
        save_seats(seats)
    
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles uploading a custom text file."""
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        # Save the uploaded file content to our seat file
        # We read the content and overwrite our local seats.txt
        content = file.read().decode('utf-8')
        
        # Simple validation: ensure it contains only numbers and spaces
        try:
            # Process to verify it's valid data before saving
            lines = content.strip().split('\n')
            temp_seats = [list(map(int, line.strip().split())) for line in lines]
            
            # If successful, save it properly
            save_seats(temp_seats)
        except ValueError:
            print("Invalid file format uploaded.")
            
    return redirect(url_for('index'))

@app.route('/reset')
def reset_seats():
    """Resets all seats to vacant (0)."""
    seats = load_seats()
    new_seats = [[0 for _ in row] for row in seats]
    save_seats(new_seats)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

