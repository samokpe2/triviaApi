import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question={"question":"What is the Capital of Finland", "answer":"Helsinki", "category":3, "difficulty":2}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # GET /categories
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))

    def test__405_get_categories(self):
        res = self.client().post("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "The requested method is not allowed")

    # GET /questions?<page=pagenumber>

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["categories"]))
        self.assertEqual(data["current_category"], None)

    def test_get_paginated_questions_with_page(self):
        res = self.client().get("/questions?page=2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["categories"]))
        self.assertEqual(data["current_category"], None)

    def test_404_get_questions_invalid_page(self):
        res = self.client().get("/questions?page=1000", json={"category": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "The requested resource is not found")

    #DELETE /questions/<id>

    def test_delete_question(self):
        res = self.client().delete("/questions/21")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 21).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 21)
        self.assertTrue(data["total_questions"])

    def test_book_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["deleted"], None)
        self.assertTrue(data["total_questions"])
    
    # POST /questions

    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])

    def test_405_if_create_qn_not_allowed(self):
        res = self.client().post("/questions/45", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "The requested method is not allowed")

    # Search POST /questions
    def test_search_question(self):
        res = self.client().post("/questions", json={"searchTerm":"What"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], None)

    def test_search_question_not_found(self):
        res = self.client().post("/questions", json={"searchTerm":"Whatx"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]),0)
        self.assertEqual(data["total_questions"],0)
        self.assertEqual(data["current_category"], None)

    #GET /categories/<id>/questions
    def test_get_qns_by_category(self):
        res=self.client().get("/categories/2/questions")
        data = json.loads(res.data)
        curr_category=Category.query.get(2).type

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], curr_category)

    def test_404_get_qns_by_invalidcategory(self):
        res=self.client().get("/categories/777/questions")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "The requested resource is not found")
        self.assertEqual(data["success"], False)


    def test_404_get_invalidqns_by_category(self):
        res=self.client().get("/categories/3/questions/12")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "The requested resource is not found")
        self.assertEqual(data["success"], False)

    def test_405_get_invalidqns_by_category(self):
        res=self.client().post("/categories/3/questions")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["message"], "The requested method is not allowed")
        self.assertEqual(data["success"], False)
    
    #POST /quizzes


    def test_get_quiz_question_given_category(self):
        self.quiz_input = {'previous_questions':[1], 'quiz_category':{'id':'1'}}
        res=self.client().post("/quizzes", json=self.quiz_input)

        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])
        self.assertEqual(data["success"], True)

    def test_get_400_quiz_question_without_category(self):
        self.quiz_input = {'previous_questions':[1]}
        res=self.client().post("/quizzes", json=self.quiz_input)

        data=json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["message"],"bad request")
        self.assertEqual(data["success"], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()