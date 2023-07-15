from django.shortcuts import render, redirect
from .models.Card import CardModel
from .models.CardForm import CardForm

def home(request):
    data = {

    }
    return render(request, 'main/home.html')

def cards(request):
    cards = CardModel.objects.all()
    return render(request, 'main/cards.html', {'cards': cards})

def newcard(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('card-list')
    else:
        form = CardForm()
    return render(request, 'main/newcard.html', {'form': form})
