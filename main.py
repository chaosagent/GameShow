from flask import Flask, render_template, request, g

import tools
import questions

app = Flask(__name__)

@app.route('/')
def page_main():
    return render_template('index.html')

@app.route('/addstuff')
def page_add():
    return 'Hi'

@app.route('/control', methods=['GET', 'POST'])
def page_control():
    # if request.method == 'GET':
    return render_template('control.html')
    """elif request.method == 'POST':
        # TODO: AJAX this
        if 'question_id' not in request.form or not tools.is_int(request.form['question_id']) \
                or int(request.form['question_id']) >= len(app.questions):
            g.success = False
            g.message = 'Invalid question id.'
        else:
            app.current_question = int(request.form['question_id'])
            g.success = True
            g.message = 'Success.'
        return render_template('control.html')"""

# TODO: Enforce a login
@app.route('/api/set_current_question', methods=['POST', 'GET'])
@tools.api_response
@tools.requires_args(required_args=['question_id'])
def api_set_current_question(data):
    if 'question_id' not in data or not tools.is_int(data['question_id']) \
                or int(data['question_id']) < 0 or \
                int(data['question_id']) >= len(app.questions):
        return tools.gen_result_fail('Invalid question ID.')
    else:
        app.current_question = int(data['question_id'])
        return tools.gen_result_success(message='Success.')

@app.route('/api/current_question')
@tools.api_response
def api_current_question():
    return {'current_question': app.current_question}

@app.route('/api/get_question', methods=['GET', 'POST'])
@tools.api_response
@tools.requires_args(required_args=['question_id'])
def api_get_question(data):
    if 'question_id' not in data or not tools.is_int(data['question_id']) \
                or int(data['question_id']) < 0 or \
                int(data['question_id']) >= len(app.questions):
        return tools.gen_result_fail('Invalid question ID.')
    return tools.gen_result_success(data=app.questions[int(data['question_id'])])

def set_up_jinja():
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

if __name__ == '__main__':
    set_up_jinja()
    app.current_question = -1
    app.questions = questions.questions
    app.run(host='0.0.0.0', port=5001, debug=True)