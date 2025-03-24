from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from leaderboard.models import LeaderboardEntry
import random
import time

DEVICES = ["lamp", "bunny_light", "monitor", "headphones", "laptop", "lava_lamp", "mouse", "phone", "tablet"]
GAME_DURATION = 25
GAME_NAME = "Energy Conservation"

@login_required(login_url='my-login')
def index(request):
    """Initialize or restore game state."""
    if "game_state" in request.session:
        if request.session["game_state"]["status"] == False:
            del request.session["game_state"]

    if "game_state" not in request.session:
        states = {device: random.choice([True, False]) for device in DEVICES}
        threshold = 4
        current_on = sum(1 for s in states.values() if s)
        if current_on < threshold:
            off_devices = [device for device, s in states.items() if not s]
            random.shuffle(off_devices)
            needed = threshold - current_on
            for device in off_devices[:needed]:
                states[device] = True
        request.session["game_state"] = {
            "devices": states,
            "score": 25,
            "start_time": time.time(),
            "status" : True,
        }
    
    game_state = request.session["game_state"]
    elapsed_time = (time.time() - game_state["start_time"])

    elapsed_ms = round(elapsed_time * 1000)
 
    if all(not state for state in game_state["devices"].values()):
        final_score = round((game_state["score"] - elapsed_time) * 40)
        entry, created = LeaderboardEntry.objects.get_or_create(
            user=request.user,
            game=GAME_NAME,
            defaults={'score': final_score, 'date': timezone.now()}
        )
        if not created and final_score > entry.score:
            entry.score = final_score
            entry.date = timezone.now()
            entry.save()
        game_state["status"] = False
        request.session["game_state"] = game_state
        return render(request, "EnergyConservationMinigame/win.html", {"score": final_score, "time_taken": elapsed_ms / 1000})

    if elapsed_time >= GAME_DURATION:
        game_state["status"] = False
        request.session["game_state"] = game_state
        return redirect("game_over")

    return render(request, "EnergyConservationMinigame/game.html", {"game": game_state, "time_left": round(GAME_DURATION - elapsed_time, 3)})

def toggle_device(request, device_name):
    """Turn on/off a device."""
    game_state = request.session.get("game_state", {})

    if device_name in game_state["devices"]:
        game_state["devices"][device_name] = not game_state["devices"][device_name]

    request.session["game_state"] = game_state
    return redirect("EnergyConservationMinigame_home")

def reset_game(request):
    """Resets the game by clearing the session and redirecting to a new game session."""
    if "game_state" in request.session:
        del request.session["game_state"]
    return redirect("EnergyConservationMinigame_home")

def game_over(request):
    """Show game over screen when time runs out."""
    return render(request, "EnergyConservationMinigame/game_over.html")
