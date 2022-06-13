from flask import Flask, request
from google_parser import GoogleParser
import json

app = Flask(__name__)
parser = GoogleParser()

@app.route('/api/search/<q>')
def search(q):
    if q is None:
        return '{\"result\": \"\'q\' is required parameter\"}'
    
    try:
        count = 10 if request.args.get('count') is None else int(request.args.get('count'))
        start = 1 if request.args.get('start') is None else int(request.args.get('start'))
        return app.response_class(
            response=json.dumps(
                parser.search(q, count, start),
                indent=4,                
                ensure_ascii=False
            ),
            status=200,
            mimetype='application/json'
        )        
    except Exception as e:
        print(e)
        return app.response_class(
            response=json.dumps(
                {
                    'error': 'Unexpected error occured'
                },
                indent=4
            ),
            status=200,
            mimetype='application/json'
        )

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)