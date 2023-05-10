from django.shortcuts import render, redirect, get_object_or_404
from .models import Table, Participant
from .forms import TableForm, ParticipantForm, EditForm, MatchForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


def index(request):
    """Home page"""
    return render(request, 'managing_tables/index.html')


def all_users_tables(request):
    """Page with user tables"""
    tables = Table.objects.filter(privacy=False).order_by('name')
    context = {'tables': tables}
    return render(request, 'managing_tables/all_users_tables.html', context)


@login_required
def tables(request):
    """Page with user tables"""
    tables = Table.objects.filter(owner=request.user).order_by('name')
    context = {'tables': tables}
    return render(request, 'managing_tables/tables.html', context)


def table(request, table_id):
    """Page with info about table"""
    table = get_object_or_404(Table, id=table_id)
    participants = table.participant_set.order_by('-points')
    context = {'table': table, 'participants': participants}
    return render(request, 'managing_tables/table.html', context)


@login_required
def new_table(request):
    """Page to creating new table"""
    if request.method != 'POST':
        # Data not upload
        form = TableForm()
    else:
        form = TableForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_table = form.save(commit=False)
            new_table.owner = request.user
            new_table.save()
            return redirect('managing_tables:tables')

    context = {'form': form}
    return render(request, 'managing_tables/new_table.html', context)


@login_required
def edit_table(request, participant_id):
    """Page allows to specify total games, wins and so on"""
    participant = get_object_or_404(Participant, id=participant_id)
    table = participant.table
    check_table_owner(request, table)
    if request.method != 'POST':
        # Data not upload
        if table.competition_type == 'Лига':
            form = EditForm(instance=participant)
        else:
            form = MatchForm(instance=participant)
    else:
        if table.competition_type == 'Лига':
            form = EditForm(instance=participant, data=request.POST)
            if form.is_valid():
                if 'wins' or 'draws' or 'defeats' in form.changed_data:
                    participant.total_games = 0
                    for i in range(participant.wins+participant.draws+participant.defeats):
                        participant.total_games += 1
                        participant.save()
                if 'wins' or 'draws' in form.changed_data:
                    participant.points = 0
                    for i in range(participant.wins):
                        participant.points += table.number_of_points_for_a_win
                        participant.save()
                    for i in range(participant.draws):
                        participant.points += 1
                        participant.save()
                form.save()
                return redirect('managing_tables:table', table_id=table.id)
        else:
            form = MatchForm(instance=participant, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('managing_tables:table', table_id=table.id)

    context = {'participant': participant, 'table': table, 'form': form}
    return render(request, 'managing_tables/edit_table.html', context)


@login_required
def new_participant(request, table_id):
    """Page to creating new table"""
    table = get_object_or_404(Table, id=table_id)
    check_table_owner(request, table)
    if request.method != 'POST':
        # Data not upload
        form = ParticipantForm()
    else:
        form = ParticipantForm(data=request.POST)
        if form.is_valid():
            new_participant = form.save(commit=False)
            new_participant.table = table
            new_participant.save()
            return redirect('managing_tables:table', table_id=table_id)

    context = {'table': table, 'form': form}
    return render(request, 'managing_tables/new_participant.html', context)


@login_required
def delete_table(request, table_id):
    """Deleting table"""
    table = get_object_or_404(Table, id=table_id)
    check_table_owner(request, table)
    if request.method == 'POST':
        table.logotype.delete(save=True)
        table.delete()
        return redirect('managing_tables:tables')
    context = {'table': table}
    return render(request, 'managing_tables/tables.html', context)


@login_required
def delete_participant(request, participant_id):
    """Deleting participants"""
    participant = get_object_or_404(Participant, id=participant_id)
    table = participant.table
    check_table_owner(request, table)
    if request.method == 'POST':
        participant.delete()
        return redirect('managing_tables:table', table_id=table.id)
    context = {'participant': participant, 'table': table}
    return render(request, 'managing_tables/edit_table.html', context)


def check_table_owner(request, table):
    """Checks that the owner of the table is the current user"""
    if table.owner != request.user:
        raise Http404


def error_404(request, exception):
    return render(request, 'managing_tables/404.html', status=404)


def error_500(request, exception=None):
    return render(request, 'managing_tables/500.html', status=500)
