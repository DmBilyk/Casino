from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse


def edit_session_balance(request):
    if request.method == 'POST':

        new_balance = request.POST.get('balance', None)

        try:

            new_balance = int(new_balance)
            request.session['balance'] = new_balance
            messages.success(request, f"Balance updated to ${new_balance}")
        except ValueError:
            messages.error(request, "Invalid balance value")

        return redirect('edit_session_balance')

    # Render the admin page for editing balance
    return render(request, 'admin/edit_balance.html', {
        'current_balance': request.session.get('balance', 1000)
    })
