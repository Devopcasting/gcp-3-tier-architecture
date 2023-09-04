from flask import Blueprint, render_template, url_for, flash, redirect
import requests
from flaskapp import app, apiurl, headers
from flaskapp.add.forms import EmployeeFrom

addObj = Blueprint('add', __name__, template_folder='templates')

@addObj.route('/add', methods=['POST', 'GET'])
def add():
    form = EmployeeFrom()
    if form.validate_on_submit():
        send_data = {"Name":form.emp_name.data,"Email":form.email.data, "Department": form.department.data}
        response = requests.post(apiurl+"/add",json=send_data,headers=headers)
        json_response = response.json()

        if json_response['status'] == "error":
            flash(f"{json_response['msg']}", 'danger')
        else:
            flash(f"{json_response['msg']}", 'success')
            return redirect(url_for('dashboard.dashboard'))
    return render_template('add/add.html', title="Add Employee", form=form)