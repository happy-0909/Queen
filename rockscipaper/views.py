from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from userinfoapp.models import userInfo
from django.http import JsonResponse

import random

# Create your views here.

@csrf_exempt
def rsp(request) :
    login_ck = loginTF(request)
    if login_ck :
        return render(request,'rsp/rspMain.html')
    else :
        return redirect('/')
    



@csrf_exempt
def rsp_start(request):
    login_ck = loginTF(request)
    if login_ck :
        user_choice = request.POST.get('choice')
        print('유저 선택',user_choice)
        choices = ['rock', 'paper', 'scissors']
        computer_choice = random.choice(choices)

    
        print(computer_choice)

        money = request.session['MONEY']
        bet_money = request.POST.get('bet_money')
        print("베팅 금액",bet_money)
        bet_money = int(bet_money)
        result = determine_winner(user_choice,computer_choice,bet_money,request)
        response_data = {'user_choice': user_choice, 
                       'computer_choice': computer_choice, 
                       'result': result,
                       'money' : money}

        return JsonResponse(response_data)
    else :
        return redirect('/')
    
    # return render(request,'rsp/rspResult.html',
    #               {'user_choice': user_choice, 
    #                'computer_choice': computer_choice, 
    #                'result': result,
    #                'money' : money}) 



@csrf_exempt
def determine_winner(player_choice, computer_choice,bet_money,request):
    print(computer_choice)
    if player_choice == computer_choice:
        return "무승부"
    elif (
        (player_choice == 'rock' and computer_choice == 'scissors') or
        (player_choice == 'paper' and computer_choice == 'rock') or
        (player_choice == 'scissors' and computer_choice == 'paper')
    ):
        money = request.session['MONEY']
        money+=bet_money
        request.session['MONEY'] = money
        getUserinfo = userInfo.objects.get(UID=request.session['UID']) # uid에 맞는 데이터 가져옴
        getUserinfo.MONEY = money                                      # 저장하기 전에 베팅 금액 계산 데이터 넣음
        getUserinfo.save()  #데이터 저장(베팅금액 계산후 db에 저장)                        
        return "와 승리!"
    else:
        money = request.session['MONEY']
        money-=bet_money
        request.session['MONEY'] = money
        getUserinfo = userInfo.objects.get(UID=request.session['UID'])
        getUserinfo.MONEY = money
        getUserinfo.save()
        return "와 패배!"
    
@csrf_exempt
def rsp_result(request) :
    login_ck = loginTF(request)
    if login_ck :
        result = request.GET.get('result')
        user_choice = request.GET.get('user_choice')
        computer_choice = request.GET.get('computer_choice')
        money = request.GET.get('money')
        print("결과",result)
        return render(request,'rsp/rspResult.html',{'user_choice': user_choice, 
                      'computer_choice': computer_choice, 
                       'result': result,
                        'money' : money})
    else :
        return redirect('/')


@csrf_exempt  
def loginTF(request) :
    if request.session['loginOk'] is True :
        return True
    else :
        return False