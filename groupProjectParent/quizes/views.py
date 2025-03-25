from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from .models import Quiz, Question, Result
from django.utils import timezone
from django.db.models import F
from leaderboard.models import LeaderboardEntry
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

def superuser_required(view_func):
    decorated_view = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view

@superuser_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})
@login_required(login_url='my-login')
def quiz_data(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = []
    for q in quiz.get_questions():
        answers = [a.text for a in q.get_answers()]
        questions.append({"question": q.text, "answers": answers})
    return JsonResponse({'quiz': quiz.title, 'questions': questions})
@login_required(login_url='my-login')
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.get_questions()
    return render(request, 'quiz_detail.html', {'quiz': quiz})


@csrf_exempt
def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        data = json.loads(request.body)
        score = 0
        time_taken = data.get("time_taken", 0)  #Get time from frontend

        for question_id, selected_answer_id in data.get("answers", {}).items():
            question = get_object_or_404(Question, id=question_id, quiz=quiz)
            answers = list(question.get_answers())  #Get all answers

            #Find the correct answer object
            correct_answer = next((ans for ans in answers if ans.correct), None)

            if correct_answer and int(correct_answer.id) == int(selected_answer_id):
                score += 1
                print("jesus")

            print(correct_answer.id if correct_answer else None)
            print(selected_answer_id)
            print("run")


        game_name = "Quiz"
        score2 = score*(150-time_taken)
        entry, created = LeaderboardEntry.objects.get_or_create(
            user=request.user,
            game=game_name,
            defaults={'score': score2, 'date': timezone.now()}
        )
        if not created and score > entry.score:
            entry.score = score
            entry.date = timezone.now()
            entry.save()

        return JsonResponse({'score': score, 'time_taken': time_taken})  # Return time_taken
