from app import app, db
from flask import request, jsonify
from models import Friend, usersdata, UserCardAccess

# Get all friends


@app.route("/api/friends", methods=["GET"])
def get_friends():
    friends = Friend.query.all()
    result = [friend.to_json() for friend in friends]
    return jsonify(result)

# Create a friend (with access control)


@app.route("/api/friends", methods=["POST"])
def create_friend():
    try:
        data = request.json

        # Validations
        required_fields = ["name", "role", "description", "gender"]
        for field in required_fields:
            if field not in data or not data.get(field):
                return jsonify({"error": f'Missing required field: {field}'}), 400

        name = data["name"]
        role = data["role"]
        description = data["description"]
        gender = data["gender"]
        # List of emails with access
        allowed_emails = data.get("allowedEmails", [])

        # Fetch avatar image based on gender
        img_url = None
        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"

        # Create the card
        new_friend = Friend(
            name=name, role=role, description=description, gender=gender, img_url=img_url)
        db.session.add(new_friend)
        db.session.commit()

        # Store access permissions in `user_card_access`
        for email in allowed_emails:
            user_exists = usersdata.query.filter_by(email=email).first()
            if user_exists:  # Only store if user exists
                user_access = UserCardAccess(
                    card_id=new_friend.id, user_email=email)
                db.session.add(user_access)

        db.session.commit()
        return jsonify(new_friend.to_json()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Delete a friend


@app.route("/api/friends/<int:id>", methods=["DELETE"])
def delete_friend(id):
    try:
        friend = Friend.query.get(id)
        if not friend:
            return jsonify({"error": "Friend not found"}), 404

        db.session.delete(friend)
        db.session.commit()
        return jsonify({"msg": "Friend deleted"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Update a friend profile


@app.route("/api/friends/<int:id>", methods=["PATCH"])
def update_friend(id):
    try:
        friend = Friend.query.get(id)
        if not friend:
            return jsonify({"error": "Friend not found"}), 404

        data = request.json
        friend.name = data.get("name", friend.name)
        friend.role = data.get("role", friend.role)
        friend.description = data.get("description", friend.description)
        friend.gender = data.get("gender", friend.gender)

        db.session.commit()
        return jsonify(friend.to_json()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get all user emails (for dropdown)


@app.route("/api/friends/emails", methods=["GET"])
def get_user_emails():
    users = usersdata.query.with_entities(usersdata.email).all()
    email_list = [user.email for user in users]
    return jsonify(email_list), 200

# Get users with access to a specific card


@app.route("/api/friends/access/<int:card_id>", methods=["GET"])
def get_card_access_users(card_id):
    access_records = UserCardAccess.query.filter_by(card_id=card_id).all()
    emails = [record.user_email for record in access_records]
    return jsonify({"card_id": card_id, "allowed_users": emails}), 200

# User Login


@app.route("/api/friends/login", methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = usersdata.query.filter_by(email=email, password=password).first()

    if user:
        return jsonify({'message': 'Login successful', 'status': 'success'}), 200
    else:
        return jsonify({'message': 'Invalid credentials', 'status': 'fail'}), 401

# Get all users (Signup list)


@app.route("/api/friends/signup", methods=["GET"])
def get_users():
    users = usersdata.query.all()
    result = [user.to_json() for user in users]
    return jsonify(result)

# Register new user


@app.route("/api/friends/signup", methods=["POST"])
def post_users():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        # Check if user already exists
        existing_user = usersdata.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "Email already registered"}), 400

        # Create new user
        new_user = usersdata(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully", "status": "success"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
