# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

1. `GET 'http://127.0.0.1:5000/categories'`

- Cet endpoint permet de recuperer un dictionnaire contenant la liste de catégories
- Request Arguments: None
- Response body : Recupère un objet `categories` sous forme d'une paire clé:valeur
      ```json
              {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
                }
        ```

2. `GET 'http://127.0.0.1:5000//questions?page=${integer}'`

- Cet endpoint permet de recuperer la liste de questions en format json
- Request Arguments: `<page>` qui est un entier, chaque page contient 10 questions 
- Response body : Au format json, contenant un dictionnaire de catégorie, liste des questions
```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "currentCategory": null,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        }
    ],
    "totalQuestions": 60
}
```
3. `GET 'http://127.0.0.1:5000/categories/${id}/questions'`

- Cet endpoint permet de recuperer les questions pour une catégorie indiquée par l'argument id request
- Request Arguments: <<id>>, qui est entier
- Response body : Recupère objet avec des questions pour la catégorie désignée, le total des questions et la chaîne   de catégorie actuelle
      ```json
  {
    "currentCategory": "Science",
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "success": true,
    "totalQuestions": 3
    }
        ```
4. `POST 'http://127.0.0.1:5000/questions'`

- Cet endpoint permet de créer une question
- Request Arguments: None
- Request body : contient un objet au format json
    ```json
      {
        "question": "Capitale de la RDC?",
        "answer": "Kinshasa",
        "difficulty": 1,
        "category": 3
      }
    ```
- Response body : un message de confirmation
      ```json
              {
                "message":"Question ajoutée avec succès"
                }
        ```

5. `POST 'http://127.0.0.1:5000/questions/titles'`

- Cet endpoint permet de rechercher une(des) question(s) contenant un terme fourni par user
- Request Arguments: None
- Request body : contient un objet au format json
    ```json
      {
        "searchTerm": "Amer"
      }
    ```
- Response body : un certain nombre de questions qui correspondent au terme de recherche et le nombre total de questions
      ```json
              "currentCategory": null,
              "questions": [
                  {
                      "answer": "Jackson Pollock",
                      "category": 2,
                      "difficulty": 2,
                      "id": 19,
                      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
                  }],
              "totalQuestions": 1
}
        ```

6. `POST 'http://127.0.0.1:5000/quizzes'`

- Cet endpoint permet d'obtenir la prochaine question
- Request Arguments: None
- Request body : contient un objet au format json contenant les questions précédantes et la catégorie courante
    ```json
      {
        "previous_questions": [1, 4, 20, 15],
        "quiz_category": "current category"
      }
    ```
- Response body : renvoi une nouvelle question
      ```json
              {
              "question": "Capitale de la RDC?",
              "answer": "Kinshasa",
              "difficulty": 1,
              "category": 3
             }
        ```
7. `DELETE 'http://127.0.0.1:5000/questions/${id}'`

- Cet endpoint permet de supprimer une question à partir du ID de la question
- Request Arguments: « id » - entier
- Request body : None
- Response body : Message confirmation
      ```json
              {
              "message": "Question na pas été supprimé" 
             }
        ```
8. Error Handling
(#Udacity course)
Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
The API will return three error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Not Processable
500: Internal Server Error

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
