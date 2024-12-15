from flask import Flask, request, jsonify, session, send_file
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS
from config import ApplicationConfig
from models import db, User
import io

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
CORS(app, supports_credentials=True)

bcrypt = Bcrypt(app)
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()
    
    
# AUTHENTICATION ROUTES #

@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({"error": "Unauthorized Login"}), 401
    
    user = User.query.filter_by(id = user_id).first()
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })

@app.route("/register", methods=["POST"])
def register_user():
    
    # Get Inputs from form data
    
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]
    
    # Check if user exist in the database
    
    user_exists = User.query.filter_by(email=email).first() is not None
    
    if user_exists:
        return jsonify({"error": "User already exists in the Database"}), 409
    
    # Adding User to the Database TANGINAMAAMAYOKONA
    
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    session["user_id"] = new_user.id
    return jsonify ({
        "id": new_user.id,
        "email": new_user.email,
        "username": new_user.username
    })
    
    
@app.route("/login", methods=["POST"])
def login_user():
    
    # Get Inputs from the form data - frontend
    
    username = request.json["username"]
    password = request.json["password"]
    
    # Check if user exist in the db
    user = User.query.filter_by(username=username).first()
    
    # Return unauthorized error if user doesnt exist
    
    if user is None:
        return jsonify({"error": "Unauthorized Login"}), 401
    
    # Check if password is same to the hashed password
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized Login"}), 401
    
    session["user_id"] = user.id
    
    return jsonify({
        "id": user.id,
        "username": user.username
        
    })
    
    
    

@app.route("/logout", methods=["POST"])
def logout_user():
    
    # Check if user_id is in session, pop if there is
    if "user_id" in session:
        session.pop("user_id")
    
    return jsonify({"message": "Logged Out Succesfull"}), 200



@app.route("/generate-cobol-file", methods=["POST"])
def generate_cobol_file():
    # Get the transaction data from the frontend
    transactions = request.json.get("transactions", [])
    
    if not isinstance(transactions, list):
        return "Invalid data format", 400
    
    # Start the COBOL output string
    cobol_output = "COBOL Report\n====================\n"
    
    # Iterate over the transactions and build the COBOL print structure
    for index, tx in enumerate(transactions):
        removed_status = " (REMOVED)" if tx.get("removed") else ""
        cobol_output += f"Transaction {index + 1}{removed_status}\n"
        cobol_output += f"Type: {tx.get('type', 'N/A').upper()}\n"
        cobol_output += f"Category: {tx.get('category', 'N/A')}\n"
        cobol_output += f"Amount: {tx.get('amount', 'N/A')} {tx.get('currency', 'N/A')}\n"
        cobol_output += f"====================\n"
    
    # Create a bytes buffer to simulate a file (you can save it to a physical file as well)
    cobol_file = io.BytesIO()
    cobol_file.write(cobol_output.encode('utf-8'))
    cobol_file.seek(0)  # Move the cursor to the start of the file
    
    # Return the file as a downloadable response
    return send_file(
        cobol_file, as_attachment=True, 
        download_name="transaction_report.txt", mimetype='text/plain'
    )



# CRUD ROUTES #
    

# Run 
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)