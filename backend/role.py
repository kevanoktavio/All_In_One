from flask import jsonify
from __main__ import app,db

class Role(db.Model):
    __tablename__ = 'Role'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), nullable=False)

    def __init__(self, role_id, role_name):
        self.role_id = role_id
        self.role_name = role_name

    def json(self):
        dto = {
            'role_id': self.role_id,
            'role_name': self.role_name
        }

        return dto

# Method
@app.route("/role")
def role_get_all():
    role_list = Role.query.all()
    if len(role_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "roles": [role.json() for role in role_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no Roles."
        }
    ), 404
