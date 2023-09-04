from flask import Blueprint, render_template, url_for, flash, redirect, request
import requests
from flaskapp import app, apiurl, headers
from flaskapp.update.forms import UpdateEmployeeFrom

updateObj = Blueprint('update', __name__, template_folder='templates')

@updateObj.route('/update/<int:empid>', methods=['POST', 'GET'])
def update(empid):
    form = UpdateEmployeeFrom()
    send_data = {"empid":empid}
    response = requests.post(apiurl+"/getdata",json=send_data,headers=headers)
    json_response = response.json()
    
    if form.validate_on_submit():
        send_data = {"empid": empid, "name":form.emp_name.data, "department": request.form.get('select-department')}
        response = requests.post(apiurl+"/update",json=send_data,headers=headers)
        json_response = response.json()
        if json_response['status'] != "error":
            flash(f"{json_response['msg']}",'success')
        else:
            flash(f"{json_response['msg']}",'danger')

        return redirect(url_for('dashboard.dashboard'))
    return render_template('update/update.html', title="Update Employee Data", empconn=json_response, form=form)
