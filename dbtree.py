from flask import Flask, render_template, jsonify, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Api, Resource

# Creating an app and connecting to database
app = Flask(__name__)
api = Api(app)
db_url = 'mysql://root:toor@localhost/DirectoryTree'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)

# This query will get immediate siblings of a given node.
siblings = (
    'select node.name, (COUNT(parent.name) - (sub_tree.depth+1)) as depth '
    'FROM dirs AS node, dirs AS parent, dirs AS sub_parent, '
    '(select node.name, (COUNT(parent.name) -1 ) as depth '
    'from dirs AS node, dirs AS parent '
    'WHERE node.lft BETWEEN parent.lft AND parent.rgt AND node.name="%s" '
    'group by node.name order by node.lft) as sub_tree '
    'where node.lft BETWEEN parent.lft '
    'and parent.rgt and node.lft between sub_parent.lft '
    'and sub_parent.rgt and sub_parent.name = sub_tree.name '
    'group by node.name having depth = 1 order by node.lft;'
)


# Serializing db query to a dictionary.
def siblings_dict(n):
    return {'name': n,
            'children': [
                {'name': k, 'children': []}
                for k, v in db.engine.execute(siblings % n)]}


# Return list of children's dictionaries.
def get_children(node):
            return [{'name': k,
                    'children': []}
                    for k, v in db.engine.execute(siblings % node)]

# build dictionary of all nodes.
def build_json(node):
    root = siblings_dict(node)
    if root['children'] != []:
        for c in root['children']:
            c['children'] = get_children(c['name'])
            build_json(c['name'])
    return root

# renders index page.
@app.route("/")
def hello():
    return render_template('index.html')

parser = reqparse.RequestParser()
parser.add_argument('prenode', type=str)
parser.add_argument('newnode', type=str)


# Shows tree structure and lets you delete the node.
class DirTree(Resource):
    def get(self, dirname):
        return build_json('root')

    def delete(self, dirname):
        delete_nodes = (
            "LOCK TABLE dirs WRITE; "
            "SELECT @myLeft := lft, @myRight := rgt, @myWidth := rgt - lft + 1 "
            "FROM dirs "
            "WHERE name = '%s'; "
            "DELETE FROM dirs WHERE lft BETWEEN @myLeft AND @myRight; "
            "UPDATE dirs SET rgt = rgt - @myWidth WHERE rgt > @myRight; "
            "UPDATE dirs SET lft = lft - @myWidth WHERE lft > @myRight; "
            "UNLOCK TABLES; "
        )
        db.engine.execute(delete_nodes % dirname)
        return build_json('root')


class AddNode(Resource):
    def get(self):
        return build_json('root')

    def post(self):
        args = parser.parse_args()
        add_node_below = (
            "LOCK TABLE dirs WRITE; "
            "SELECT @myLeft := lft FROM dirs "
            "WHERE name = '%s'; "
            "UPDATE dirs SET rgt = rgt + 2 WHERE rgt > @myLeft; "
            "UPDATE dirs SET lft = lft + 2 WHERE lft > @myLeft; "
            "INSERT INTO dirs(name, lft, rgt) "
            "VALUES('%s', @myLeft + 1, @myLeft + 2); "
            "UNLOCK TABLES "
        )
        db.engine.execute(add_node_below % (args['prenode'], args['newnode']))
        return redirect('/')
# Add endpoints for api with flask-restful.
api.add_resource(DirTree, '/tree/<dirname>')
api.add_resource(AddNode, '/tree/add')


if __name__ == "__main__":
    app.run(debug=True)
