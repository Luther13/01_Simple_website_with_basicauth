#pd2.py
from flask import Flask, request, render_template, make_response,redirect, jsonify
from functools import wraps
pd2 = Flask(__name__)

real_username ='Akwarysta69'
real_password = 'J3si07r'
logged_in = ''
pass_in = ''
fishes_database = {}
id_number = 1


# Decorator
def check_for_login(in_function):
    @wraps(in_function)
    def checker(*args, **kwargs):
        if request.cookies.get('Logged') == 'Yes':
            return in_function(*args,**kwargs)
        else:
            return redirect("/")
    return checker


@pd2.route('/')
def nothing():
    return "Witam!"


# Task 1
@pd2.route('/login', methods=['POST'])
def login():
    global pass_in, logged_in, real_password, real_username
    if (request.authorization and request.authorization.username == real_username
            and request.authorization.password == real_password):
        logged_in = request.authorization.username
        pass_in = request.authorization.password
        resp = make_response(redirect(
            '/hello'
        ))
        resp.set_cookie('Logged', 'Yes')
        return resp

    return make_response('Niepoprawne dane!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


# Task 2
@pd2.route('/logout', methods=['POST'])
def logout():
    global logged_in
    resp = make_response(
        render_template(
            'logout.html', user = logged_in
        )
    )
    resp.set_cookie('Logged', 'No')
    return resp


# Task 3
@pd2.route('/hello')
@check_for_login
def hello():
    return render_template('hello.html', user=logged_in)


# Task 4
@pd2.route('/fishes', methods=['GET', 'POST'])
@check_for_login
def fishes():
    if request.method == 'GET':
        return get_fishes()
    elif request.method=='POST':
        return post_fishes()


def get_fishes():
    return jsonify(fishes_database)


def post_fishes():
    global id_number
    data = request.get_json()
    new_fish = {
        'who': data.get('who'),
        'where': data.get('where'),
        'mass': data.get('mass'),
        'length': data.get('length'),
        'kind': data.get('kind')
    }
    fish_id = f'id_{id_number}'
    id_number += 1
    fishes_database[fish_id] = new_fish
    return "Ok"


# Task 5
@pd2.route('/fishes/<id>', methods=['GET','DELETE','PUT','PATCH'])
@check_for_login
def fish(id):
    if request.method=='GET':
        return get_fish(id)
    elif request.method == 'DELETE':
        return delete_fish(id)
    elif request.method == 'PUT':
        return put_fish(id)
    elif request.method == 'PATCH':
        return patch_fish(id)


def get_fish(arg):
    return jsonify(fishes_database.get(arg))


def delete_fish(arg):
    del fishes_database[arg]
    return f'Usunieto rybe o id: {arg}'


def put_fish(arg):
    data = request.get_json()
    switch_fish = {
        'who': data.get('who'),
        'where': data.get('where'),
        'mass': data.get('mass'),
        'length': data.get('length'),
        'kind': data.get('kind')
    }
    fishes_database[arg] = switch_fish
    return "Ok"


def patch_fish(arg):
    data = request.get_json()
    for key in data.keys():
        fishes_database.get(arg)[key] = data.get(key)
        print(f'podmieniono {data.get(key)}')
    return "Podmiana udana"


if __name__ == '__main__':
    pd2.run(debug=True)