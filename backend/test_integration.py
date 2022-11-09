import unittest
from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
import flask_testing
import json


app = Flask(__name__)
db = SQLAlchemy(app)


class TestApp(flask_testing.TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


from course import Course

class TestCourse(TestApp):
    def test_course_get_empty_course(self):

        response = self.client.get("/course")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
        {
            "code": 404,
            "message": "There are no Courses."
        }
        ).data, 404)

    def test_course_get_all(self):
        db.session.add(Course('IS212', 'Software Project Management', 'Learn Agile', 'Active', 'External', 'Management'))
        db.session.add(Course('SAL001', 'Risk Management for Smart Business', 'Apply risk management concepts to digital business', 'Retired', 'Internal', 'Sales'))
        db.session.add(Course('COR006', 'Manage Change', 'Identify risks associated with change and develop risk mitigation plans.', 'Retired', 'External', 'Core'))
        db.session.commit()
        response = self.client.get("/course")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "courses": [
                {
                    'Course_ID': 'IS212',
                    'Course_Name': 'Software Project Management',
                    'Course_Desc': 'Learn Agile',
                    'Course_Status': 'Active',
                    'Course_Type': 'External',
                    'Course_Category': 'Management'
                },
                {
                    'Course_ID': 'SAL001',
                    'Course_Name': 'Risk Management for Smart Business',
                    'Course_Desc': 'Apply risk management concepts to digital business',
                    'Course_Status': 'Retired',
                    'Course_Type': 'Internal',
                    'Course_Category': 'Sales'
                },
                {
                    'Course_ID': 'COR006',
                    'Course_Name': 'Manage Change',
                    'Course_Desc': 'Identify risks associated with change and develop risk mitigation plans.',
                    'Course_Status': 'Retired',
                    'Course_Type': 'External',
                    'Course_Category': 'Core'
                }
                ]
            }
            }
        ).data)

    def test_course_get_by_name(self):
        db.session.add(Course('IS212', 'Software Project Management', 'Learn Agile', 'Active', 'External', 'Management'))
        db.session.add(Course('SAL001', 'Risk Management for Smart Business', 'Apply risk management concepts to digital business', 'Retired', 'Internal', 'Sales'))
        db.session.add(Course('COR006', 'Manage Change', 'Identify risks associated with change and develop risk mitigation plans.', 'Retired', 'External', 'Core'))
        db.session.commit()
        response = self.client.get("/course/name/Software Project Management")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "courses": 
                {
                    'Course_ID': 'IS212',
                    'Course_Name': 'Software Project Management',
                    'Course_Desc': 'Learn Agile',
                    'Course_Status': 'Active',
                    'Course_Type': 'External',
                    'Course_Category': 'Management'
                },
            }
            }
        ).data)
    
    def test_course_get_by_non_existing_name(self):
        db.session.add(Course('IS212', 'Software Project Management', 'Learn Agile', 'Active', 'External', 'Management'))
        db.session.add(Course('SAL001', 'Risk Management for Smart Business', 'Apply risk management concepts to digital business', 'Retired', 'Internal', 'Sales'))
        db.session.add(Course('COR006', 'Manage Change', 'Identify risks associated with change and develop risk mitigation plans.', 'Retired', 'External', 'Core'))
        db.session.commit()

        response = self.client.get("/course/name/Engineering")

        #print(response.data)
        self.assertEqual(response.data, jsonify(
        {
            "code": 404,
            "message": 'No course named Engineering'
        }
        ).data)

    def test_get_course_by_course_id(self):
        db.session.add(Course('IS212', 'Software Project Management', 'Learn Agile', 'Active', 'External', 'Management'))
        db.session.add(Course('SAL001', 'Risk Management for Smart Business', 'Apply risk management concepts to digital business', 'Retired', 'Internal', 'Sales'))
        db.session.add(Course('COR006', 'Manage Change', 'Identify risks associated with change and develop risk mitigation plans.', 'Retired', 'External', 'Core'))
        db.session.commit()

        response = self.client.get("/course/id/IS212")

        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "course": 
                {
                    'Course_ID': 'IS212',
                    'Course_Name': 'Software Project Management',
                    'Course_Desc': 'Learn Agile',
                    'Course_Status': 'Active',
                    'Course_Type': 'External',
                    'Course_Category': 'Management'
                },
            }
            }
        ).data)
    
    def test_get_course_by_wrong_course_id(self):
        db.session.add(Course('IS212', 'Software Project Management', 'Learn Agile', 'Active', 'External', 'Management'))
        db.session.add(Course('SAL001', 'Risk Management for Smart Business', 'Apply risk management concepts to digital business', 'Retired', 'Internal', 'Sales'))
        db.session.add(Course('COR006', 'Manage Change', 'Identify risks associated with change and develop risk mitigation plans.', 'Retired', 'External', 'Core'))
        db.session.commit()

        response = self.client.get("/course/id/IS213")

        self.assertEqual(response.data, jsonify(
        {
            "code": 404,
            "message": "IS213 id not found."
        }
    ).data)

from learning_journey import LearningJourney
from staff import Staff
from positions import Positions
from skill import Skill
from course import Course

