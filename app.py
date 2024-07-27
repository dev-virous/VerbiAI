from webservice import routes, render_template, Response, request
from Translation import model
from json import dumps
import os, yaml
os.system("cls")


@routes.get("/")
def home():
    return render_template("index.html")

@routes.route("/swagger.yaml")
def swagger():
    with open("swagger.yaml", "r") as file:
        swagger_data = yaml.safe_load(file)
    swagger_yaml = yaml.dump(swagger_data)
    return Response(swagger_yaml, mimetype='text/yaml')

@routes.post("/translator")
def translator():
    query = request.json.get("query")
    from_lang = request.json.get("query.source_language")
    to_lang = request.json.get("query.target_language")
    if not query:
        data = {
            "success": False,
            "Exception": {
                "code": 400,
                "ErrorMsg": "Request contains an invalid argument.",
            }
        }
        return dumps(data, indent=4, ensure_ascii=False), 400, {"Content-Type": "application/json; charset=utf-8"}
    elif not to_lang:
        data = {
            "success": False,
            "Exception": {
                "code": 400,
                "ErrorMsg": "Request contains an invalid argument.",
                }
            }
        return dumps(data, indent=4, ensure_ascii=False), 400, {"Content-Type": "application/json; charset=utf-8"}
    else:
        translate = model.translate(
            query=query,
            target_language_code=to_lang,
            source_language_code=from_lang
        )
        data = {
            "success": True,
            "sentences": {
                "trans": translate,
                "original": query,
            }
        }
        if not from_lang:
            data["sentences"]["detection_lang"] = model.detection_lang
        return dumps(data, indent=4, ensure_ascii=False), {"Content-Type": "application/json; charset=utf-8"}

@routes.get("/get_langs")
def get_langs():
    return dumps(model.get_langs(), indent=4, ensure_ascii=False), {"Content-Type": "application/json; charset=utf-8"}

routes.run()