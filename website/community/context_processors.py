from django.shortcuts import render, redirect
from notifications.models import Notification
from website import settings


def inbox(request, **kwargs):
    if request.user.is_authenticated:
        inbox = request.user.notifications
        if settings.DELETE_POST == True:
            n = Notification.objects.filter(action_object_object_id=request.session['notify_delete'])
            n.delete()
        settings.DELETE_POST = False
        context = {'inbox': inbox}
        return context
    else:
        return request


def inbox_read_view(request, id=None):
    if request.user.is_authenticated:
        inbox = request.user.notifications
        for inbox_list in inbox.unread():
            if id:
                notifies = Notification.objects.filter(action_object_object_id=id)
                for n in notifies:
                    n.mark_as_read()
                return redirect('community:question_view', inbox_list.action_object.ask_slug)
    return render(request, 'community/inbox_read_view.html')


def mark_all_as_read(request):
    if request.user.is_authenticated:
        inbox = request.user.notifications
        inbox.mark_all_as_read()
        return redirect('community:all_items')
    return render(request, 'community/inbox_read_view.html')


def remove_all_notifications(request):
    if request.user.is_authenticated:
        inbox = request.user.notifications
        inbox.all().delete()
        return redirect('accounts:view_profile', request.user.userprofile.slug)
    return render(request, 'community/inbox_read_view.html')


def remove_notify(request, id=None):
    if request.user.is_authenticated:
        inbox = request.user.notifications
        for inbox_list in inbox.all():
            if id:
                notify_object = Notification.objects.get(id=inbox_list.id)
                notify_object.delete()
                return redirect('community:all_items')
    return render(request, 'community/inbox_read_view.html')
