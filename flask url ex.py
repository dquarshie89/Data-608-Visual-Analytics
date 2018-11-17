import pandas as pd
import flask
from flask import jsonify

health_query = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=boroname,health,steward,count(tree_id)' +\
        '&$group=boroname,steward,health').replace(' ', '%20')

df = pd.read_json(health_query)

boros = pd.DataFrame(df["boroname"].unique())
boros=boros.values.tolist()

server = flask.Flask(__name__)

@server.route('/boros')
def return_complex():
    return jsonify(boros)


if __name__ == '__main__':
    server.run(debug=True)