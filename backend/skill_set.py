from flask import jsonify, request
from __main__ import app,db
#from app import app,db

class Skill_Set(db.Model):
    __tablename__ = 'Skill_Set'

    Skill_Set_ID = db.Column(db.Integer, primary_key=True)
    Skill_Name = db.Column(
        db.String(50), db.ForeignKey('Skill.Skill_Name'))
    Position_Name = db.Column(
        db.String(50), db.ForeignKey('Positions.Position_Name'))
    

    def __init__(self, Skill_Name, Position_Name):
        if not isinstance(Skill_Name, str):
            raise TypeError("Skill_Name must be a string")
        if not isinstance(Position_Name, str):
            raise TypeError("Position_Name must be a string")
        self.Skill_Name = Skill_Name
        self.Position_Name = Position_Name

    def json(self):
        return {"Skill_Set_ID": self.Skill_Set_ID, 
                "Skill_Name": self.Skill_Name, 
                "Position_Name": self.Position_Name}

@app.route("/skill_set")  # get all skill sets
def get_all():
    skill_set = Skill_Set.query.all()
    if len(skill_set):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "skill_set": [skill.json() for skill in skill_set]
                }
            }
        )
    else:
        return jsonify({
            "message": "Skill set not found."
        }), 404

@app.route("/skill_set/<Position_Name>")  # get skills by Position_Name
def get_skills_by_position(Position_Name):
    skill_set_list = Skill_Set.query.filter_by(Position_Name=Position_Name).all()

    if skill_set_list:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "Skill_Set": [skill_set.json() for skill_set in skill_set_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Position name is not found. Please double check."
        }
    ), 404

@app.route("/skill_set/get_position/<Skill_Name>")  # get positions by Skill_Name
def get_positions_by_skill(Skill_Name):
    skill_set_list = Skill_Set.query.filter_by(Skill_Name=Skill_Name).all()

    if skill_set_list:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "Skill_Set": [skill_set.json() for skill_set in skill_set_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Skill Name is not found. Please double check."
        }
    ), 404

@app.route("/create_new_skillset", methods=['POST']) # create skillset 
def create_new_skillset():

    data = request.get_json()
    if (Skill_Set.query.filter_by(Position_Name=data["Position_Name"], Skill_Name=data["Skill_Name"]).first()):
        return jsonify(
            {
                "code": 400,
                "data": data,
                "message": "A skillset with the same ID already exists."
            }
        ), 400

    #print(data)
    skillset = Skill_Set(**data)
    #print(skillset)
    try:
        db.session.add(skillset)
        db.session.commit()
    except Exception as e:
        print(e,'================================================')
        return jsonify(
            {
                "code": 500,
                "data": {
                    "New_SkillSet": data
                },
                "message": "An error occurred while creating the skillset."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": skillset.json()
        }
    ), 201

@app.route("/delete_skillset", methods=['POST']) # create skillset 
def delete_skillset():

    data = request.get_json()
    try:
        res = Skill_Set.query.filter_by(Position_Name=data["Position_Name"], Skill_Name=data["Skill_Name"]).delete()
        db.session.commit()
        if res:
            return jsonify(
                {
                    "code": 200,
                    "deleted_position": res 
                }
            ), 200
    except Exception as e:
        print(e,'================================================')
        return jsonify(
            {
                "code": 500,
                "data": {
                    "New_SkillSet": data
                },
                "message": "An error occurred while deleting the skillset."
            }
        ), 500



@app.route("/update_skillset_same_position", methods=['POST']) # update skillset WITH CONSTANT POSITION NAME
def update_skillset_same_position():

    data = request.get_json()
    print (data,'=============================================================================')
    position=data['Position_Name']
    to_add=data['Skills_To_Add']
    to_delete=data['Skills_To_Delete']
    
    try:
        for item in to_delete :
            Skill_Set.query.filter_by(Skill_Name=item,Position_Name=position).delete()
            db.session.commit()
        for item in to_add:
            data={
                "Skill_Name": item,
                "Position_Name": position
            }
            skillset = Skill_Set(**data)
            db.session.add(skillset)
            db.session.commit()
        skill_set_list = Skill_Set.query.filter_by(Position_Name=position)
    
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the skillset."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "message":"skills successfully updated!",
            "new skills":[skill_set.json() for skill_set in skill_set_list]
        }
    ), 201

@app.route("/update_skillset_same_skill", methods=['POST']) # update skillset WITH CONSTANT SKILL NAME
def update_skillset_same_skill():

    data = request.get_json()
    print (data,'=============================================================================')
    skill=data['Skill_Name']
    to_add=data['Positions_Add']
    to_delete=data['Positions_Delete']
    
    try:
        for item in to_delete :
            Skill_Set.query.filter_by(Position_Name=item, Skill_Name=skill).delete()
            db.session.commit()
            print('================ delete skillset successful ==========')
        for item in to_add:
            data={
                "Skill_Name": skill,
                "Position_Name": item
            }
            skillset = Skill_Set(**data)
            db.session.add(skillset)
            db.session.commit()
            print('================ create new skillset successful ==========')
        skill_set_list = Skill_Set.query.filter_by(Skill_Name = skill)
    
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the skillset."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "message":"skills successfully updated!",
            "new skills":[skill_set.json() for skill_set in skill_set_list]
        }
    ), 201