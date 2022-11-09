from flask import request, jsonify
from __main__ import app,db
from invokes import invoke_http


class Positions(db.Model):
    __tablename__ = 'Positions'

    Position_Name = db.Column(db.String(50), primary_key=True)

    def __init__(self, Position_Name):
        if not isinstance(Position_Name, str):
            raise TypeError("Position_Name must be a string")
        self.Position_Name = Position_Name

    def json(self):
        return {"Position_Name": self.Position_Name}

@app.route("/positions")
def position_get_all():
    position_list = Positions.query.all()
    if position_list:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "positions": [position.json() for position in position_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no Positions."
        }
    ), 404

@app.route("/get_position_by_name/<Position_Name>")
def get_position_by_name(Position_Name):
    position = Positions.query.filter_by(Position_Name=Position_Name).first()
    if position:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "Positions": [position.json()]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Position is not found. Please double check."
        }
    ), 404

@app.route("/get_position/<Position_Name>")
def get_position(Position_Name):
    position_list = Positions.query.filter_by(Position_Name=Position_Name)
    if position_list:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "Positions": [position.json() for position in position_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Position is not found. Please double check."
        }
    ), 404

@app.route("/create_new_position/<string:new_position>", methods=['POST'])
def create_new_position(new_position):
    if (Positions.query.filter_by(Position_Name=new_position).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "Position_Name": new_position
                },
                "message": "Position already exists."
            }
        ), 400

    data = request.get_json()
    position = Positions(**data)

    try:
        db.session.add(position)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "Position_Name": position
                },
                "message": "An error occurred creating the Position."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": position.json()
        }
    ), 201


@app.route("/position/update", methods=['POST'])
def update_position_name():

    data = request.get_json()
    old_position_name=data['Current_Name']
    new_position_name=data['New_Name']
       
    result=Positions.query.filter_by(Position_Name=old_position_name).update({'Position_Name': new_position_name})
    db.session.commit()
    if result:
        return jsonify(
            {
                "code": 200,
                "old_position": old_position_name ,
                "current_position":new_position_name
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Position is not found. Please double check."
        }
    ), 404

@app.route("/position/delete", methods=['POST'])
def delete_position():

    data = request.get_json()
    position=data['Delete']
    #new_position_name=data['New_Name']
    res=Positions.query.filter_by(Position_Name=position).delete()
    db.session.commit()
    if res:
        return jsonify(
            {
                "code": 200,
                "deleted_position": res 
                
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Position is not found. Please double check."
        }
    ), 404