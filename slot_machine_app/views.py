from django.shortcuts import render,redirect
from userinfoapp.models import userInfo  # userInfo 모델을 가져옵니다.
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import random


def spin(request):
    login_ck = loginTF(request)
    if login_ck :
        return render(request,'slot_machine_app/slot.html')
    else :
        return redirect('/')

@csrf_exempt
def spin_start(request):
    
    login_ck = loginTF(request)
    if login_ck :
    
        symbols = ['cherry', 'lemon', 'orange', 'banana', 'bell', 'bar', 'seven']

        slot1 = random.choice(symbols)
        slot2 = random.choice(symbols)
        slot3 = random.choice(symbols)

        print(slot1,slot2,slot3)
        money = request.session['MONEY']
        result = slot_result(slot1,slot2,slot3,int(request.POST.get('bet_money')),request)

        if result != "":

            return render(request, 'slot_machine_app/result.html',
                      { 'slot1' : slot1,
                        'slot2' : slot2,
                        'slot3' : slot3,
                        'money' : money,
                        'result' : result })
        else :
            return redirect('/')
            
    else :
        return redirect('/')

@csrf_exempt
def slot_result(slot1,slot2,slot3,bet_money,request):
    login_ck = loginTF(request)
    if login_ck :
        print(slot1,slot2,slot3)
        if slot1 == slot2 or slot1 == slot3 or slot2 == slot3 :
            money = request.session['MONEY']
            money += (bet_money / 2)
            request.session['MONEY'] = money
            getUserinfo = userInfo.objects.get(UID=request.session['UID']) # uid에 맞는 데이터 가져옴
            getUserinfo.MONEY = money                                      # 저장하기 전에 베팅 금액 계산 데이터 넣음
            getUserinfo.save()  #데이터 저장(베팅금액 계산후 db에 저장)                        
            return "2개 맞춤 0.5배!"

        elif slot1 == slot2 and slot2 == slot3 :
            money = request.session['MONEY']
            money += (bet_money * 5)
            request.session['MONEY'] = money
            getUserinfo = userInfo.objects.get(UID=request.session['UID'])
            getUserinfo.MONEY = money
            getUserinfo.save()
            return "잭팟 5배!"

        elif slot1 != slot2 or slot2 != slot3 or slot1 != slot3 :
            money = request.session['MONEY']
            money-=bet_money
            request.session['MONEY'] = money
            getUserinfo = userInfo.objects.get(UID=request.session['UID'])
            getUserinfo.MONEY = money
            getUserinfo.save()
            return "꽝!"
        
        
    else :
        return redirect('/')
    
    

@csrf_exempt  
def loginTF(request) :
    if request.session['loginOk'] is True :
        return True
    else :
        return False                 

