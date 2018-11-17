import dash
from flask import Flask, jsonify

server = Flask(__name__)

app = dash.Dash(__name__, server=server, url_base_pathname='/dashapp')

# This is a hello world flask api.
# visit localhost:5000/hello in a browser to see what gets returned
@server.route('/hello', methods=['GET'])
def return_hello():
    return jsonify({'hello': 'world'})


# This is a more complex API who's returned information depends on a variable
# from the URL.
# visit localhost:5000/complex/foo to see what gets returned. Replace
# foo with other words to verify the API is reponding to that variable.
@server.route('/complex/<string:word>')
def return_complex(word):
    return jsonify({'complex': word})


if __name__ == '__main__':
    server.run(debug=True)