class TestLearningJourney(TestApp): 

    def test_get_empty_learning_journey(self):
        response = self.client.get("/get_learning_journey")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
        {
            "code": 404,
            "message": "There are no Learning Journey."
        }
        ).data)

    def test_get_learning_journey(self):
        db.session.add(LearningJourney(130001, 'Human Resource Manager', 'Public Speaking', 'MGT001'))
        db.session.add(LearningJourney(130001, 'Data Analyst', 'Python', 'FIN001'))
        db.session.add(LearningJourney(130002, 'Data Analyst', 'Python', 'FIN001'))
        db.session.add(Staff(130001, 'John', 'Sim', 'Chairman', 'john.sim@allinone.com.sg', 1))
        db.session.add(Staff(130002, 'Jack', 'Sim', 'CEO', 'jack.sim@allinone.com.sg', 1))
        db.session.add(Staff(140001, 'Derek', 'Tan', 'Sales', 'Derek.Tan@allinone.com.sg', 3))
        db.session.add(Positions('Human Resource'))
        db.session.add(Positions('Data Analyst'))
        db.session.add(Skill('Public Speaking'))
        db.session.add(Skill('Python'))
        db.session.add(Course('MGT001', 'Agile Leadership', 'Learn Agile leadership', 'Active', 'External', 'Management'))
        db.session.add(Course('FIN001', 'Analytics Foundation', 'Learn pandas framework', 'Retired', 'Internal', 'Analytics'))
        db.session.commit()

        response = self.client.get("/get_learning_journey")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "lj": [
                {
                    "Learning_Journey_ID":1,
                    "Staff_ID": 130001,
                    "Position_Name": 'Human Resource Manager',
                    "Skill_Name": 'Public Speaking',
                    "Course_ID": 'MGT001'
                },
                {
                    "Learning_Journey_ID":2,
                    "Staff_ID": 130001,
                    "Position_Name": 'Data Analyst',
                    "Skill_Name": 'Python',
                    "Course_ID": 'FIN001'
                },
                {
                    "Learning_Journey_ID":3,
                    "Staff_ID": 130002,
                    "Position_Name": 'Data Analyst',
                    "Skill_Name": 'Python',
                    "Course_ID": 'FIN001'
                }
                ]
            }
            }
        ).data)

    def test_get_learning_journey_by_staff_id(self):
        db.session.add(LearningJourney(130001, 'Human Resource Manager', 'Public Speaking', 'MGT001'))
        db.session.add(LearningJourney(130001, 'Data Analyst', 'Python', 'FIN001'))
        db.session.add(LearningJourney(130002, 'Data Analyst', 'Python', 'FIN001'))
        db.session.add(Staff(130001, 'John', 'Sim', 'Chairman', 'john.sim@allinone.com.sg', 1))
        db.session.add(Staff(130002, 'Jack', 'Sim', 'CEO', 'jack.sim@allinone.com.sg', 1))
        db.session.add(Staff(140001, 'Derek', 'Tan', 'Sales', 'Derek.Tan@allinone.com.sg', 3))
        db.session.add(Positions('Human Resource'))
        db.session.add(Positions('Data Analyst'))
        db.session.add(Skill('Public Speaking'))
        db.session.add(Skill('Python'))
        db.session.add(Course('MGT001', 'Agile Leadership', 'Learn Agile leadership', 'Active', 'External', 'Management'))
        db.session.add(Course('FIN001', 'Analytics Foundation', 'Learn pandas framework', 'Retired', 'Internal', 'Analytics'))
        db.session.commit()

        response = self.client.get("/get_learning_journey_by_staff_id/130001")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "lj": [
                {
                    "Learning_Journey_ID":1,
                    "Staff_ID": 130001,
                    "Position_Name": 'Human Resource Manager',
                    "Skill_Name": 'Public Speaking',
                    "Course_ID": 'MGT001'
                },
                {
                    "Learning_Journey_ID":2,
                    "Staff_ID": 130001,
                    "Position_Name": 'Data Analyst',
                    "Skill_Name": 'Python',
                    "Course_ID": 'FIN001'
                }
                ]
            }
            }
        ).data)

    def test_get_learning_journey_by_staff_id_with_no_lj(self):
        db.session.add(LearningJourney(130001, 'Human Resource Manager', 'Public Speaking', 'MGT001'))
        db.session.add(LearningJourney(130001, 'Data Analyst', 'Python', 'FIN001'))
        db.session.add(LearningJourney(130002, 'Data Analyst', 'Python', 'FIN001'))
        db.session.add(Staff(130001, 'John', 'Sim', 'Chairman', 'john.sim@allinone.com.sg', 1))
        db.session.add(Staff(130002, 'Jack', 'Sim', 'CEO', 'jack.sim@allinone.com.sg', 1))
        db.session.add(Staff(140001, 'Derek', 'Tan', 'Sales', 'Derek.Tan@allinone.com.sg', 3))
        db.session.add(Positions('Human Resource'))
        db.session.add(Positions('Data Analyst'))
        db.session.add(Skill('Public Speaking'))
        db.session.add(Skill('Python'))
        db.session.add(Course('MGT001', 'Agile Leadership', 'Learn Agile leadership', 'Active', 'External', 'Management'))
        db.session.add(Course('FIN001', 'Analytics Foundation', 'Learn pandas framework', 'Retired', 'Internal', 'Analytics'))
        db.session.commit()

        response = self.client.get("/get_learning_journey_by_staff_id/140001")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
        {
            "code": 404,
            "message": "140001 has no Learning Journey."
        }
        ).data)


    def test_get_learning_journey_by_lj_id(self):
        db.session.add(LearningJourney(130001, 'Human Resource Manager', 'Public Speaking', 'MGT001'))
        db.session.add(LearningJourney(130001, 'Data Analyst', 'Python', 'FIN001'))
        db.session.add(LearningJourney(130002, 'Data Analyst', 'Python', 'FIN001'))
        db.session.add(Staff(130001, 'John', 'Sim', 'Chairman', 'john.sim@allinone.com.sg', 1))
        db.session.add(Staff(130002, 'Jack', 'Sim', 'CEO', 'jack.sim@allinone.com.sg', 1))
        db.session.add(Staff(140001, 'Derek', 'Tan', 'Sales', 'Derek.Tan@allinone.com.sg', 3))
        db.session.add(Positions('Human Resource'))
        db.session.add(Positions('Data Analyst'))
        db.session.add(Skill('Public Speaking'))
        db.session.add(Skill('Python'))
        db.session.add(Course('MGT001', 'Agile Leadership', 'Learn Agile leadership', 'Active', 'External', 'Management'))
        db.session.add(Course('FIN001', 'Analytics Foundation', 'Learn pandas framework', 'Retired', 'Internal', 'Analytics'))
        db.session.commit()

        response = self.client.get("/get_learning_journey_by_lj_id/3")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "lj": [
                {
                    "Learning_Journey_ID":3,
                    "Staff_ID": 130002,
                    "Position_Name": 'Data Analyst',
                    "Skill_Name": 'Python',
                    "Course_ID": 'FIN001'
                }
                ]
            }
            }
        ).data)

    def test_get_learning_journey_by_non_existing_lj_id(self):
        db.session.add(LearningJourney(130001, 'Human Resource Manager', 'Public Speaking', 'MGT001'))
        db.session.add(LearningJourney(130001, 'Data Analyst', 'Python', 'FIN001'))
        db.session.add(LearningJourney(130002, 'Data Analyst', 'Python', 'FIN001'))
        db.session.add(Staff(130001, 'John', 'Sim', 'Chairman', 'john.sim@allinone.com.sg', 1))
        db.session.add(Staff(130002, 'Jack', 'Sim', 'CEO', 'jack.sim@allinone.com.sg', 1))
        db.session.add(Staff(140001, 'Derek', 'Tan', 'Sales', 'Derek.Tan@allinone.com.sg', 3))
        db.session.add(Positions('Human Resource'))
        db.session.add(Positions('Data Analyst'))
        db.session.add(Skill('Public Speaking'))
        db.session.add(Skill('Python'))
        db.session.add(Course('MGT001', 'Agile Leadership', 'Learn Agile leadership', 'Active', 'External', 'Management'))
        db.session.add(Course('FIN001', 'Analytics Foundation', 'Learn pandas framework', 'Retired', 'Internal', 'Analytics'))
        db.session.commit()

        response = self.client.get("/get_learning_journey_by_lj_id/4")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
        {
            "code": 404,
            "message": "Learning Journey ID do not exist."
        }
        ).data)

    def test_create_learning_journey(self):
        request_body = {
                    "Staff_ID": 150001,
                    "Position_Name": 'Software Developer',
                    "Skill_Name": 'Python',
                    "Course_ID": 'FIN001'
                }

        response = self.client.post("/create_learning_journey",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        #print(response.data)
        response1 = self.client.get("/get_learning_journey")
        #print(response1.data)
        self.maxDiff = None
        self.assertEqual(response.data, jsonify(
        {
        "code": 201,
        "data": {
                "Staff_ID": 150001,
                "Position_Name": 'Software Developer',
                "Skill_Name": 'Python',
                "Course_ID": 'FIN001'
        }
        }
        ).data)
        #check also that it is posted and learning journey ID is auto_incremented
        self.assertEqual(response1.data, jsonify(
        {
        "code": 200,
        "data": {
            "lj": [
                {
                "Learning_Journey_ID":1,
                "Staff_ID": 150001,
                "Position_Name": 'Software Developer',
                "Skill_Name": 'Python',
                "Course_ID": 'FIN001'
            }
            ]
        }
        }
        ).data)

    def test_delete_learning_journey_by_ID(self):
        db.session.add(LearningJourney(130001, 'Human Resource Manager', 'Public Speaking', 'MGT001'))
        db.session.add(LearningJourney(130001, 'Data Analyst', 'Python', 'FIN001'))
        db.session.add(LearningJourney(130002, 'Data Analyst', 'Python', 'FIN001'))
        db.session.add(Staff(130001, 'John', 'Sim', 'Chairman', 'john.sim@allinone.com.sg', 1))
        db.session.add(Staff(130002, 'Jack', 'Sim', 'CEO', 'jack.sim@allinone.com.sg', 1))
        db.session.add(Staff(140001, 'Derek', 'Tan', 'Sales', 'Derek.Tan@allinone.com.sg', 3))
        db.session.add(Positions('Human Resource'))
        db.session.add(Positions('Data Analyst'))
        db.session.add(Skill('Public Speaking'))
        db.session.add(Skill('Python'))
        db.session.add(Course('MGT001', 'Agile Leadership', 'Learn Agile leadership', 'Active', 'External', 'Management'))
        db.session.add(Course('FIN001', 'Analytics Foundation', 'Learn pandas framework', 'Retired', 'Internal', 'Analytics'))
        db.session.commit()

        self.client.delete("/delete_learning_journey/130001/Human Resource Manager")
        response = self.client.get("/get_learning_journey")

        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "lj": [
                {
                    "Learning_Journey_ID":2,
                    "Staff_ID": 130001,
                    "Position_Name": 'Data Analyst',
                    "Skill_Name": 'Python',
                    "Course_ID": 'FIN001'
                },
                {
                    "Learning_Journey_ID":3,
                    "Staff_ID": 130002,
                    "Position_Name": 'Data Analyst',
                    "Skill_Name": 'Python',
                    "Course_ID": 'FIN001'
                }
                ]
            }
            }
            ).data)

    def test_update_learning_journey_by_ID(self):
        db.session.add(LearningJourney(130001, 'Human Resource Manager', 'Public Speaking', 'MGT001'))
        db.session.add(LearningJourney(130001, 'Data Analyst', 'Python', 'FIN001'))
        db.session.add(LearningJourney(130002, 'Data Analyst', 'Python', 'FIN001'))
        db.session.add(Staff(130001, 'John', 'Sim', 'Chairman', 'john.sim@allinone.com.sg', 1))
        db.session.add(Staff(130002, 'Jack', 'Sim', 'CEO', 'jack.sim@allinone.com.sg', 1))
        db.session.add(Staff(140001, 'Derek', 'Tan', 'Sales', 'Derek.Tan@allinone.com.sg', 3))
        db.session.add(Positions('Human Resource'))
        db.session.add(Positions('Data Analyst'))
        db.session.add(Skill('Public Speaking'))
        db.session.add(Skill('Python'))
        db.session.add(Course('MGT001', 'Agile Leadership', 'Learn Agile leadership', 'Active', 'External', 'Management'))
        db.session.add(Course('FIN001', 'Analytics Foundation', 'Learn pandas framework', 'Retired', 'Internal', 'Analytics'))
        db.session.commit()

        request_body = {
                    "Skill_Name": 'Python',
                    "Course_ID": 'MGT001'
                }

        response = self.client.put("/update_learning_journey/2",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        response1 = self.client.get("/get_learning_journey")
        #print(response.data)
        #return updated learning journey with ID equal 2
        self.assertEqual(response.data, jsonify(
            {
                "code": 200,
                "data": request_body,
                "message": "Successfully updated learning journey " + "2"
            }, 200
        ).data)
        self.assertEqual(response1.data, jsonify(
            {
            "code": 200,
            "data": {
                "lj": [
                {
                    "Learning_Journey_ID":1,
                    "Staff_ID": 130001,
                    "Position_Name": 'Human Resource Manager',
                    "Skill_Name": 'Public Speaking',
                    "Course_ID": 'MGT001'
                },
                {
                    "Learning_Journey_ID":2,
                    "Staff_ID": 130001,
                    "Position_Name": 'Data Analyst',
                    "Skill_Name": 'Python',
                    "Course_ID": 'MGT001'
                },
                {
                    "Learning_Journey_ID":3,
                    "Staff_ID": 130002,
                    "Position_Name": 'Data Analyst',
                    "Skill_Name": 'Python',
                    "Course_ID": 'FIN001'
                }
                ]
            }
            }
        ).data)    


from positions import Positions

class TestPositions(TestApp):    
    def test_create_new_position(self):
        db.session.add(Positions('Human Resource'))
        db.session.add(Positions('Analyst'))
        db.session.add(Positions('Head of Security'))
        db.session.commit()
        new_position = Positions(Position_Name= 'Software Developer')

        request_body = {
            'Position_Name': new_position.Position_Name
        }

        response = self.client.post("/create_new_position/"+new_position.Position_Name,
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        #print(response.data)
        self.maxDiff = None
        self.assertEqual(response.data, jsonify(
        {
            "code": 201,
            "data": {
            'Position_Name': new_position.Position_Name
        }
        }
        ).data)
    
    def test_create_existing_position(self):
        db.session.add(Positions('Human Resource'))
        db.session.add(Positions('Analyst'))
        db.session.add(Positions('Head of Security'))
        db.session.commit()
        new_position = Positions(Position_Name= 'Head of Security')
        # db.session.add(new_position)
        # db.session.commit()

        request_body = {
            'Position_Name': new_position.Position_Name
        }

        response = self.client.post("/create_new_position/"+new_position.Position_Name,
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        #print(response.data)
        self.maxDiff = None
        self.assertEqual(response.data, jsonify(
        {
            "code": 400,
            "data": {"Position_Name":"Head of Security"},
            "message":"Position already exists."}
        ).data)

    def test_get_all_position_empty(self):
        response = self.client.get("/positions")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
        {
            "code": 404,
            "message": "There are no Positions."
        }
        ).data)

    def test_get_all_position(self):
        db.session.add(Positions('Human Resource'))
        db.session.add(Positions('Analyst'))
        db.session.add(Positions('Head of Security'))
        db.session.commit()
        response = self.client.get("/positions")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "positions": [
                {
                    "Position_Name": "Human Resource"
                },
                {
                    "Position_Name": "Analyst"
                },
                {
                    "Position_Name": "Head of Security"
                }
                ]
            }
            }
        ).data)

    def test_delete_position(self):
        db.session.add(Positions('Human Resource'))
        db.session.add(Positions('Analyst'))
        db.session.add(Positions('Head of Security'))
        db.session.commit()
        request_body = {
            'Delete': 'Human Resource'
        }
        self.client.post("/position/delete",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        #print(response.data)
        self.maxDiff = None
         
        response = self.client.get("/positions")
        # print(response.data,'RESPONS DATA!')
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "positions": [
                {
                    "Position_Name": "Analyst"
                },
                {
                    "Position_Name": "Head of Security"
                }
                ]
            }
            }
        ).data)

    #optional
    def test_get_all_position_length(self):
        db.session.add(Positions('Human Resource'))
        db.session.add(Positions('Analyst'))
        db.session.add(Positions('Head of Security'))
        db.session.commit()
        response = self.client.get("/positions")
        #print(response.data)
        response = response.data.decode('utf-8')
        response = json.loads(response)
        self.assertEqual(len(response['data']['positions']), 3)

    def test_get_position_by_name(self):
        db.session.add(Positions('Human Resource'))
        db.session.add(Positions('Analyst'))
        db.session.add(Positions('Head of Security'))
        db.session.commit()
        response = self.client.get("/get_position_by_name/Head of Security")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "Positions": [
                {
                    "Position_Name": "Head of Security"
                }
                ]
            }
            }
        ).data)

    def test_get_position_by_non_existing_name(self):
        db.session.add(Positions('Human Resource'))
        db.session.add(Positions('Analyst'))
        db.session.add(Positions('Head of Security'))
        db.session.commit()
        response = self.client.get("/get_position_by_name/CEO")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
        {
            "code": 404,
            "message": "Position is not found. Please double check."
        }
        ).data)



    def test_update_position(self):
        db.session.add(Positions('Human Resource'))
        db.session.add(Positions('Analyst'))
        db.session.add(Positions('Head of Security'))
        db.session.commit()

        request_body = {
            'Current_Name': 'Analyst',
            'New_Name': 'Senior Analyst'
        }

        response = self.client.post("/position/update",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
                "code": 200,
                "old_position": 'Analyst' ,
                "current_position": 'Senior Analyst'
            }
        ).data)
        response1 = self.client.get("/positions")
        #print(response.data)
        self.assertEqual(response1.data, jsonify(
            {
            "code": 200,
            "data": {
                "positions": [
                {
                    "Position_Name": "Human Resource"
                },
                {
                    "Position_Name": "Senior Analyst"
                },
                {
                    "Position_Name": "Head of Security"
                }
                ]
            }
            }
        ).data)

