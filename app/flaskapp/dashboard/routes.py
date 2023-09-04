from flask import Blueprint, render_template, url_for, flash, redirect, request
import requests
from flaskapp import app, apiurl, headers


dashboardObj = Blueprint('dashboard', __name__, template_folder='templates')

@dashboardObj.route('/', methods=['POST','GET'])
def dashboard():
    response = requests.get(apiurl+"/ls",headers=headers)
    json_response = response.json()
    len_emp_db = ""
    employeedb = ""
    if isinstance(json_response, list):
        employeedb = json_response
    else:
        len_emp_db = 0
    return render_template('dashboard/index.html',title='Dashboard', len_emp_db=len_emp_db, employee=employeedb)

# Delete Employee
@dashboardObj.route('/delete/<int:empid>', methods=['POST', 'GET'])
def delete(empid):
    send_data = {"empid":empid}
    response = requests.post(apiurl+"/delete",json=send_data,headers=headers)
    json_response = response.json()

    if json_response['status'] == "error":
        flash(f"{json_response['msg']}", 'danger')
    else:
        flash(f"{json_response['msg']}", 'success')
        return redirect(url_for('dashboard.dashboard'))