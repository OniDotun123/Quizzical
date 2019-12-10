from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from Quizzical.extensions import db
from Quizzical.models import Question, User



main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('home.html')



@main.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    if request.method == 'POST':
        question = request.form['question']
        expert = request.form['expert']

        question = Question(
            question=question, 
            expert_id=expert, 
            asked_by_id=current_user.id
        )
        
        db.session.add(question)
        db.session.commit()

        return redirect(url_for('main.index'))

    experts = User.query.filter_by(expert=True).all()

    context = {
        'experts' : experts
    }

    return render_template('ask.html', **context)





@main.route('/answer/<int:question_id>', methods=['GET', 'POST'])
def answer(question_id):
    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        question.answer = request.form['answer']
        db.session.commit()

        return redirect(url_for('main.unanswered'))
    
    context = {'question' : question}
    return render_template('answer.html', **context)














@main.route('/question')
def question():
    return render_template('/question.html')





@main.route('/unanswered')
@login_required
def unanswered():
    unanswered_questions = Question.query\
        .filter_by(expert_id=current_user.id)\
        .filter(Question.answer == None)\
        .all()

    context = {
        'unanswered_questions' : unanswered_questions
    }


    return render_template('/unanswered.html', **context)
    





@main.route('/users')
def users():
    return render_template('/users.html')

@main.route('/home')
def home():
    return render_template('/home.html')