from registration import Registration

class TestRegistration(TestApp):

    def test_registration_get_all_empty(self):
        response = self.client.get("/registration")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
        {
            "code": 404,
            "message": "There are no registrations."
        }
        ).data)

    def test_registration_get_all(self):
        db.session.add(Registration(1, 'Registered', 'Completed', 'COR002',130001))
        db.session.add(Registration(2, 'Registered', 'Completed', 'COR002',130002))
        db.session.add(Registration(3, 'Registered', 'Completed', 'COR002',140001))
        db.session.commit()
        response = self.client.get("/registration")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "registrations": [
                {
                    'reg_id': 1,
                    'reg_status': 'Registered',
                    'completion_status': 'Completed',
                    'course_id': 'COR002',
                    'staff_id': 130001,
                },
                {
                    'reg_id': 2,
                    'reg_status': 'Registered',
                    'completion_status': 'Completed',
                    'course_id': 'COR002',
                    'staff_id': 130002,
                },
                {
                    'reg_id': 3,
                    'reg_status': 'Registered',
                    'completion_status': 'Completed',
                    'course_id': 'COR002',
                    'staff_id': 140001,
                }
                ]
            }
            }
        ).data)

from role import Role

class TestRole(TestApp): 

    def test_role_get_all_empty(self):
        response = self.client.get("/role")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
        {
            "code": 404,
            "message": "There are no Roles."
        }
        ).data)

    def test_role_get_all(self):
        db.session.add(Role(1, 'Admin'))
        db.session.add(Role(2, 'User'))
        db.session.add(Role(3, 'Manager'))
        db.session.add(Role(4, 'Trainer'))
        db.session.commit()

        response = self.client.get("/role")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "roles": [
                {
                    'role_id': 1,
                    'role_name': 'Admin'
                },
                {
                    'role_id': 2,
                    'role_name': 'User'
                },
                {
                    'role_id': 3,
                    'role_name': 'Manager'
                },
                {
                    'role_id': 4,
                    'role_name': 'Trainer'
                }
                ]
            }
            }
        ).data)

