# Bookshelf  


Bookshelf is a virtual bookshelf to store and rate your books. It was built as part of Udacity's fulls stack development nanodegree to practice API development skills. 

## Getting Started


### Pre-requisites and Local Development


Developers who wishes to work on this project should already have Python3, pip and node installed

#### Backend


From the backend folder, run ```bash pip install requirements.txt```. All required packages are included in the requirements file.

To run this application, run the following commands:
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

* ```bash export FLASK_APP=flaskr ``` this command will insure that Flask is going to use __init__.py in our flaskr folder.
* ```bash export FLASK_ENV=development ``` this command will insure that we will be working in development mode, which will show us an interactive debugger in the console and resart the server whenever a change is made.
* ```bash flask run ``` this command will start the application.

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

#### Frontend


From the frontend folder, run 
```bash
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on  http://127.0.0.1:3000/.


## API Reference


### Getting Started


Base URL: The application can only run on the localhost as it is not hosted yet:
http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

### Error Messages


Errors are returned as JSON objects in the following format:
```json
{
    'success': False,
    'message': 'Bad request',
    'error': 400
}
```

The API will return 4 possible error types when requests fail
Error code | Message
--- | --- 
400 | Bad request
404 | resource not found
405 | method not allowed
422 | resource unprocessable

### API Endpoints


#### GET /books


Expects: None
Returns: 
* A list of book objects, success value, and total number of books.
* Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1.

Sample: 
```curl
curl http://127.0.0.1:5000/books
```
```json
  "books": [
    {
      "author": "Stephen King",
      "id": 1,
      "rating": 5,
      "title": "The Outsider: A Novel"
    },
    {
      "author": "Lisa Halliday",
      "id": 2,
      "rating": 5,
      "title": "Asymmetry: A Novel"
    },
    {
      "author": "Kristin Hannah",
      "id": 3,
      "rating": 5,
      "title": "The Great Alone"
    },
    {
      "author": "Tara Westover",
      "id": 4,
      "rating": 5,
      "title": "Educated: A Memoir"
    },
    {
      "author": "Jojo Moyes",
      "id": 5,
      "rating": 5,
      "title": "Still Me: A Novel"
    },
    {
      "author": "Leila Slimani",
      "id": 6,
      "rating": 5,
      "title": "Lullaby"
    },
    {
      "author": "Amitava Kumar",
      "id": 7,
      "rating": 5,
      "title": "Immigrant, Montana"
    },
    {
      "author": "Madeline Miller",
      "id": 8,
      "rating": 5,
      "title": "CIRCE"
    }
  ],
"success": true,
"total_books": 18
}
```

#### POST /books


Creates a new book using the submitted title, author and rating. 
Expects: Book's title, author, and rating.
Returns: 
* A list of new book id, book objects, success value, and total number of books and book list based on current page number to update the frontend.
* Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1.

Sample: 
```curl
curl http://127.0.0.1:5000/books?page=3 -X POST -H "Content-Type: application/json" -d '{"title":"Neverwhere", "author":"Neil Gaiman", "rating":"5"}'
```
```json
{
"books": [
  {
    "author": "Neil Gaiman",
    "id": 24,
    "rating": 5,
    "title": "Neverwhere"
  }
],
"created": 24,
"success": true,
"total_books": 17
}
```

#### DELETE /books/{book_id}


Deletes the book of the given ID if it exists
Expects: None
Returns: 
* A list of deleted book id, book objects, success value, and total number of books and book list based on current page number to update the frontend.
* Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1.

Sample: 
```curl
curl -X DELETE http://127.0.0.1:5000/books/16?page=2
```
```json
{
"books": [
  {
    "author": "Gina Apostol",
    "id": 9,
    "rating": 5,
    "title": "Insurrecto: A Novel"
  },
  {
    "author": "Tayari Jones",
    "id": 10,
    "rating": 5,
    "title": "An American Marriage"
  },
  {
    "author": "Jordan B. Peterson",
    "id": 11,
    "rating": 5,
    "title": "12 Rules for Life: An Antidote to Chaos"
  },
  {
    "author": "Kiese Laymon",
    "id": 12,
    "rating": 1,
    "title": "Heavy: An American Memoir"
  },
  {
    "author": "Emily Giffin",
    "id": 13,
    "rating": 4,
    "title": "All We Ever Wanted"
  },
  {
    "author": "Jose Andres",
    "id": 14,
    "rating": 4,
    "title": "We Fed an Island"
  },
  {
    "author": "Rachel Kushner",
    "id": 15,
    "rating": 1,
    "title": "The Mars Room"
  }
],
"deleted": 16,
"success": true,
"total_books": 15
}
```

#### Patch /books/{book_id}


If provided, updates the rating of the specified book. 
Expects: Book's id
Returns: 
* Updated book id, success value.


Sample: 
```curl
curl http://127.0.0.1:5000/books/15 -X PATCH -H "Content-Type: application/json" -d '{"rating":"1"}'
```
```json
{ "id": 15, "success": true }
```