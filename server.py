from flask import Flask, request, jsonify, render_template
from helper import getBooks, uploadRss
import os
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv()
FLASK_ENV = os.environ.get('FLASK_ENV',"dev")
@app.route('/')
def index():
    # Render the index.html template on accessing the root endpoint
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    title = request.args.get('title', '',type=str)

    if not title:
        return jsonify({'error': 'Missing book title'}), 400

    search_results = getBooks(title)
    print(search_results)
    return render_template("book_info.html", books=search_results)



@app.route('/upload', methods=['POST'])
def upload():
    rss_url = request.form.get("rss_url",'',type=str)
    title = request.form.get("title",'',type=str)
    app.logger.info(f"{rss_url},{title}")
    result = uploadRss(rss_url,title)
    if(result['status'] == 'ok'):
        return render_template("link.html",url = result['url'])
    else:
        return render_template("error.html",error = result['message'])
if __name__ == '__main__':
    app.run(threaded = True, debug = FLASK_ENV=='dev')