from skill_rewarded import Skill_Rewarded

class TestSkillRewarded(TestApp):

    def test_view_course_skills(self):
        db.session.add(Skill_Rewarded('Python','FIN001'))
        db.session.add(Skill_Rewarded('Tableau','COR001'))
        db.session.add(Skill_Rewarded('R','COR001'))
        db.session.commit()

        response = self.client.get("/view_course_skills/get_skill/COR001")

        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "Skill_Rewarded": [
                {
                    "Skill_Rewarded_ID": 2, 
                    "Skill_Name": 'Tableau', 
                    "Course_ID": 'COR001'
                },
                {
                    "Skill_Rewarded_ID": 3, 
                    "Skill_Name": 'R', 
                    "Course_ID": 'COR001'
                }
                ]
            }
                }
            ).data)

    def test_view_course_skills_with_wrong_CourseID(self):
        db.session.add(Skill_Rewarded('Python','FIN001'))
        db.session.add(Skill_Rewarded('Tableau','COR001'))
        db.session.add(Skill_Rewarded('R','COR001'))
        db.session.commit()

        response = self.client.get("/view_course_skills/get_skill/COR002")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
        {
            "code": 404,
            "message": "Course ID is not found. Please double check."
        }
        ).data)

    def test_view_course_by_skill_name(self):
        db.session.add(Skill_Rewarded('Python','FIN001'))
        db.session.add(Skill_Rewarded('Tableau','COR001'))
        db.session.add(Skill_Rewarded('R','COR001'))
        db.session.commit()

        response = self.client.get("/view_course_skills/get_course/Python")

        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "Skill_Rewarded": [
                {
                    "Skill_Rewarded_ID": 1, 
                    "Skill_Name": 'Python', 
                    "Course_ID": 'FIN001'
                }
                ]
            }
            }
        ).data)


    def test_delete_skill_from_course_by_id(self):
        db.session.add(Skill_Rewarded('Python','FIN001'))
        db.session.add(Skill_Rewarded('Tableau','COR001'))
        db.session.add(Skill_Rewarded('R','COR001'))
        db.session.commit()
        request_body = {
                        "Skill_Name": 'Tableau', 
                        "Course_ID": 'COR001'
                        }

        response = self.client.post("/delete_skill_rewarded",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        #print(response.data)
        self.maxDiff = None
        #print(response.data)
        self.assertEqual(response.data, jsonify(
         {
                    "code": 200,
                    "message": "Skill is no longer associated with the course."
                }
        ).data)


    def test_view_course_by_non_existing_skill_name(self):
        db.session.add(Skill_Rewarded('Python','FIN001'))
        db.session.add(Skill_Rewarded('Tableau','COR001'))
        db.session.add(Skill_Rewarded('R','COR001'))
        db.session.commit()

        response = self.client.get("/view_course_skills/get_course/Python3")

        self.assertEqual(response.data, jsonify(
            {
                "code": 404,
                "message": "No course is associated"
            }
        ).data)
    
    def test_update_skill_rewarded_same_skill(self):
        db.session.add(Skill_Rewarded('Python','FIN001'))
        db.session.add(Skill_Rewarded('Tableau','COR001'))
        db.session.add(Skill_Rewarded('R','COR001'))
        db.session.commit()
        request_body = {
                        'Skill_Name': 'Python',
                        'Courses_Add': ['COR001'],
                        'Courses_Delete':[]
                    }

        response = self.client.post("/update_skill_rewarded_same_skill",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        #print(response.data)
        self.maxDiff = None
        #print(response.data)
        self.assertEqual(response.data, jsonify(
        {
            "code": 201,
            "message":"skill_rewarded successfully updated!",
            "new skills": [
                {
                    "Skill_Rewarded_ID": 1, 
                    "Skill_Name": 'Python', 
                    "Course_ID": 'FIN001'
                },
                {
                    "Skill_Rewarded_ID": 4, 
                    "Skill_Name": 'Python', 
                    "Course_ID": 'COR001'
                }
                ]
        }
        ).data)


from skill_set import Skill_Set

class TestSkillSet(TestApp):

    def test_get_all_skill_set_empty(self):
        response = self.client.get("/skill_set")
        #print(response.data)
        self.assertEqual(response.data, jsonify({
            "message": "Skill set not found."
        }).data)

    def test_get_all_skill_set(self):
        db.session.add(Skill_Set('Python','Data Analyst'))
        db.session.add(Skill_Set('R','Data Analyst'))
        db.session.add(Skill_Set('Public Speaking','Human Resource'))
        db.session.commit()
        response = self.client.get("/skill_set")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "skill_set": [
                {
                "Skill_Set_ID": 1, 
                "Skill_Name": 'Python', 
                "Position_Name": 'Data Analyst'
                },
                {
                "Skill_Set_ID": 2, 
                "Skill_Name": 'R', 
                "Position_Name":'Data Analyst'
                },
                {
                "Skill_Set_ID": 3, 
                "Skill_Name": 'Public Speaking', 
                "Position_Name":'Human Resource'
                }
                ]
            }
            }
        ).data)

    def test_get_skills_by_position(self):
        db.session.add(Skill_Set('Python','Data Analyst'))
        db.session.add(Skill_Set('R','Data Analyst'))
        db.session.add(Skill_Set('Public Speaking','Human Resource'))
        db.session.commit()
        response = self.client.get("/skill_set/Data Analyst")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "Skill_Set": [
                {
                "Skill_Set_ID": 1, 
                "Skill_Name": 'Python', 
                "Position_Name": 'Data Analyst'
                },
                {
                "Skill_Set_ID": 2, 
                "Skill_Name": 'R', 
                "Position_Name":'Data Analyst'
                }
                ]
            }
            }
        ).data)

    def test_get_skills_by_non_existing_position(self):
        db.session.add(Skill_Set('Python','Data Analyst'))
        db.session.add(Skill_Set('R','Data Analyst'))
        db.session.add(Skill_Set('Public Speaking','Human Resource'))
        db.session.commit()
        response = self.client.get("/skill_set/CEO")
        print(response.data)
        self.assertEqual(response.data, jsonify(
        {
            "code": 404,
            "message": "Position name is not found. Please double check."
        }
        ).data)

    def test_create_new_skillset(self):
        db.session.add(Skill_Set('Python','Data Analyst'))
        db.session.add(Skill_Set('R','Data Analyst'))
        db.session.add(Skill_Set('Public Speaking','Human Resource'))
        db.session.commit()

        request_body = {
                        "Skill_Name": 'Tableau', 
                        "Position_Name": 'Data Analyst'
                        }

        response = self.client.post("/create_new_skillset",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        #print(response.data)
        self.maxDiff = None
        response1 = self.client.get("/skill_set")
        #print(response.data)
        self.assertEqual(response1.data, jsonify(
            {
            "code": 200,
            "data": {
                "skill_set": [
                {
                "Skill_Set_ID": 1, 
                "Skill_Name": 'Python', 
                "Position_Name": 'Data Analyst'
                },
                {
                "Skill_Set_ID": 2, 
                "Skill_Name": 'R', 
                "Position_Name":'Data Analyst'
                },
                {
                "Skill_Set_ID": 3, 
                "Skill_Name": 'Public Speaking', 
                "Position_Name":'Human Resource'
                },
                {
                "Skill_Set_ID": 4, 
                "Skill_Name": 'Tableau', 
                "Position_Name":'Data Analyst'
                }
                ]
            }
            }
        ).data)

    def test_update_skillset_same_skill(self):
        db.session.add(Skill_Set('Python','Data Analyst'))
        db.session.add(Skill_Set('R','Data Analyst'))
        db.session.add(Skill_Set('Public Speaking','Human Resource'))
        db.session.commit()

        request_body = {
                        "Skill_Name": 'Python', 
                        "Positions_Add": ['Head of Securities'],
                        'Positions_Delete': []
                        }

        response = self.client.post("/update_skillset_same_skill",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        print(response.data)
        self.maxDiff = None
        response1 = self.client.get("/skill_set")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
                "code":201,
                "message":"skills successfully updated!",
                "new skills":[
                    {
                    "Position_Name":"Data Analyst",
                    "Skill_Name":"Python",
                    "Skill_Set_ID":1
                    },
                    {
                    "Position_Name":"Head of Securities",
                    "Skill_Name":"Python",
                    "Skill_Set_ID":4
                    }
                ]
            }
        ).data)

