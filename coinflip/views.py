import random
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from userinfoapp.models import userInfo

@csrf_exempt
def coinflip(request):
    login_ck = loginTF(request)
    if login_ck :
        return render(request, 'coinflip/game.html')
    else :
        return redirect('/')

@csrf_exempt
def result(request) :
    login_ck = loginTF(request)
    if login_ck :
        bet = request.POST.get('bet')
        choice = request.POST.get('my_choice')
        com_choice = ["홀", "짝"]
        com_result = random.choice(com_choice)
        print(bet)
        print(choice)
        result_text = money_result(request,bet,choice,com_result)
        

        return render(request,'coinflip/coinre.html', {'result' : result_text,
        'bet' : bet,
        'choice':choice,
        'com_result':com_result})
    else :
        return redirect('')

        
        

@csrf_exempt
def money_result(request,bet,choice,com_result):
    login_ck = loginTF(request)
    if login_ck :
        
        if request.method == 'POST':
            
            getUserinfo = userInfo.objects.get(UID=request.session['UID'])

            if choice == com_result:
                outcome = "Win"
                winnings = int(bet) * 2
                money = request.session['MONEY']
                money+=winnings
                getUserinfo.MONEY = money
                request.session['MONEY'] = money
                getUserinfo.save()
                return '인생역전!!!'
            
            else:
                #print(choice,com_choice)
                outcome = "Lose"
                money = request.session['MONEY']
                money -= int(bet)
                getUserinfo.MONEY = money
                request.session['MONEY'] = money
                getUserinfo.save()
                return '패가망신!!!'
    else :
        return redirect('/')

    return render(request, 'coinflip/coinre.html', {'bet': bet, 'choice': choice, 'outcome': outcome, 'winnings': winnings, 'com_result' : com_result})
    
@csrf_exempt  
def loginTF(request) :
    if request.session['loginOk'] is True :
        return True
    else :
        return False          
