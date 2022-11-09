from flask import jsonify
from __main__ import app,db
#from app import app,db


class Registration(db.Model):
    __tablename__ = 'Registration'

    reg_id = db.Column(db.Integer, primary_key=True)
    reg_status = db.Column(db.String(32), nullable=False)
    completion_status = db.Column(db.String(32), nullable=False)
    course_id = db.Column(db.String(32), nullable=False)
    staff_id = db.Column(db.Integer, nullable=False)

    def __init__(self, reg_id, reg_status, completion_status, course_id, staff_id):
        self.reg_id = reg_id
        self.reg_status = reg_status
        self.completion_status = completion_status
        self.course_id = course_id
        self.staff_id = staff_id

    def json(self):
        dto = {
            'reg_id': self.reg_id,
            'reg_status': self.reg_status,
            'completion_status': self.completion_status,
            'course_id': self.course_id,
            'staff_id': self.staff_id
        }

        return dto

@app.route("/registration")
def registration_get_all():
    registration_list = Registration.query.all()
    if len(registration_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "registrations": [registration.json() for registration in registration_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no registrations."
        }
    ), 404