from skill import Skill

class TestSkills(TestApp):

    def test_skill_get_all_empty(self):
        response = self.client.get("/skill")
        #print(response.data)
        self.assertEqual(response.data, jsonify({
            "message": "Skills not found."
        }).data)

    def test_skill_get_all(self):
        db.session.add(Skill('Python'))
        db.session.add(Skill('Flutter'))
        db.session.add(Skill('Tableau'))
        db.session.commit()
        response = self.client.get("/skill")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "skill": [
                {
                    "Skill_Name": "Python"
                },
                {
                    "Skill_Name": "Flutter"
                },
                {
                    "Skill_Name": "Tableau"
                }
                ]
            }
            }
        ).data)
    
    #test if wildcard works
    def test_skill_get_by_name_wildcard(self):
        db.session.add(Skill('Python'))
        db.session.add(Skill('Flutter'))
        db.session.add(Skill('Tableau'))
        db.session.commit()
        response = self.client.get("/skill/name/P")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "skills": [
                {
                    "Skill_Name": "Python"
                }
                ]
            }
            }
        ).data)
    def test_create_new_skill(self):
        db.session.add(Skill('Python'))
        db.session.add(Skill('Flutter'))
        db.session.add(Skill('Tableau'))
        db.session.commit()
        
        new_skill = Skill(Skill_Name= 'Public Speaking SKills')

        request_body = {
            'Skill_Name': new_skill.Skill_Name
        }

        response = self.client.post("/skill/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        response1 = self.client.get("/skill")
        #print(response.data)
        self.maxDiff = None
        self.assertEqual(response.data, jsonify(
            {
            "code": 201,
            "data": {
                "Skill_Name": new_skill.Skill_Name
            }
            }
        ).data)
 
        self.assertEqual(response1.data,jsonify(
            {
            "code": 200,
            "data": {
                "skill": [
                {
                    "Skill_Name": "Python"
                },
                {
                    "Skill_Name": "Flutter"
                },
                {
                    "Skill_Name": "Tableau"
                },
                                {
                    "Skill_Name": "Public Speaking SKills"
                }
                ]
            }
            }
        ).data)

    def test_create_existing_skill(self):
        db.session.add(Skill('Python'))
        db.session.add(Skill('Flutter'))
        db.session.add(Skill('Tableau'))
        db.session.commit()
        
        new_skill = Skill(Skill_Name= 'Python')

        request_body = {
            'Skill_Name': new_skill.Skill_Name
        }

        response = self.client.post("/skill/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        #print(response.data)
        self.maxDiff = None
        self.assertEqual(response.data, jsonify(
            {
            "code": 400,
            "data": {
                "Skill_Name":"Python"
                },
            "message":"Skill already exists."
            }
        ).data)

    def test_delete_skill_by_name(self):
        db.session.add(Skill('Python'))
        db.session.add(Skill('Flutter'))
        db.session.add(Skill('Tableau'))
        db.session.commit()

        self.client.delete("/skill/delete/Python")
        response1 = self.client.get("/skill")

        self.assertEqual(response1.data, jsonify(
            {
            "code": 200,
            "data": {
                "skill": [
                {
                    "Skill_Name": "Flutter"
                },
                {
                    "Skill_Name": "Tableau"
                }
                ]
            }
            }
        ).data)

    def test_delete_non_existing_skill_name(self):
        db.session.add(Skill('Python'))
        db.session.add(Skill('Flutter'))
        db.session.add(Skill('Tableau'))
        db.session.commit()

        response = self.client.delete("/skill/delete/Python3")
        response1 = self.client.get("/skill")
        self.assertEqual(response.data,jsonify(
            {
                "code": 404,
                "data": {
                    "Skill_Name": 'Python3'
                },
                "message": "Skill does not exist"
            }
        ).data)
        self.assertEqual(response1.data, jsonify(
            {
            "code": 200,
            "data": {
                "skill": [
                {
                    "Skill_Name": "Python"
                },
                {
                    "Skill_Name": "Flutter"
                },
                {
                    "Skill_Name": "Tableau"
                }
                ]
            }
            }
        ).data)

    def test_update_skill(self):
        db.session.add(Skill('Python'))
        db.session.add(Skill('Flutter'))
        db.session.add(Skill('Tableau'))
        db.session.commit()

        request_body = {
            "Old_Skill_Name":"Python",
            "New_Skill_Name":"Flask"
        }

        response = self.client.post("/skill/update",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
                "code": 200,
                "message": "Python has been changed to Flask"
            }
        ).data)

    def test_skill_get_by_name(self):
        db.session.add(Skill('Python'))
        db.session.add(Skill('Flutter'))
        db.session.add(Skill('Tableau'))
        db.session.commit()
        response = self.client.get("/skill/name/F")
        #print(response.data)
        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "skills": [
                {
                    "Skill_Name": "Flutter"
                }
                ]
            }
            }
        ).data)

    def test_skill_get_by_non_existing_name(self):
        db.session.add(Skill('Python'))
        db.session.add(Skill('Flutter'))
        db.session.add(Skill('Tableau'))
        db.session.commit()
        response = self.client.get("/skill/name/PublicSpeaking")
        #print(response.data)
        self.assertEqual(response.data, jsonify (
        {
            "code": 404,
            "message": 'No skill named PublicSpeaking'
        }
        ).data)


