from flask import Flask
from flask_restful import Api
from resources.saphetor.saphetor import Saphetor
from environs import Env


env = Env()
env.read_env("src/config/.env")
app = Flask(__name__)
app.config["SECRET_KEY"] = env.str("SECRET_KEY")
api = Api(app)


api.add_resource(Saphetor, '/saphetor/getRow/<string:row_id>', endpoint='saphetor')
api.add_resource(Saphetor, '/saphetor/getPaginatedData', endpoint='saphetor_all')
api.add_resource(Saphetor, '/saphetor/addRow', endpoint='saphetor_add')
api.add_resource(Saphetor, '/saphetor/updateRow/<string:row_id>', endpoint='saphetor_update')

if __name__ == '__main__':
    app.run(debug=True)
