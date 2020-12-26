import helper
from flask import Flask, request, jsonify, render_template, url_for, Response, redirect
import json

app = Flask(__name__)

if __name__ == "main":
    app.run(debug=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/print')
def printMsg():
    app.logger.warning('testing warning log')
    app.logger.error('testing error log')
    app.logger.info('testing info log')
    return "Check your console"

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/todolist')
def todolist():
    var1 = get_all_items()
    #parsedData = json.parse(var1);
    return render_template("todolist.html", complete=var1)

@app.route('/item/new', methods=['POST'])
def add_item():
    # Get item from the POST body
    req_data = request.form
    app.logger.warning("=========HI")
    app.logger.warning(request)
    app.logger.warning("=========FORM")
    app.logger.warning(request.form)
    app.logger.warning("=========vALUES")
    app.logger.warning(request.values)
    app.logger.warning(req_data)
    #item = req_data.values()[1]
    item = req_data['item']

    # Add item to the list
    res_data = helper.add_to_list(item)

    # Return error if item not added
    if res_data is None:
        response = Response("{'error': 'Item not added - " + item + "'}", status=400 , mimetype='application/json')
        #return response
    	return redirect(url_for('todolist'))

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    #return response
    return redirect(url_for('todolist'))


@app.route('/items/all')
def get_all_items():
    # Get items from the helper
    res_data = helper.get_all_items()

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response
    #return res_data

@app.route('/item/status', methods=['GET'])
def get_item():
    # Get parameter from the URL
    item_name = request.args.get('name')

    # Get items from the helper
    status = helper.get_item(item_name)

    # Return 404 if item not found
    if status is None:
        response = Response("{'error': 'Item Not Found - %s'}"  % item_name, status=404 , mimetype='application/json')
        return response

    # Return status
    res_data = {
        'status': status
    }

    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    return response

@app.route('/item/update', methods=['PUT'])
def update_status():
    # Get item from the POST body
    req_data = request.get_json()
    item = req_data['item']
    status = req_data['status']

    # Update item in the list
    res_data = helper.update_status(item, status)

    # Return error if the status could not be updated
    if res_data is None:
        response = Response("{'error': 'Error updating item - '" + item + ", " + status   +  "}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response

@app.route('/item/remove', methods=['POST'])
def delete_item():
    # Get item from the POST body
    req_data = request.form
    #print(req_data)
    item = req_data['item']

    # Delete item from the list
    res_data = helper.delete_item(item)

    # Return error if the item could not be deleted
    if res_data is None:
        response = Response("{'error': 'Error deleting item - '" + item +  "}", status=400 , mimetype='application/json')
        #return response
        return redirect(url_for('todolist'))


    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    #return response
    return redirect(url_for('todolist'))

