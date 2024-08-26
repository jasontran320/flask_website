from flask import request, jsonify
from config import app, db
from models import Friend

@app.route("/api/friends", methods=["GET"])
def get_friends():
    friends = Friend.query.all() #Similar to SELECT * FROM friends. Returns a list
    result = [friend.to_json() for friend in friends]#decouples list into json
    return jsonify(result)

#create friend
@app.route("/api/friends", methods=["POST"])
def create_friend():
    try:
        data = request.json#request receieved

        required_fields = ["name", "role", "description", "gender"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        name = data.get("name")
        role = data.get("role")
        description = data.get("description")
        gender = data.get("gender")
        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        new_friend = Friend(name=name, role=role, 
                            description=description,
                            gender=gender, 
                            img_url=img_url)
        db.session.add(new_friend)#stage this change
        db.session.commit()
        return jsonify({"mgs": "friend created successfully"}), 201#POST must return both of these
    except Exception as e:
        db.session.rollback()#Returns db to previous state
        return jsonify({"error": str(e)}), 500

#Delete
@app.route("api/friends/<int:id>", methods=["DELETE"])#how to pass dynamic info
def delete_friend(id):
    try:
        friend = Friend.query.get(id)
        if friend is None:
            return jsonify({"error": "Friend not found"}), 404
        db.session.delete(friend)
        db.session.commit()
        return jsonify({"msg": "Friend deleted"}), 200
    except Exception as e:
        db.session.rollback()#Rollback to previous state since something unexpected happen
        return jsonify({"error":str(e)}), 500

#Update a friend profile
@app.route("api/friends/<int:id>", methods=["PATCH"])#how to pass dynamic info
def update_friend(id):    
    try:
        friend = Friend.query.get(id)#You get to modify this directly?
        if friend is None:
            return jsonify({"error": "Friend not found"}), 404
        data = request.json
        friend.name = data.get("name", friend.name)#default to friend.name
        friend.role = data.get("role", friend.role)
        friend.description = data.get("description", friend.description)
        friend.gender = data.get("gender", friend.gender)
        db.session.commit(friend.to_json()), 200

    except Exception as e:
        db.session.rollback()#Rollback to previous state since something unexpected happen
        return jsonify({"error":str(e)}), 500

if __name__ == "__main__":
    with app.app_context(): 
        db.create_all()#Creates the tables specified
    app.run(debug=True, use_reloader=True)