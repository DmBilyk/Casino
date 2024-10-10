from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

def edit_all_session_balances(request):
    sessions_with_balances = []

    # Отримуємо всі активні сесії
    sessions = Session.objects.all()
    for session in sessions:
        try:
            data = session.get_decoded()
            if 'balance' in data:
                sessions_with_balances.append({
                    'session_key': session.session_key,
                    'balance': data['balance']
                })
        except Exception as e:
            logger.error(f"Error accessing session {session.session_key}: {e}")

    if request.method == 'POST':
        session_key = request.POST.get('session_key')
        new_balance = request.POST.get('balance')

        try:
            new_balance = int(new_balance)
            session = Session.objects.get(session_key=session_key)
            session_data = session.get_decoded()

            old_balance = session_data.get('balance', 'N/A')
            session_data['balance'] = new_balance
            session.session_data = session_data
            session.save()

            logger.info(f"Updated balance for session {session_key}: {old_balance} -> {new_balance}")
            messages.success(request, f"Balance for session {session_key} updated to ${new_balance}")
        except ValueError:
            logger.error(f"Invalid balance input: {new_balance}")
            messages.error(request, "Invalid balance input. Please enter a valid number.")
        except Session.DoesNotExist:
            logger.error(f"Session not found: {session_key}")
            messages.error(request, "Session not found.")
        except Exception as e:
            logger.error(f"Error updating session {session_key}: {e}")
            messages.error(request, "An error occurred while updating the balance.")

        return redirect('blackjack_app:edit_all_session_balances')

    return render(request, 'admin/edit_all_balances.html', {
        'sessions_with_balances': sessions_with_balances,
    })