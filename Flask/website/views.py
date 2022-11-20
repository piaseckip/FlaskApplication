from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    request,
    send_from_directory,
    jsonify,
    Response,
    Flask,
)
from flask_pymongo import PyMongo, ObjectId
from pymongo import MongoClient
import os
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import time

views = Blueprint("views", __name__)
MONGODB_URI = os.environ.get("MONGODB_URI")
client = MongoClient(str(MONGODB_URI))
db = client.flask_db
techs = db.techs

_INF = float("inf")

graphs = {}
graphs["c"] = Counter(
    "python_request_operations_total", "The total number of processed requests"
)
graphs["h"] = Histogram(
    "python_request_duration_seconds",
    "Histogram for the duration in seconds.",
    buckets=(1, 2, 5, 6, 10, _INF),
)


@views.route("/favicon.ico")
def favicon():

    start = time.time()
    graphs["c"].inc()

    end = time.time()
    graphs["h"].observe(end - start)

    return send_from_directory(
        os.path.join(views.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@views.route("/", methods=["GET"])
def home():

    start = time.time()
    graphs["c"].inc()

    elem_count = techs.count_documents({})

    if elem_count <= 4:
        row_count = 1
    elif elem_count > 4 and elem_count % 4 == 0:
        row_count = elem_count / 4
    else:
        row_count = (elem_count // 4) + 1

    if elem_count <= 4:
        col_count = elem_count
    else:
        col_count = 4

    data = techs.find()
    table = []
    for record in data:
        table.append(record)

    end = time.time()
    graphs["h"].observe(end - start)

    return render_template(
        "index.html", ec=elem_count, rc=row_count, data=table, cc=col_count
    )


@views.route("/adding", methods=["POST", "GET"])
def adding():

    start = time.time()
    graphs["c"].inc()

    if request.method == "POST":
        name = request.form["tech_name"]
        descr = request.form["tech_descr"]
        link = request.form["image_link"]
        if techs.count_documents({"name": name}) != 0:

            end = time.time()
            graphs["h"].observe(end - start)

            return redirect(
                url_for(
                    "views.action",
                    title="Adding",
                    header="We can't perform that action",
                    paragraph="Record with that name exists.",
                )
            )
        else:
            techs.insert_one({"name": name, "descr": descr, "link": link})
            end = time.time()
            graphs["h"].observe(end - start)
            return redirect(
                url_for(
                    "views.action",
                    title="Adding",
                    header="Element succesfully added",
                    paragraph="You can check it on the home page!",
                )
            )
    elif request.method == "GET":
        end = time.time()
        graphs["h"].observe(end - start)
        return render_template("adding.html")


@views.route("/deleting", methods=["POST", "GET"])
def deleting():
    start = time.time()
    graphs["c"].inc()
    if request.method == "POST":
        name = request.form["tech_name"]
        if techs.count_documents({"name": name}) != 0:
            techs.delete_one({"name": name})
            end = time.time()
            graphs["h"].observe(end - start)
            return redirect(
                url_for(
                    "views.action",
                    title="Delete",
                    header="Element succesfully deleted",
                    paragraph="You can check it on the home page!",
                )
            )
        else:
            end = time.time()
            graphs["h"].observe(end - start)
            return redirect(
                url_for(
                    "views.action",
                    title="Delete",
                    header="There is no element with that name!",
                    paragraph="Check if u provided correct name",
                )
            )
    elif request.method == "GET":
        end = time.time()
        graphs["h"].observe(end - start)
        return render_template("deleting.html")


@views.route("/edit", methods=["POST", "GET"])
def edit():
    start = time.time()
    graphs["c"].inc()
    if request.method == "POST":
        name = request.form["tech_name"]
        if techs.count_documents({"name": name}) != 0:
            data = techs.find({"name": name})
            table = []
            for record in data:
                table.append(record)
            end = time.time()
            graphs["h"].observe(end - start)
            return redirect(
                url_for(
                    "views.editing",
                    id=table[0]["_id"],
                    name=table[0]["name"],
                    descr=table[0]["descr"],
                    link=table[0]["link"],
                )
            )
        else:
            end = time.time()
            graphs["h"].observe(end - start)
            return redirect(
                url_for(
                    "views.action",
                    title="Edit",
                    header="There is no element with that name!",
                    paragraph="Check if u provided correct name",
                )
            )
    elif request.method == "GET":
        end = time.time()
        graphs["h"].observe(end - start)
        return render_template("edit.html")


@views.route("/editing", methods=["POST", "GET"])
def editing():
    start = time.time()
    graphs["c"].inc()
    if request.method == "POST":
        id = request.form["id"]
        name = request.form["name"]
        descr = request.form["descr"]
        link = request.form["link"]
        techs.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": {"name": name, "descr": descr, "link": link}},
        )
        end = time.time()
        graphs["h"].observe(end - start)
        return redirect(
            url_for(
                "views.action",
                title="Edit",
                header="Element succesfully edited",
                paragraph="You can check it on the home page!",
            )
        )
    elif request.method == "GET":

        id = request.args["id"]
        name = request.args["name"]
        descr = request.args["descr"]
        link = request.args["link"]
        end = time.time()
        graphs["h"].observe(end - start)
        return render_template("editing.html", id=id, name=name, descr=descr, link=link)


@views.route("/action")
def action():
    start = time.time()
    graphs["c"].inc()
    title = request.args["title"]
    header = request.args["header"]
    paragraph = request.args["paragraph"]
    end = time.time()
    graphs["h"].observe(end - start)
    return render_template("action.html", t=title, h=header, p=paragraph)


@views.route("/tech")
def tech():
    start = time.time()
    graphs["c"].inc()
    title = request.args["h"]
    descr = request.args["des"]
    image = request.args["img"]
    end = time.time()
    graphs["h"].observe(end - start)
    return render_template("tech.html", h=title, des=descr, img=image)


@views.route("/metrics")
def requests_count():
    res = []
    for k, v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")
