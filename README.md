# Backend - Entertianment Web App API


### Install Dependencies

1. **Python 3.7** - Follow the steps in the to install the most recent version of Python for your platform.[python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - When using Python for projects, we recommend working in a virtual environment. This keeps your project dependencies distinct and structured. Setup instructions for your platform's virtual environment may be found in the[python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Install the needed dependencies after your virtual environment is up and running by heading to the API directory and executing:

```bash
pip install -r requirements.txt
```

#### Major Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Setting up your Database

Having Postgres installed and running, create a `entertainment` database:

```bash
createbd entertainment
```
```powershell
createbd entertainment
```

Fill up the database using the included 'Entertain.psql' file. In terminal, run the following command from the same directory as the psql file:

```bash
psql entertainment < Entertain.psql
```

```powershell or CMD
psql -U postgres entertainment < Entertain.psql
```

### Run the Server

First, confirm that you are working in your generated virtual environment from within the directory.

To start the server, type:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


### Endpoints Documentation

`GET '/categories'`

-Gets a dictionary of categories, where the keys are the ids and the value is the category's associated string.

- There are no request arguments.

- Returns: An object with a single key, `categories`, that contains an object with the key: value pairs `id: category string`.

```json
{
    "categories": {
        "1": "Movies",
        "2": "Tv Series"
    },
    "success": true,
    "total_categories": 2
}
```

`GET '/'`

-Gets an array of movies dictionarys,contain each movie attributes

- There are no request arguments.

- Returns: An Array that contains objects where each object key value are the attributes of that object.

```json
 "Movies": [
        {
            "category": 1,
            "id": 1,
            "isbookmarked": false,
            "istrending": true,
            "rating": "PG",
            "thumbnails": "./assets/thumbnails/beyond-earth/trending/small.jpg",
            "title": "Beyond Earth",
            "year": 2019
        },
        {
            "category": 2,
            "id": 3,
            "isbookmarked": false,
            "istrending": true,
            "rating": "18+",
            "thumbnails": "./assets/thumbnails/autosport-the-series/regular/large.jpg",
            "title": "Autosport the Series",
            "year": 2016
        },
    ],
    "success": true,
    "totalMovies": 2
}

```