from staff import Staff

class TestStaff(TestApp): 
    def test_staff_get_all(self):
        db.session.add(Staff(130001, 'John', 'Sim', 'Chairman', 'john.sim@allinone.com.sg', 1))
        db.session.add(Staff(130002, 'Jack', 'Sim', 'CEO', 'jack.sim@allinone.com.sg', 1))
        db.session.add(Staff(140001, 'Derek', 'Tan', 'Sales', 'Derek.Tan@allinone.com.sg', 3))
        db.session.commit()

        response = self.client.get("/staff")

        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "staffs": [
                {
                    'staff_id': 130001,
                    'staff_fname': 'John',
                    'staff_lname': 'Sim',
                    'dept': 'Chairman',
                    'email': 'john.sim@allinone.com.sg',
                    'role': 1
                },
                {
                    'staff_id': 130002,
                    'staff_fname': 'Jack',
                    'staff_lname': 'Sim',
                    'dept': 'CEO',
                    'email': 'jack.sim@allinone.com.sg',
                    'role': 1
                },
                {
                    'staff_id': 140001,
                    'staff_fname': 'Derek',
                    'staff_lname': 'Tan',
                    'dept': 'Sales',
                    'email': 'Derek.Tan@allinone.com.sg',
                    'role': 3
                }
                ]
            }
            }
        ).data)

    def test_staff_get_by_id(self):
        db.session.add(Staff(130001, 'John', 'Sim', 'Chairman', 'john.sim@allinone.com.sg', 1))
        db.session.add(Staff(130002, 'Jack', 'Sim', 'CEO', 'jack.sim@allinone.com.sg', 1))
        db.session.add(Staff(140001, 'Derek', 'Tan', 'Sales', 'Derek.Tan@allinone.com.sg', 3))
        db.session.commit()

        response = self.client.get("/staff_get/130001")

        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "staff": [
                {
                    'staff_id': 130001,
                    'staff_fname': 'John',
                    'staff_lname': 'Sim',
                    'dept': 'Chairman',
                    'email': 'john.sim@allinone.com.sg',
                    'role': 1
                }
                ]
            }
            }
        ).data)

    def test_staff_get_by_dept(self):
        db.session.add(Staff(130001, 'John', 'Sim', 'Chairman', 'john.sim@allinone.com.sg', 1))
        db.session.add(Staff(130002, 'Jack', 'Sim', 'CEO', 'jack.sim@allinone.com.sg', 1))
        db.session.add(Staff(140001, 'Derek', 'Tan', 'Sales', 'Derek.Tan@allinone.com.sg', 3))
        db.session.commit()

        response = self.client.get("/staff_get_by_dept/Sales")

        self.assertEqual(response.data, jsonify(
            {
            "code": 200,
            "data": {
                "staffs": [
                {
                    'staff_id': 140001,
                    'staff_fname': 'Derek',
                    'staff_lname': 'Tan',
                    'dept': 'Sales',
                    'email': 'Derek.Tan@allinone.com.sg',
                    'role': 3
                }
                ]
            }
            }
        ).data)

#allow us to run the whole test suite by running - python test_unittest.py
#UPDATE: don't have to cd test just run: python -m unittest test.test_unittest
if __name__ == '__main__':
    unittest.main()