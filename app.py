import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db,Movies,Category,db




############Paginations#############

def pagination (request, sel):
    #Implement pagination, get the arg of page and if it dont exist, then it will default to 1
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10
    formatt = [ movies.format() for movies in sel]
    #instead of getting all the query it will get only the "start to end "
    pag = formatt[start:end]
    return pag

########API ##############
def create_app(test_config=None):
    # create and configure the app and Migrations
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    #cors = CORS(app, resources={r"/categories": {"origins": "http://localhost:5000"}}
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH,DELETE, OPTIONS')
        return response

    #########MOVIE CATEGORIES######
    @app.route('/categories', methods=['GET'])

    #@cross_origin()
    def get_categories():
        try:
            cats = Category.query.all()
            format_cats = {cat.id:cat.type for cat in cats}
            return jsonify({
                'success': True,
                'categories' : format_cats,
                'total_categories':len(cats)
                })
        except:
            abort(500)

    #done
    ###########HOME OR GET MOVIES##########
    @app.route('/', methods=['GET'])
    def get_movies():
        try:
            sel = Movies.query.all()
            paged_que = pagination(request, sel)
            if len(paged_que) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'Movies' : paged_que,
                'totalMovies':len(sel),
                })
        except:
            abort(404)

    #########GET MOVIE BY ID #############
    @app.route("/movie/<int:movie_id>", methods=["GET"])
    def get_movies_by_id (movie_id):
        movie = {}
        result = Movies.query.filter(Movies.id == movie_id).one_or_none()
        if result is None:
            abort(404)
            print (result)
        else:
            movie['id'] = result.id
            movie['title'] = result.title
            movie['thumbnails']  = result.thumbnails
            movie['category']  = result.category
            movie['rating']  = result.year
            movie['isbookmarked']  = result.isbookmarked
            movie['istrending'] = result.istrending
        return jsonify({
            "success": True,
            "data" : movie
            })

    #########DELETE MOVIE#############
    @app.route("/movie/<int:movie_id>", methods=["DELETE"])
    def delete_movie (movie_id):
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        else:
            movie.delete()
            return jsonify({
                "success": True,
                "deleted": movie_id,
            })

    ############CREATE A NEW MOVIE#################
    @app.route("/movie/create", methods=["POST"])
    def create_movie():
        data_body = request.get_json()
        new_title = data_body.get("title")
        new_thumbnails = data_body.get("thumbnails",)
        new_year = data_body.get("year")
        new_category = data_body.get("category")
        new_rating = data_body.get("rating")
        new_isbookmarked = data_body["isbookmarked"]
        new_istrending = data_body["istrending"]

        movie = Movies.query.filter(Movies.title == new_title).one_or_none()
        if movie is None:
            new_movie = Movies(
                title =  new_title,
                thumbnails = new_thumbnails,
                year = new_year,
                category = new_category,
                rating = new_rating,
                isbookmarked = new_isbookmarked,
                istrending = new_istrending
            )
            new_movie.insert()
        else:
            abort(400)
            #print("movie title already exist ")
        sel = Movies.query.order_by(Movies.id).all()
        paged_que = pagination(request, sel)
        return jsonify({
            'success': True,
            'created Movie': new_movie.id,
            'data' : paged_que,
            'total_movies':len(sel)
        })

    #done
    ######MOVIE SEARCH################
    @app.route('/movie/search', methods=['POST'])
    def movie_search():
        try:

            data_body = request.get_json()
            search = data_body.get("search",None)
            search_term=search.title()
            print(search_term)
            results = Movies.query.filter(Movies.title.like("%"+search_term+"%")).all()
            data=[]
            for res in results:
                info = {
                    "title" : res.title,
                    "thumbnails" :res.thumbnails,
                    "year": res.year,
                    "category": res.category,
                    "rating" :res.rating,
                    "isbookmarked": res.isbookmarked,
                    "istrending": res.istrending

                }
                data.append(info)
            count = len(results)
            return jsonify({

                    'success': True,
                    'totalMovies' : count,
                    'searched_results' : data
                })
        except:
            (422)

    #done
    #########MOVIES BY CATEGORIES####
    @app.route('/categories/<int:category_id>/movie', methods=['GET'])
    def get_movies_by_category(category_id):
        try:
            data=[]
            category = Movies.query.join(Category,Movies.category == category_id).all()
            if category == None:
                abort(404)
            cur =  Category.query.get(category_id)
            current = cur.type
            for res in category:
                info = {

                    "title" : res.title,
                    "thumbnails" :res.thumbnails,
                    "year": res.year,
                    "category": res.category,
                    "rating" :res.rating,
                    "isbookmarked": res.isbookmarked,
                    "istrending": res.istrending

                }
                data.append(info)
            return jsonify({
                'success': True,
                'questions' : data,
                'totalQuestions' : len(category),
                'currentCatergory': current
            })
        except:
            abort(404)





    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Requested page Not found"
            }), 404


    @app.errorhandler(422)
    def unprocessed_request(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Server can't process your request"
            }), 422


    @app.errorhandler(400)
    def invalid_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
            }), 400


    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
            }),500


    return app
