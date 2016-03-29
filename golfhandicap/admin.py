from django.contrib import admin
from .models import Course, Player, Game, Score

class ScoreInline(admin.TabularInline):
    model = Score


class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nick_name', 'first_name', 'last_name']}),
        ('Other Information', {'fields': ['email']}),
    ]

    list_display = ['nick_name', 'first_name', 'last_name', 'email']


class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['course', 'tee', 'course_handicap', 'course_slope', 'game_date', 'game_index']}),
    ]
    inlines = [ScoreInline]
    list_display = ['game_date', 'course', 'tee', 'course_handicap', 'course_slope']


class ScoreAdmin(admin.ModelAdmin):
    list_display = ['game', 'player', 'score', 'adjusted_score']


admin.site.register(Course)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Score, ScoreAdmin)
