from flask import request, jsonify
from __main__ import app,db
#from app import app,db

class Skill(db.Model):
    __tablename__ = 'Skill'
    
    Skill_Name = db.Column(db.String(50), primary_key=True)

    def __init__(self, Skill_Name):
        if not isinstance(Skill_Name, str):
            raise TypeError("Skill_Name must be a string")
        self.Skill_Name = Skill_Name

    def json(self):
        return {"Skill_Name": self.Skill_Name}

@app.route("/skill")  # get all skill
def skill_get_all():
    skills = Skill.query.all()
    if len(skills):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "skill": [skill.json() for skill in skills]
                }
            }
        )
    else:
        return jsonify({
            "message": "Skills not found."
        }), 404

@app.route("/skill/name/<string:name>", methods=['GET']) # search skill by name using wildcard
def skill_get_by_name(name):
    skill_data = Skill.query.filter(Skill.Skill_Name.like('%' + name + '%')).all()
    if skill_data:
        return jsonify(
            {
                "code": 200,
                "data": {
                    # "skills": skill_data
                    "skills": [skill.json() for skill in skill_data]
                }
            }
        ), 200
    return jsonify (
        {
            "code": 404,
            "message": 'No skill named ' + str(name) 
        }
    ), 404

@app.route("/skill/delete/<string:skill_name>", methods=["DELETE"]) #delete skill by name
def skill_delete_by_name(skill_name):
    # if skill doesnt exist
    if not (Skill.query.filter_by(Skill_Name=skill_name).first()):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "Skill_Name": skill_name
                },
                "message": "Skill does not exist"
            }
        ), 404
    # if skill exists
    try:
        # Skill.query.filter_by(Skill_Name = skill_name).delete()
        result = Skill.query.filter_by(Skill_Name = skill_name).first()
        db.session.delete(result)
        db.session.commit()
        return('success')
    except Exception as e: print(e)
    return('error')
    # except:    
    #     return jsonify(
    #             {
    #                 "code": 500,
    #                 "data": {
    #                     "Skill_Name": skill_name
    #                 },
    #                 "message": "An error occurred while deleting the Skill."
    #             }
    #         ), 500

    # return jsonify(
    #     {
    #         "code": 200,
    #         "data": skill_name
    #     }
    # ), 200

@app.route("/skill/create", methods=['POST']) #add new skill
def create_new_skill():
    data = request.get_json()
    Skill_Name = data['Skill_Name']

    # If skill name already exists
    if (Skill.query.filter_by(Skill_Name=Skill_Name).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "Skill_Name": Skill_Name
                },
                "message": "Skill already exists."
            }
        ), 400

    # Create skill record
    skill = Skill(
        Skill_Name=Skill_Name
    )
    # return Skill_Name
    try:
        db.session.add(skill)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "Skill_Name": skill
                },
                "message": "An error occurred creating the Skill."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": skill.json()
        }
    ), 201

@app.route("/skill/update", methods=['POST']) # Update skill name
def update_skill_name():

    data = request.get_json()
    Old_Skill_Name=data['Old_Skill_Name']
    New_Skill_Name=data['New_Skill_Name']

    if Old_Skill_Name == New_Skill_Name:
        return jsonify(
            {
                "code": 400,
                "message": "Old and new skill name is the same"
            }
        )
       
    result=Skill.query.filter_by(Skill_Name=Old_Skill_Name).update({'Skill_Name': New_Skill_Name})
    db.session.commit()
    if result:
        return jsonify(
            {
                "code": 200,
                "message": Old_Skill_Name +" has been changed to " + New_Skill_Name
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Skill is not found. Please double check."
        }
    ), 404