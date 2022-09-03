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

- [python-dotenv] is teh python library we use to handle sensitive information like db username and password. These are stored in a separate .env file under the project root directory. Usually not added to git. Please create your own .env file with the key:value pairs `DBUSR:Your_db_user` and `DBPW:Your_db_password`. (I have included the .env file with project for evaluation purposes)

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

### API Endpoint Documentation

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Sample Request
  ```
  curl -X get http://localhost:5000/categories
  ```
- Sample Response
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

`GET '/questions'`

- Fetches a dictionary of questions from all categories from teh database.
- Request Arguments: page: Optional argument. Passed to specify the page number to be retrieved.
- Returns: An object with keys, 
  - `categories`, that contains an object of `id: category_string` key: value pairs,
  - `current_category`, that contains None as value,
  - `questions`, that contains an object of  10 items with {`id: question_id`, `question: question_string`, `difficulty: difficulty_value`, `category: category_id`, `answer: answer_string` } key: value pairs,
  - `success` set to True,
  - `total_questions`, that contains the count of questions present in the database
- Sample Request
  ```
  curl -X get http://localhost:5000/questions
  ```
- Sample Response
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
    "current_category": null,
    "questions": [
      {
        "answer": "Tom Cruise",
        "category": 5,
        "difficulty": 4,
        "id": 4,
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
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
        "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
      },
      {
        "answer": "Mona Lisa",
        "category": 2,
        "difficulty": 3,
        "id": 17,
        "question": "La Giaconda is better known as what?"
      }
    ],
    "success": true,
    "total_questions": 20
  }

  ```

`DELETE '/questions/<int:qn_id>'`

- Deletes the question with given question id from the database.
- Request Arguments: qn_id: The id of the question to be deleted from the database.
- Returns: An object with keys, 
  - `deleted`, that contains the id of the deleted question
  - `success`, set to true
  - `total_questions`, that contains the count of questions currently in the database.
- Sample Request
  ```
  curl -X delete http://localhost:5000/questions/2
  ```
- Sample Response
  ```json
  {
    "deleted": 31,
    "success": true,
    "total_questions": 19
  }

  ```

`POST '/questions'` - To post a new question.

- Posts a new quesiton to the database (or) fetches the questions from the database if searchTerm is given.
- Request Arguments:
  - `question`: The question string to be added
  - `category`: The category id of question to be added. Integer.
  - `difficulty`: The difficulty level of question to be added. Integer.
  - `answer`: The answer string for the question to be added. 
- Returns: An object with keys, 
  - `created`, that contains the id of the created question
  - `questions`, List of ten questions from the database
  - `success`, set to true
  - `total_questions`, that contains the count of questions currently in the database.
- Sample request: 
  ```  
    curl -X POST http://localhost:5000/questions -H "Content-type: application/json" -d "{\"question\":\"My sample question\",\"category\": 1,\"difficulty\":2,\"answer\":\"my sample answer\" }" 
    ```
- Sample Response
    ```json
      {
        "created": 32,
        "questions": [
          {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
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
            "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
          },
          {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
          }
        ],
        "success": true,
        "total_questions": 20
      }
    ```

`POST '/questions'` - To Search questions.

- Fetches the questions from the database based on the searchTerm given.
- Request Arguments:
  - `searchTerm`: The search key for the questions to be fetched from the database.Only given if the endpoint is hit to perform a search operation. Do not provide if POST new question operation is performed. 
- Returns: An object with keys, 
    - `current_category`, set to None
    - `questions`, List of questions that match the searchterm from the database
    - `success`, set to true
    - `total_questions`, that contains the count of questions fetched from the database.
- Sample request: 
    ```  
    curl -X POST http://localhost:5000/questions -H "Content-type: application/json" -d "{ \"searchTerm\":\"medicine\" }"
    ```
- Sample Response
    ```json
    {
      "current_category": null,
      "questions": [
        {
          "answer": "Blood",
          "category": 1,
          "difficulty": 4,
          "id": 22,
          "question": "Hematology is a branch of medicine involving the study of what?"
        }
      ],
      "success": true,
      "total_questions": 1
    }
    ```
`GET '/categories/<cat_id>/questions'`

- Fetches a dictionary of questions from given category from the database
- Request Arguments: page: Optional argument. Passed to specify the page number to be retrieved.
- Returns: An object with keys, 
  - `current_category`, that contains Current category id as value,
  - `questions`, that contains an object of ten items with {`id: question_id`, `question: question_string`, `difficulty: difficulty_value`, `category: category_id`, `answer: answer_string` } key: value pairs,
  - `success` set to True,
  - `total_questions`, that contains the count of questions in given category present in the database
- Sample request: 
    ``` 
     curl http://localhost:5000/categories/1/questions
     ```
- Sample Response
    ```json
      {
      "current_category": "Science",
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
        },
        {
          "answer": "Phantom Galaxy (M74)",
          "category": 1,
          "difficulty": 3,
          "id": 28,
          "question": "What is the name of the Galaxy revealed by James Webb?"
        },
        {
          "answer": "my sample answer",
          "category": 1,
          "difficulty": 2,
          "id": 32,
          "question": "My sample question"
        }
      ],
      "success": true,
      "total_questions": 5
    }
    ```
`POST '/quizzes'`

- Fetches a question from given category from the database
- Request Arguments: 
  - previous_questions: List of question ids previously retrieved in the current quiz.
  - quiz_category: Dictionary with {`type: category_type`,`id: category_id`} as key:value pairs.
- Returns: A object with keys, 
  - `question`, that contains an object with {`id: question_id`, `question: question_string`, `difficulty: difficulty_value`, `category: category_id`, `answer: answer_string` } key: value pairs,
  - `success` set to True
- Sample request:
  ```
  curl -X POST "http://127.0.0.1:5000/quizzes" -d "{\"quiz_category\":{\"type\": \"Sports\", \"id\": \"4\"},\"previous_questions\":[2]}" -H "Content-Type: application/json"
  ```
- Sample response:
  ```json
  {
      "question": {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    "success": true
  }
  ```





## Errors

-  400
    -   Description - The error code 400 is thrown for Bad request
    -   Response Json
        -   Response code: 400
        -   Message: Bad Request
        -   Success: False
-   404
    -   Description - The error code 404 is thrown if requested resource is not available
    -   Response Json
        -   Response code: 404
        -   Message: Respurce not found
        -   Success: False
-   405
    -   Description - The error code 405 is thrown for when request Method is not allowed
    -   Response Json
        -   Response code: 405
        -   Message: Method not Allowed
        -   Success: False
-   422
    -   Description - The error code 422 is thrown for Unprocessable request
    -   Response Json
        -   Response code: 422
        -   Message: Unprocessable
        -   Success: False


## Testing


To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
