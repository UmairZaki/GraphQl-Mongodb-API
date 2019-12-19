import graphene
from flask import Flask, request, jsonify, json
from flask_graphql import GraphQLView
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://umair:fabeha123@flaskapp-mteqh.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)

class Task_items(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String(name=graphene.String(default_value="Task"))
    description = graphene.String(required=True)
    done = graphene.Boolean(status=graphene.Boolean(default_value=False))

    def task(self, args):
        myTask = mongo.db.myTask
        match=myTask.find()
        fields = [Task_items(id=match['id'], description=match['description'], title=match['title'],done=match['done']) for todo in match]
        return jsonify(fields)

class Query_items(graphene.ObjectType):
    todo_items = graphene.List(Task_items)
    todo_item = graphene.Field(Task_items, id=graphene.Int())

    def resolve_fields(self, args):
        myTask = mongo.db.myTask
        match = myTask.find()
        fields = [Task_items(id=match['id'], description=match['description'], title=match['title'],done=match['done']) for todo in match]
        return jsonify(fields)

schema = graphene.Schema(query=Query_items)

app.add_url_rule('/', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


app.run(debug=True)