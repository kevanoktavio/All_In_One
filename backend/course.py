from flask import jsonify
from __main__ import app,db

class Course(db.Model):
    __tablename__ = 'Course'

    Course_ID = db.Column(db.String(50), primary_key=True)
    Course_Name = db.Column(db.String(32), nullable=False)
    Course_Desc = db.Column(db.String(32), nullable=False)
    Course_Status = db.Column(db.String(32), nullable=False)
    Course_Type = db.Column(db.String(32), nullable=False)
    Course_Category = db.Column(db.String(32), nullable=False)

    def __init__(self, Course_ID, Course_Name, Course_Desc, Course_Status, Course_Type, Course_Category):
        self.Course_ID = Course_ID
        self.Course_Name = Course_Name
        self.Course_Desc = Course_Desc
        self.Course_Status = Course_Status
        self.Course_Type = Course_Type
        self.Course_Category = Course_Category

    def json(self):
        dto = {
            'Course_ID': self.Course_ID,
            'Course_Name': self.Course_Name,
            'Course_Desc': self.Course_Desc,
            'Course_Status': self.Course_Status,
            'Course_Type': self.Course_Type,
            'Course_Category': self.Course_Category
        }
        return dto 


#role_database = invoke_http(route_dict["role"] , method='GET')
@app.route("/course")
def course_get_all():
    course_list = Course.query.all()
    
    if course_list:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "courses": [course.json() for course in course_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no Courses."
        }
    ), 404


@app.route("/course/name/<string:course_name>", methods=['GET'])
def course_get_by_name(course_name):
    course_data = Course.query.filter_by(Course_Name = course_name).first()
    if course_data:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "courses": course_data.json()
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": 'No course named ' +str(course_name) 
        }
    ), 404

@app.route("/course/id/<string:course_id>", methods=['GET'])
def get_course_by_course_id(course_id):
    course = Course.query.filter_by(Course_ID = course_id).first()
    if course:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "course": course.json()
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": str(course_id) + " id not found."
        }
    ), 404

