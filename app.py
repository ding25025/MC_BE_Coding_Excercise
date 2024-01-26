"""app function."""
from flask import Flask
from flask import Blueprint
from flasgger import Swagger
from swagger_ui_bundle import swagger_ui_path
from src.task import task_bp

swagger_bp = Blueprint(
    "swagger_ui",
    __name__,
    static_url_path="/MC_Coding",
    static_folder=swagger_ui_path,
    template_folder=swagger_ui_path,
)

app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "MC_BE_Coding_Excercise API",
    "description": "MC_BE_Coding_Excercise API",
    "version": "0.0.1",
    "termsOfService": "",
    "hide_top_bar": True,
}

Swagger(app)

app.register_blueprint(task_bp, url_prefix="/task")


@app.route("/", methods=["GET"])
def welcome():
    return "Hello World!"


if __name__ == "__main__":
    app.run("0.0.0.0", port=5002, debug=True)
