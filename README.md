# SE568 - Stock Tracking and Prediction

## Environment
This project uses [Python3](https://www.python.org/downloads/) as the running environment.

## Running the Code
```buildoutcfg
git clone https://github.com/liuchengtian/SE568
cd SE568
pip install -r requirements.txt
python flask_starter.py
```

## Project Structure
### Folder Structure 
![alt text](https://github.com/liuchengtian/SE568/blob/master/folder_structure.png)

### 
* Web related:
1. controller.py defines the RESTful app routes and backend functions.
2. config.py stores the configuration shared by other fils.
3. rss.py gets the latest news from yahoo.
* Database related
1. fetch_data.py initializes the database and continuously fetches data from alpha vantage
api.
2. query_info.py uses SQL_Alchemy to query data from the sqlite database and returns to
controller.py.
3. data_manager.py and read_file.py define a class and reads csv.
4. StockTracking/database.db stores the user information.
5. StockTracking/backendserver/database_stock.db stores the stock information.
* Algorithm related
1. analyzer.py top module for algorthms like SVM and moving average.
2. bayesian.py, neural_networks.py define a Beyesian class and a neural network class.
3. macd.py and rsi.py returns technical indicators.

## Resource Used
### gentelella
[Gentelella Admin](https://github.com/puikinsh/gentelella) is a free to use Bootstrap admin template.
This template uses the default Bootstrap 3 styles along with a variety of powerful jQuery plugins and tools to create a powerful framework for creating admin panels or back-end dashboards.

Theme uses several libraries for charts, calendar, form validation, wizard style interface, off-canvas navigation menu, text forms, date range, upload area, form autocomplete, range slider, progress bars, notifications and much more.

We would love to see how you use this awesome admin template. You can notify us about your site, app or service by tweeting to [@colorlib](https://twitter.com/colorlib). Once the list will grown long enough we will write a post similar to [this](https://colorlib.com/wp/avada-theme-examples/) to showcase the best examples.

### flask
[Flask](https://github.com/pallets/flask) is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. It began as a simple wrapper around Werkzeug and Jinja and has become one of the most popular Python web application frameworks.

Flask offers suggestions, but doesn't enforce any dependencies or project layout. It is up to the developer to choose the tools and libraries they want to use. There are many extensions provided by the community that make adding new functionality easy.