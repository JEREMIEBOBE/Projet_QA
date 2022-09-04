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
        #self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgresql://{}:{}@{}/{}".format("postgres", "bobe", "localhost:5432", self.database_name)

        setup_db(self.app, self.database_path)

        # new question
        self.new_question = {
            'question': 'Capitale de la RDC?',
            'answer': 'Kinshasa',
            'difficulty': 1,
            'category': 3
        }

        self.error_question = {
            'question': 'Capitale de la RDC?',
            'answer': 'Kinshasa'
        }

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
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        #self.assertEqual(data["success"], True)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data['questions'])
        self.assertTrue(len(data["questions"]))
        #self.assertIsInstance(data['questions'], list)

    def test_error_sent_questions(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    
    def test_retrieve_categories(self):
        """GET categories """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        

    def test_404_categories(self):
        res = self.client().get('/categories/*')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_create_new_question(self):
        """Tests question creation success"""
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["message"], "Question ajoutée avec succès")
    
    def test_error_create_new_question(self):
        """Tests question creation success"""
        res = self.client().post('/questions', json=self.error_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error')
    
    
    def test_delete_question(self):

        question = Question(question=self.new_question['question'], answer=self.new_question['answer'],
                            category=self.new_question['category'], difficulty=self.new_question['difficulty'])
        
        question.insert()

        # get  new question
        q_id = question.id

        # test
        response = self.client().delete('/questions/{}'.format(q_id))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_error_delete_question(self):

        
        # get  new question
        q_id = 100

        # test
        response = self.client().delete('/questions/{}'.format(q_id))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    
    def test_get_questions_by_category(self):
        """Tests getting questions by category success"""
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_error_questions_by_category(self):
        
        response = self.client().get('/categories/100/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    
    def test_play_quiz_game(self):
        
        response = self.client().post('/quizzes',
                                      json={'previous_questions': [20, 21],
                                            'quiz_category': {'type': 'Science', 'id': '1'}})

        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    

    def test_play_quiz_fails(self):
        
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable Entity')
    

    def test_search_questions(self):
        
        response = self.client().post('/questions/titles',json={'searchTerm': 'Amer'})

        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
                

    def test_error_search_questions(self):
        
        response = self.client().post('/questions/titles')
        data = json.loads(response.data)

        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()