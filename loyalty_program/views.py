from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TeamPointsBalance, PointsTransaction


@login_required
def team_balance(request):
    """Страница с балансами всех команд"""
    balances = TeamPointsBalance.objects.select_related("team").all()

    context = {
        "balances": balances,
    }
    return render(request, "loyalty/team_balance.html", context)


@login_required
def transactions(request):
    """Страница с историей операций"""
    transactions = PointsTransaction.objects.select_related("team").all()

    context = {
        "transactions": transactions,
    }
    return render(request, "loyalty/transactions.html", context)
