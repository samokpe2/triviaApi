import os
from tokenize import String
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql import func

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r'*':{'origins':'*'}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,DELETE,OPTIONS")
        return response

    #Pagiantion logic
    def paginate_qns(request, questions):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        qns = [qn.format() for qn in questions]
        current_qns = qns[start:end]
        return current_qns

#####CATEGORIES#############

    def get_categories_helper():
        try:
            categories = Category.query.order_by(Category.id).all()
            dict_of_categories={}
            for category in categories:
                dict_of_categories[category.id]=category.type
            return dict_of_categories
        except:
            abort(404)

    @app.route('/categories', methods=['GET'])
    def get_categories():
        return jsonify({
            'success':True,
            'categories':get_categories_helper()
            })
         
#######--------QUESTIONS-------#############

    #GET /question paginated
    def get_questions_helper():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_qns(request, questions)
        if(len(current_questions)==0):
            abort(404)
        return jsonify(
                {
                    'success':True,
                    'questions':current_questions,
                    'total_questions':len(Question.query.all()),
                    'categories': get_categories_helper(),
                    'current_category':None
                }
            )

    @app.route('/questions', methods=['GET'])
    def get_questions():
        return get_questions_helper()
        
    #Delete question
    def delete_qn_helper(qn_id):
        try:
            qn = Question.query.get_or_404(qn_id)
            qn.delete()
            return jsonify({'success': True,
            'deleted':qn_id,
            'total_questions': Question.query.count() })
        except:
            db.session.rollback()
            return jsonify({'success': False,
            'deleted':None,
            'total_questions': Question.query.count() }),404
        finally:
            db.session.close()
             

    @app.route('/questions/<int:qn_id>', methods=['DELETE'])
    def delete_question(qn_id):
        return delete_qn_helper(qn_id)

    #POST or Search question

    def post_or_search_questions_helper(request):
        body = request.get_json()
        question = body.get("question", None)
        answer = body.get("answer", None)
        difficulty = body.get("difficulty", None)
        category = body.get("category", None)
        searchkey = body.get("searchTerm", None)

        try:
            if searchkey:
                #Search Logic
                ques_list = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(searchkey))
                )
                current_questions = paginate_qns(request, ques_list)
                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": len(ques_list.all()),
                        "current_category":None
                    }
                )
            else:
                #post question
                question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
                question.insert()
                question_list = Question.query.order_by(Question.id).all()
                current_qns = paginate_qns(request, question_list)

                return jsonify(
                    {
                        "success": True,
                        "created": question.id,
                        "questions": current_qns,
                        "total_questions": len(Question.query.all()),
                    }
                )
        except:
            abort(422)


    @app.route('/questions', methods=['POST'])
    def post_or_search_questions():
        return post_or_search_questions_helper(request)

    #Get quesitons by category

    def get_qns_by_category_helper(cat_id):
        try:
            questions = Question.query.filter(Question.category==cat_id).all()
            curr_category=Category.query.get(cat_id)
            qns = [qn.format() for qn in questions]     
            return jsonify(
                    {
                        'success':True,
                        'questions':qns,
                        'total_questions':len(qns),
                        'current_category':curr_category.type
                    }
                )
        except:
            abort(404)


    @app.route('/categories/<cat_id>/questions', methods=['GET'])
    def get_qns_by_category(cat_id):
        return get_qns_by_category_helper(cat_id)


    #Play Quiz
    
    def quiz_helper(request):
        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions", None)
            if previous_questions is None:
                abort(400)
            quiz_category = body.get("quiz_category", None)
            if quiz_category is None:
                abort(400)
            categ = quiz_category['id']
            if(categ == 0):
                qn = Question.query.filter(~Question.id.in_(previous_questions)).order_by(func.random()).first()
            else:
                qn = Question.query.filter(Question.category == categ, ~Question.id.in_(previous_questions)).order_by(func.random()).first()
            qn_final = qn if (qn==None) else qn.format()
            
            return jsonify({
                'success':True,
                'question':qn_final})
        except:
            abort(400)


    @app.route('/quizzes', methods=['POST'])
    def post_quiz():
        return quiz_helper(request)


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "The requested resource is not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable request"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}), 400
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "The requested method is not allowed"}),
            405,
        )

    return app

