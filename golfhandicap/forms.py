from django import forms


class CalculateCourseHandicapForm(forms.Form):
    course_slope = forms.IntegerField(max_value=155, min_value=55)
