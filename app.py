from flask import Flask, render_template, request, session, jsonify
import random
app = Flask(__name__)
app.secret_key = 'secret_key_for_session'
TASKS = [
    {"word": "Девч_нка", "answer": "О"},
    {"word": "Медвеж_нок", "answer": "О"},
    {"word": "Крюч_к", "answer": "О"},
    {"word": "Ж_лтого", "answer": "Ё"},
    {"word": "Ш_пот", "answer": "Ё"},
    {"word": "Ут_нок", "answer": "Ё"},
    {"word": "Мыш_нок", "answer": "О"},
    {"word": "Обожж_нный", "answer": "Ё"},
    {"word": "Сраж_нный", "answer": "Ё"},
    {"word": "Реш_нный", "answer": "Ё"}
]
@app.route('/')
def index():
    session.clear()
    session['score'] = 0
    session['used'] = []
    
    first_task = random.choice(TASKS)
    session['current'] = first_task
    session['used'].append(first_task)
    
    return render_template('index.html', 
                           word=first_task['word'], 
                           current_num=1, 
                           total=len(TASKS),
                           score=0)
@app.route('/check', methods=['POST'])
def check_answer():
    user_answer = request.json.get('answer')
    current_task = session.get('current')
    
    is_correct = (user_answer == current_task['answer'])
    
    if is_correct:
        session['score'] += 1
    
    next_task = None
    available = [t for t in TASKS if t not in session['used']]
    
    if available:
        next_task = random.choice(available)
        session['current'] = next_task
        session['used'].append(next_task)
    
    return jsonify({
        'correct': is_correct,
        'real_answer': current_task['answer'],
        'score': session['score'],
        'next_word': next_task['word'] if next_task else None,
        'current_num': len(session['used']),
        'total': len(TASKS)
    })
if __name__ == '__main__':
    app.run(debug=True, port=5001)












