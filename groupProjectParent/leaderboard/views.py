from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Max
from .models import LeaderboardEntry
from .utils import update_badges
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
import json


@login_required(login_url='my-login')
@csrf_exempt
@require_POST
@login_required(login_url='my-login')
@csrf_exempt
@require_POST
def submit_unity_score(request):
    try:
        score = request.POST.get('score') or json.loads(request.body).get('score')

        # Create or update leaderboard entry
        entry, created = LeaderboardEntry.objects.get_or_create(
            user=request.user,
            game="Cycling",
            defaults={
                'score': int(score) * 6,
                'date': timezone.now()
            }
        )

        # Update score if new score is higher
        if not created and (int(score) * 6) > entry.score:
            entry.score = int(score)
            entry.date = timezone.now()
            entry.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Score submitted successfully'
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required(login_url='my-login')
def leaderboard_view(request):
    update_badges()
    games = ["Energy Conservation", "Recycling", "Cycling", "Quiz"]
    
    leaderboard_data = []
    
    users = User.objects.filter(leaderboardentry__isnull=False).distinct()
    for user in users:
        display_name = user.profile.display_name if user.profile.display_name else user.username
        user_row = {"display_name": display_name}
        overall = 0
        for game in games:
            best_score = LeaderboardEntry.objects.filter(user=user, game=game).aggregate(Max('score'))['score__max'] or 0
            user_row[game] = best_score
            overall += best_score
        user_row["overall"] = overall
        leaderboard_data.append(user_row)

    leaderboard_data.sort(key=lambda x: x["overall"], reverse=True)
    
    context = {
        "leaderboard_data": leaderboard_data,
        "games": games
    }
    return render(request, "leaderboards.html", context)
