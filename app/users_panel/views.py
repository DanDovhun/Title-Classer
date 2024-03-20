from django.shortcuts import render

def user_dashboard(request):
    if request.method == 'POST':
        search_input = request.POST.get('search_input', '')
        return render(request, 'user_dashboard.html', {'search_input': search_input})
    else:
        return render(request, 'user_dashboard.html')
