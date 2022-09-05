from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, true")
        response.headers.add("Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTION")
        return response


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        
        categories = [categories.format() for categories in Category.query.all()]

        #https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/3_Testing_Starter/backend/flaskr/__init__.py
        if categories is None:
            abort(404)

        data = {}
        
        for category in categories:
            data[category['id']] = category['type']

        return jsonify({
            "categories": data
        })
    


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        # Implement pagniation/Udacity
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        #Recupère les questions
        questions = Question.query.order_by(Question.id).all()

        formatted_question = [question.format() for question in questions]
        data_question = formatted_question[start:end]
        #a = len(data_question)

        #Test
        if len(data_question) != 0:

            #Recupere categories
            categories = [categories.format() for categories in Category.query.all()]

            #https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/3_Testing_Starter/backend/flaskr/__init__.py
            if categories is None:
                abort(404)

            data = {}
            
            for category in categories:
                data[category['id']] = category['type']
            
            return jsonify({
                            "questions": data_question,
                            "totalQuestions": len(formatted_question),
                            "categories": data,
                            "currentCategory": None})
        else:
            abort(404)


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            question = Question.query.get(question_id)

            if question is None:
                abort(404)
            
            question.delete()

            return jsonify({
                'id': question.id,
                'message': 'Question supprimée avec succès'
            })
        
        except AttributeError:
            return jsonify({
                'message': 'Question na pas été supprimé' 
            })
    

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods =['POST'])
    def create_questions():

        #recuperation du corps de la requete
        body = request.get_json()

        if len(body) == 4:
            question = body.get('question')
            answer = body.get('answer')
            category = body.get('category')
            difficulty = body.get('difficulty')

            new_question = Question(question, answer, category, difficulty)
            new_question.insert()

            return jsonify({
                "message":"Question ajoutée avec succès"
            })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/titles', methods =['POST'])
    def search_question():
        body = request.get_json('searchTerm')
        searchTerm = body.get('searchTerm')
        
        result = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
        question = [data.format() for data in result]
        
        return jsonify({
                    "questions":question,
                    "totalQuestions": len(result),
                    "currentCategory": None
                })


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:cat_id>/questions')
    def get_category(cat_id):
        category = Category.query.filter(Category.id == cat_id).one_or_none()

        if category is None:
            abort(404)
        
        # all questions par category
        all_questions = Question.query.filter(Question.category == cat_id).all()

        if all_questions is None:
            abort(400)

        question_cat = [question.format() for question in all_questions]

        return jsonify({
                "success": True, 
                "questions":question_cat,
                "totalQuestions": len(question_cat),
                "currentCategory": category.type.format()
                })




    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods =['POST'])
    def get_quiz():

        try:

            #recupere le corps de la requette
            body = request.get_json()
            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')

            if ((previous_questions is None) or (quiz_category is None)):   
                abort(400)

            #Obtenir les questions en fonctions de categories qui ne sont pas dans les questions précedantes
            if quiz_category['id'] == 0:
                all_questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
            else:
                all_questions = Question.query.filter_by(category=quiz_category['id']).filter(Question.id.notin_((previous_questions))).all()
            
            question = all_questions[random.randrange(0, len(all_questions))].format() if len(all_questions) > 0 else None

            return jsonify({
                    'success': True,
                    'question': question
                })
        except:
            abort(422)
        
        




    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(500)
    def not_found(error):
        return (
            jsonify({"success": False, 
            "error": 500, 
            "message": "Internal Server Error"}),
            500,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, 
            "error": 404, 
            "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, 
            "error": 422, 
            "message": "unprocessable Entity"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, 
        "error": 400, 
        "message": "bad request"}), 400
    

    return app

