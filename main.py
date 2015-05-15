from flask import Flask, render_template, request, g

import tools
import questions

app = Flask(__name__)

@app.route('/')
def page_main():
    return 'Hello World!'

@app.route('/addstuff')
def page_add():
    return 'Hi'

@app.route('/control', methods=['GET', 'POST'])
def page_control():
    if request.method == 'GET':
        return render_template('control.html')
    elif request.method == 'POST':
        if 'question_id' not in request.form or not tools.is_int(request.form['question_id']) \
                or int(request.form['question_id']) >= len(app.questions):
            g.success = False
            g.message = 'Invalid question id.'
        else:
            app.current_question = int(request.form['question_id'])
            g.success = True
            g.message = 'Success.'
        return render_template('control.html')

@app.route('/api/current_question')
@tools.response
def api_current_question():
    return {'current_question': app.current_question}

def set_up_jinja():
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

if __name__ == '__main__':
    set_up_jinja()
    app.current_question = -1
    app.questions = questions.questions
    app.run(host='0.0.0.0', port=5001, debug=True)