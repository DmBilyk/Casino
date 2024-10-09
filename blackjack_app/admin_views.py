from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


@staff_member_required
def edit_session_balance(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        session_key = request.POST.get('session_key')
        new_balance = request.POST.get('new_balance')

        if session_key and new_balance:
            from django.contrib.sessions.models import Session
            try:
                session = Session.objects.get(session_key=session_key)
                session_data = session.get_decoded()
                session_data['balance'] = int(new_balance)
                session.session_data = Session.objects.encode(session_data)
                session.save()
                messages.success(request, f"Balance updated for session {session_key}")
            except Session.DoesNotExist:
                messages.error(request, f"Session {session_key} not found")
            except ValueError:
                messages.error(request, "Invalid balance value")
        else:
            messages.error(request, "Both session key and new balance are required")

        return redirect('admin:edit_session_balance')

    from django.contrib.sessions.models import Session
    sessions = Session.objects.all()
    session_data = []
    for session in sessions:
        data = session.get_decoded()
        if 'balance' in data:
            session_data.append({
                'session_key': session.session_key,
                'balance': data['balance']
            })

    return render(request, 'admin/edit_session_balance.html', {'sessions': session_data})