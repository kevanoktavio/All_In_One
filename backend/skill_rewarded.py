from flask import jsonify,request
from __main__ import app,db
#from app import app,db

class Skill_Rewarded(db.Model):
    __tablename__ = 'Skill_Rewarded'

    Skill_Rewarded_ID = db.Column(db.Integer, primary_key=True)
    Skill_Name = db.Column(
        db.String(50), db.ForeignKey('Skill.Skill_Name'))
    Course_ID = db.Column(
        db.String(20), db.ForeignKey('Course.Course_ID'))

    def __init__(self, Skill_Name, Course_ID):
        if not isinstance(Skill_Name, str):
            raise TypeError("Skill_Name must be a string")
        if not isinstance(Course_ID, str):
            raise TypeError("Course_ID must be an string")
        self.Skill_Name = Skill_Name
        self.Course_ID = Course_ID

    def json(self):
        return {"Skill_Rewarded_ID": self.Skill_Rewarded_ID, 
                "Skill_Name": self.Skill_Name, 
                "Course_ID": self.Course_ID}

@app.route("/view_course_skills/get_skill/<Course_ID>")
def view_course_skills(Course_ID):
    skill_rewarded_list = Skill_Rewarded.query.filter_by(Course_ID=Course_ID).all()
    if skill_rewarded_list:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "Skill_Rewarded": [skill_rewarded.json() for skill_rewarded in skill_rewarded_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Course ID is not found. Please double check."
        }
    ), 404

@app.route("/view_course_skills/get_course/<Skill_Name>")
def view_course_by_skill_name(Skill_Name):
    skill_rewarded_list = Skill_Rewarded.query.filter_by(Skill_Name=Skill_Name).all()
    if skill_rewarded_list:
        return jsonify(
                {
                    "code": 200,
                    "data": {
                        "Skill_Rewarded": [skill_rewarded.json() for skill_rewarded in skill_rewarded_list]
                    }
                }
        )
    
    return jsonify(
            {
                "code": 404,
                "message": "No course is associated"
            }
        ), 404

@app.route("/create_new_skill_rewarded", methods=['POST']) # create skillset 
def create_new_skill_rewarded():

    data = request.get_json()
    if (Skill_Rewarded.query.filter_by(Course_ID=data["Course_ID"], Skill_Name=data["Skill_Name"]).first()):
        return jsonify(
            {
                "code": 400,
                "data": data,
                "message": "A skill rewarded with the same ID already exists."
            }
        ), 400

    print(data)
    skill_rewarded = Skill_Rewarded(**data)
    print(skill_rewarded)
    try:
        db.session.add(skill_rewarded)
        db.session.commit()
    except Exception as e:
        print(e,'================================================')
        return jsonify(
            {
                "code": 500,
                "data": {
                    "New_Skill_Rewarded": data
                },
                "message": "An error occurred while creating the skill_rewarded"})
    return jsonify(
        {
            "code": 201,
            "data": skill_rewarded.json()
        }
    ), 201

                
@app.route("/delete_skill_rewarded", methods=['POST']) # create skillset 
def delete_skill_rewarded():

    data = request.get_json()
    try:
        res = Skill_Rewarded.query.filter_by(Course_ID=data["Course_ID"], Skill_Name=data["Skill_Name"]).delete()
        db.session.commit()
        if res:
            return jsonify(
                {
                    "code": 200,
                    "message": "Skill is no longer associated with the course."
                }
            ), 200
    except Exception as e:
        print(e,'================================================')
        return jsonify(
            {
                "code": 500,
                "data": {
                    "Skillset to Delete": data
                },
                "message": "An error occurred while deleting the skillset."
            }
        ), 500





@app.route("/update_skill_rewarded", methods=['POST']) # create skillset 
def update_skill_rewarded():

    data = request.get_json()

    course_id=data['course_id']
    to_add=data['add']
    to_delete=data['delete']
 
    try:
        for item in to_add:
            data={"Skill_Name":item,"Course_ID":course_id}
            skill_rewarded = Skill_Rewarded(**data)
            db.session.add(skill_rewarded)
            db.session.commit()
        for item in to_delete :
            Skill_Rewarded.query.filter_by(Skill_Name=item,Course_ID=course_id).delete()
            db.session.commit()
        skill_rewarded_list = Skill_Rewarded.query.filter_by(Course_ID=course_id)   
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
            "new skills":[skill_rewarded.json() for skill_rewarded in skill_rewarded_list]
        }
    ), 201

@app.route("/update_skill_rewarded_same_skill", methods=['POST']) # update skill rewarded WITH CONSTANT SKILL NAME
def update_skill_rewarded_same_skill():

    data = request.get_json()
    print (data,'=============================================================================')
    skill=data['Skill_Name']
    to_add=data['Courses_Add']
    to_delete=data['Courses_Delete']
    
    try:
        for item in to_delete :
            Skill_Rewarded.query.filter_by(Course_ID=item, Skill_Name=skill).delete()
            db.session.commit()
        print('================ delete skill rewarded successful ==========')
        for item in to_add:
            data={
                "Skill_Name": skill,
                "Course_ID": item
            }
            skill_rewarded = Skill_Rewarded(**data)
            db.session.add(skill_rewarded)
            db.session.commit()
        print('================ create new skillset successful ==========')
        skill_rewarded_list = Skill_Rewarded.query.filter_by(Skill_Name = skill)
    
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the skill rewarded."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "message":"skill_rewarded successfully updated!",
            "new skills":[skill_rewarded.json() for skill_rewarded in skill_rewarded_list]
        }
    ), 201
     