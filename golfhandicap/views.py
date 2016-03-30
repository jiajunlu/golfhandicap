from django.shortcuts import render

from .models import Score, Player, Game
from .forms import CalculateCourseHandicapForm
from operator import itemgetter

#  https://en.wikipedia.org/wiki/Handicap_(golf)
USGA_DIFFERENTIAL_SCHEDULE = [1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3,
                              4, 4, 5, 5, 6, 6, 7, 8, 9, 10]


def usga_handicap_formula(diff_list):
    """
    Get an average of the differentials used by adding them together and dividing by the number used
    (i.e., if five differentials are used, add them up and divide by five).
    Multiply the result by .96 (96-percent).
    Drop all the digits after the tenths (do not round off) and the result is handicap index.

        (Sum of differentials / number of differentials) x 0.96
    """
    return int(sum(diff_list) / float(len(diff_list)) * 0.96 * 10) / 10.0


def usga_handicap_index(round_list):
    """
    Determine how many differentials are being used. Not every differential that results
    from Step 1 will be used in the next step. If only five rounds are entered,
    only the lowest differential will be used.
    If 20 rounds are entered, only the 10 lowest differentials are used.

   """
    num_diff = len(round_list)
    diff_index = USGA_DIFFERENTIAL_SCHEDULE[num_diff]

    sorted_round_list = sorted(round_list, key=itemgetter('diff'))
    diff_list = []
    for i in range(diff_index):
        sorted_round_list[i]['used'] = True
        diff_list.append(sorted_round_list[i]['diff'])

    return usga_handicap_formula(diff_list)


def usga_handicap_differential(adjusted_score, course_handicap, course_slope):
    """
    Calculate the handicap differential for each round by using the USGA Course Ration and Slope Rating
    for the courses played.
    That formula is HCP Dif = (Adjusted Score - Course Handicap Rating) x 113 / Slope Rating.
    For example, the score is 75, the course rating is 71.2 and the slope is 130,
    so the formula will look like (75 - 71.2) x 113/130.
    Repeat this step differential for each round.
    """
    handi = (adjusted_score - course_handicap) * 113 / course_slope
    return int(handi * 10 + 0.5) / 10.0


def usga_course_handicap(slope, user_handicap):
    """
    """
    course_handicap = slope * user_handicap / 113.0
    return int(course_handicap + 0.5)


def index(request):
    return allplayers(request)


def allplayers(request):
    players = Player.objects.all()
    course_handi = False
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CalculateCourseHandicapForm(request.POST)
        if form.is_valid():
            course_handi = True
    else:
        form = CalculateCourseHandicapForm()
        form.course_slope = 113

    output = []
    for player in players:
        p = {'nick_name': player.nick_name}

        scores = Score.objects.filter(player_id=player).order_by('-game__game_date')[:20]
        round_list = []
        for r in scores:
            round_dict = {'score': r.score, 'adjscore': r.adjusted_score, 'course': r.game.course,
                          'handicap': r.game.course_handicap, 'slope': r.game.course_slope,
                          'tee': r.game.get_tee_display(), 'play_date': r.game.game_date, '#': r.game.game_index}
            round_dict['diff'] = usga_handicap_differential(round_dict['adjscore'],
                                                            round_dict['handicap'],
                                                            round_dict['slope'])
            round_list.append(round_dict)

        if len(round_list) == 0:
            continue

        p['handicap'] = usga_handicap_index(round_list)
        if course_handi:
            p['course_handi'] = usga_course_handicap(form.cleaned_data['course_slope'],
                                                     p['handicap'])
        output.append({'player': p, 'rounds': round_list})

    output = sorted(output, key=lambda r: r['player']['handicap'])

    return render(request, 'golfhandicap/allplayers.html', {'course_form': form,
                                                            'Players': output,
                                                            'course_handi': course_handi})


def games(request):
    games = Game.objects.all().order_by('-game_date')
    for game in games:
        scores = Score.objects.filter(game_id=game).order_by('score')
        for score in scores:
            score.diff = usga_handicap_differential(score.adjusted_score,
                                                    game.course_handicap,
                                                    game.course_slope)
        game.scores = scores
        
    return render(request, 'golfhandicap/games.html', {'Games': games})