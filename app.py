import os
import pandas as pd
import tempfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, abort, session, redirect, url_for
from flask_cors import CORS
from main import main
from utils import automation_report, remove_files, create_dirs, MailSender
import secrets
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = secrets.token_urlsafe(16)
CORS(app)

# create directory for storing the user data
create_dirs([Path("client_bkt"), Path("client_bkt/ip"), Path("client_bkt/op")])

# api route for contact us automation
@app.route('/automate/contact_us', methods=['POST'])
def automate_contact_us():
    mail_sender = MailSender(os.environ.get("EMAIL"), os.environ.get("PASSKEY"))
    
    print(f"{session.get('user_email')}, {os.environ.get('EMAIL')}, {os.environ.get('PASSKEY')}, {os.environ.get('GECKO_DRIVER_PATH')}")
    
    try:
        file = request.files['csv']

        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', dir=Path('client_bkt/ip')) as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name
            print(temp_file_path)
    except Exception:
        return jsonify({'status':'fail', 'message': 'Error while writing the CSV file. Ensure it is a valid CSV file'}), 400

    # checks:
    #   - check 1: check sent file is in proper format encoding or not
    #   - check 2: checks all the required columns present or not in client file
    try:
        data = pd.read_csv(temp_file_path)
    except pd.errors.ParserError:
        return jsonify({'status':'fail', 'message': 'Error reading the CSV file. Ensure it is a valid CSV format.'}), 400
        
    required_columns = ["website", "First Name", "Last Name", "Phone Number", "Email", "Subject", "Comments"]
    # 406 [Not Acceptable]
    if not set(required_columns).issubset(set(data.columns)):
        return jsonify({'status':'fail', 'message': f"Error: Missing Required Columns\n\nThe CSV file you uploaded is missing some required columns\n\nPlease upload a CSV file containing the following columns:\n\nRequired Columns: {required_columns}"}), 406        

    result_filepath = main(filepath=temp_file_path, save_dir=Path("client_bkt/op"))
    # 500 [Internal Error] 
    if not result_filepath:
        mail_sender.send_mail(
            receiver=session.get("user_email", os.environ.get("EMAIL")),
            subject="Automation Report",
            body="""Dear user,\n\nInternal Server Error! We're unable to automate your form filling. Please try again later.\n\n\nThankyou\nQuantum IT Innovation\n(AI Team)""",
        )
        mail_sender.tear_down()
        return jsonify({'status':'fail', 'message': 'Internal server error! Failed to Automate the form filling.'}), 500
    
    mail_sender.send_mail(
        receiver=session.get("user_email", os.environ.get("EMAIL")),
        subject="Automation Report",
        body="""Dear user,\n\nPlease find your automation report below 👇.\n\n\nThankyou\nQuantum IT Innovation\n(AI Team)""",
        attachments_paths=[result_filepath]
    )
    mail_sender.tear_down()
    
    report = automation_report(filepath=result_filepath)

    # removes the stored client file
    try:
        remove_files([temp_file_path])
    except Exception as e:
        print(f"Error deleting files: {e}")

    if report:
        return jsonify({'status': 'success', 'message': 'Report generated successfully.', 'report': report, 'file': str(result_filepath)}), 200
    # 500 [Internal Error]
    else:
        return jsonify({'status': 'fail', 'message': 'Internal server error! Failed in Generating the Report'}), 500


# index/application route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_email = request.form.get('email')
        session['user_email'] = user_email
        return redirect(url_for('index'))
        
    email_flag = session.get('user_email', False)
    return render_template('index.html', email_flag=email_flag)


# route which sends the file as attachment
@app.route('/download/report/<filename>', methods=['GET'])
def send_report(filename):
    report_bkt = Path("client_bkt/op")
    filepath = report_bkt / filename    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return abort(404, description="File not found")
    
    
if __name__ == "__main__":
    app.run(debug=True)
        