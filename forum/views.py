from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import managing_tables.views
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def topics(request):
    """Displays all topics"""
    topics = Topic.objects.filter().order_by('date_added')
    context = {'topics': topics}
    return render(request, 'forum/topics.html', context)


def topic(request, topic_id):
    """Displays one topic and all its entries"""
    topic = get_object_or_404(Topic, id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'forum/topic.html', context)


@login_required
def new_topic(request):
    """Page to creating new topic"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.save()
            return redirect('forum:topics')

    context = {'form': form}
    return render(request, 'forum/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Page to creating new entry"""
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return redirect('forum:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'forum/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Page allows to specify entry"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    managing_tables.views.check_table_owner(request, entry)
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'forum/edit_entry.html', context)


@login_required
def delete_entry(request, entry_id):
    """Deleting entries"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    managing_tables.views.check_table_owner(request, entry)
    if request.method == 'POST':
        entry.delete()
        return redirect('forum:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic}
    return render(request, 'forum/topics.html', context)
