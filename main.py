from flask import Flask, render_template, request, g

import tools
import config.questions as questions

from copy import deepcopy as cp

from collections import OrderedDict

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

# TODO: Enforce a login
@app.route('/api/set_current_question', methods=['POST', 'GET'])
@tools.api_response
@tools.requires_args(required_args=['question_id'])
def api_set_current_question(data):
    if 'question_id' not in data or not tools.is_int(data['question_id']) \
                or int(data['question_id']) < -1 or \
                int(data['question_id']) >= len(app.questions):
        return tools.gen_result_failure('Invalid question ID.')
    else:
        app.show_answer = False
        app.current_question = int(data['question_id'])
        return tools.gen_result_success(message='Success.')

@app.route('/api/set_show_answer', methods=['POST', 'GET'])
@tools.api_response
@tools.requires_args(required_args=['show'])
def api_set_show_answer(data):
    app.show_answer = data['show'] == 'true'
    return tools.gen_result_success(message='Success.')

# TODO: use standard success/failure + data api format
@app.route('/api/current_question', methods=['GET', 'POST'])
@tools.api_response
def api_current_question():
    return {'current_question': app.current_question}

def get_question(question_id):
    question = cp(app.questions[question_id])
    question.pop('answer', None)
    return question

@app.route('/api/get_question', methods=['GET', 'POST'])
@tools.api_response
@tools.disabled
@tools.requires_args(required_args=['question_id'])
def api_get_question(data):
    if 'question_id' not in data or not tools.is_int(data['question_id']) \
                or int(data['question_id']) < 0 or \
                int(data['question_id']) >= len(app.questions):
        return tools.gen_result_failure('Invalid question ID.')
    return tools.gen_result_success(data=get_question(int(data['question_id'])))

@app.route('/api/get_current_question', methods=['GET', 'POST'])
@tools.api_response
def api_get_current_question():
    if app.current_question != -1:
        return tools.gen_result_success(data=get_question(app.current_question))
    else:
        return tools.gen_result_failure(message='No active question.')

def get_answer(question_id):
    question = app.questions[question_id]
    return {'choice': question['answer']}

@app.route('/api/get_current_answer', methods=['GET', 'POST'])
@tools.api_response
def api_get_current_answer():
    if app.current_question == -1:
        return tools.gen_result_failure(message='No active question.')
    elif app.show_answer:
        return tools.gen_result_success(data=get_answer(app.current_question))
    else:
        return tools.gen_result_failure(message='Answer not available yet!')

def set_up_jinja():
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

if __name__ == '__main__':
    set_up_jinja()
    app.questions = questions.questions
    app.current_question = -1
    app.show_answer = False
    app.config.from_pyfile('config/config.py')
    import config.config as config
    if hasattr(config, 'HOST') and hasattr(config, 'PORT'):
        app.run(host=config.HOST, port=config.PORT)
    else:
        app.run()