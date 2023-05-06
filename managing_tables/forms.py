from django import forms
from .models import Table, Participant


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['name', 'privacy', 'competition_type', 'number_of_points_for_a_win', 'logotype']
        labels = {'name': 'Название',
                  'privacy': 'Приватная таблица',
                  'competition_type': 'Тип соревнования',
                  'number_of_points_for_a_win': 'Количество очков за победу',
                  'logotype': 'Логотип'}


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['participant']
        labels = {'participant': 'Участник'}


class EditForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['participant', 'wins', 'draws', 'defeats']
        labels = {'participant': 'Участник',
                  'wins': 'Победы',
                  'draws': 'Ничьи',
                  'defeats': 'Поражения'}


class MatchForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['participant', 'wins']
        labels = {'participant': 'Участник',
                  'wins': 'Победы'}
