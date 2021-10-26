from django.shortcuts import render
from django.shortcuts import redirect


def admin(request):
    if request.user.is_staff:
        return render(request, 'react.html', {})
    return redirect('/')