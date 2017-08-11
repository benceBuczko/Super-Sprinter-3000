from flask import Flask, render_template, redirect, request, session
import csv
import random

app = Flask(__name__)


def id_generator():
    data = open_file()
    while True:
        generated = ""
        for i in range(2):
            generated = generated + random.choice('0123456789')
        if generated in data:
            continue
        else:
            return generated


def open_file():
    data = []
    with open("data.csv", "r") as datafile:
        file = csv.reader(datafile, delimiter=",")
        for row in file:
            data.append(row)
    return data


@app.route('/')
def route_list():
    return render_template('list.html', data=open_file())


@app.route('/new-story')
def route_edit():
    return render_template('form.html', list=["", "", "", "", "", "", ""], button="Create", URL="/save-story",
                           title="Super Sprinter 3000 - Add new Story", header="User Story Manager - Add new story")


@app.route('/delete-story', methods=["POST"])
def route_delete():
    data = open_file()
    for list in data:
        if list[0] == request.form["delete"]:
            data.remove(list)
    with open("data.csv", "w") as datafile:
        file = csv.writer(datafile, delimiter=",")
        for i in data:
            file.writerow(i)
    return redirect("/")


@app.route('/update-story', methods=["POST"])
def route_update():
    data = open_file()
    for list in data:
        if list[0] == request.form["update"]:
            k = list
    return render_template('form.html', list=k, button="Update", URL="/save-update",
                           title="Super Sprinter 3000 - Edit Story", header="User Story Manager - Edit story")


@app.route('/save-update', methods=["POST"])
def route_updatesave():
    print('POST request received!')
    data = []
    data.append(request.form["id"])
    data.append(request.form["title"])
    data.append(request.form["userstory"])
    data.append(request.form["criteria"])
    data.append(request.form["businessvalue"])
    data.append(request.form["estimation"])
    data.append(request.form["status"])
    data2 = open_file()
    for list in data2:
        if list[0] == request.form["id"]:
            for i in range(len(list)):
                list[i] = data[i]
    with open("data.csv", "w") as datafile:
        file = csv.writer(datafile, delimiter=",")
        for i in data2:
            file.writerow(i)
    return redirect("/")


@app.route('/save-story', methods=['POST'])
def route_save():
    print('POST request received!')
    data = []
    data.append(id_generator())
    data.append(request.form["title"])
    data.append(request.form["userstory"])
    data.append(request.form["criteria"])
    data.append(request.form["businessvalue"])
    data.append(request.form["estimation"])
    data.append(request.form["status"])
    with open("data.csv", "a") as datafile:
        file = csv.writer(datafile, delimiter=",")
        file.writerow(data)
    return redirect('/')

if __name__ == "__main__":
    app.secret_key = "123"
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )