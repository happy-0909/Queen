from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from userinfoapp.models import userInfo
import random



def lowhighView (request) :
    return render(request,'lowhigh/lowhigh.html')



@csrf_exempt
def lowhighStart(request) :
    if loginTF(request) :
        if request.method == 'POST' or request.method == 'post':
            bet_money = request.POST.get('bet_money')
            card_all = [11,12,13,14,15,16,17,18,19,110,111,112,113,
                        21,22,23,24,25,26,27,28,29,210,211,212,213,
                        31,32,33,34,35,36,37,38,39,310,311,312,313,
                        41,42,43,44,45,46,47,48,49,410,411,412,413]
            com_card = random.choice(card_all)
            user_card = random.choice(card_all)
            if com_card == user_card :
                while True :
                    com_card = random.choice(card_all)
                    user_card = random.choice(card_all)
                    if com_card == user_card :
                        continue
                    else :
                        break
            com_card = str(com_card)
            user_card = str(user_card)
            com_pattern = makePattern(com_card)
            com_num = makeNumber(com_card)
            user_pattern = makePattern(user_card)
            user_num = makeNumber(user_card)
            request.session['com_num'] = com_num
            request.session['com_pattern'] = com_pattern
            request.session['user_num'] = user_num
            request.session['user_pattern'] = user_pattern
            
            
            print("컴 문양",com_pattern,type(com_pattern))
            print("컴 숫자",com_num,type(com_num))

            print("유저 문양",user_pattern,type(user_pattern))
            print("유저 숫자",user_num,type(user_num))




            return render(request,'lowhigh/lowhighSelect.html',{'com_pattern':com_pattern,
                                                          'com_num':com_num,
                                                          'user_pattern':user_pattern,
                                                          'user_number':user_num,
                                                          'bet_money':bet_money})
    else :
        return redirect('/')
    

# 계산식
@csrf_exempt
def lowhighResult(request) :
    if loginTF(request) :
        if request.method == 'post' or request.method == 'POST':
            com_num = request.session['com_num']
            com_pattern = request.session['com_pattern']
            user_num = request.session['user_num']
            user_pattern = request.session['user_pattern']
            selectLH = request.POST.get('selectLH')
            print(selectLH)
            result = ''
            # 선택이 low
            if selectLH == "LOW":
                if user_num == com_num :
                    if user_pattern < com_pattern:
                        getUserinfo = userInfo.objects.get(UID=request.session['UID'])
                        bet_money = int(request.POST.get('bet_money'))
                        money = getUserinfo.MONEY
                        money += bet_money
                        getUserinfo.MONEY = money
                        request.session['MONEY'] = money
                        getUserinfo.save()
                        result = "승리"
                    else :
                        getUserinfo = userInfo.objects.get(UID=request.session['UID'])
                        bet_money = int(request.POST.get('bet_money'))
                        money = getUserinfo.MONEY
                        money -= bet_money
                        getUserinfo.MONEY = money
                        request.session['MONEY'] = money
                        getUserinfo.save()
                        result = "패배"


                elif user_num < com_num :
                    getUserinfo = userInfo.objects.get(UID=request.session['UID'])
                    bet_money = int(request.POST.get('bet_money'))
                    money = getUserinfo.MONEY
                    money += bet_money
                    getUserinfo.MONEY = money
                    request.session['MONEY'] = money
                    getUserinfo.save()
                    result = "승리"
                else :
                    getUserinfo = userInfo.objects.get(UID=request.session['UID'])
                    bet_money = int(request.POST.get('bet_money'))
                    money = getUserinfo.MONEY
                    money -= bet_money
                    getUserinfo.MONEY = money
                    request.session['MONEY'] = money
                    getUserinfo.save()
                    result = "패배"
            #선택이 high
            else :
                if user_num == com_num :
                    if user_pattern < com_pattern:
                        getUserinfo = userInfo.objects.get(UID=request.session['UID'])
                        bet_money = int(request.POST.get('bet_money'))
                        money = getUserinfo.MONEY
                        money -= bet_money
                        getUserinfo.MONEY = money
                        request.session['MONEY'] = money
                        getUserinfo.save()
                        result = "패배"
                    else :
                        getUserinfo = userInfo.objects.get(UID=request.session['UID'])
                        bet_money = int(request.POST.get('bet_money'))
                        money = getUserinfo.MONEY
                        money += bet_money
                        getUserinfo.MONEY = money
                        request.session['MONEY'] = money
                        getUserinfo.save()
                        result = "승리"


                elif user_num < com_num :
                    getUserinfo = userInfo.objects.get(UID=request.session['UID'])
                    bet_money = int(request.POST.get('bet_money'))
                    money = getUserinfo.MONEY
                    money -= bet_money
                    getUserinfo.MONEY = money
                    request.session['MONEY'] = money
                    getUserinfo.save()
                    result = "패배"
                else :
                    getUserinfo = userInfo.objects.get(UID=request.session['UID'])
                    bet_money = int(request.POST.get('bet_money'))
                    money = getUserinfo.MONEY
                    money += bet_money
                    getUserinfo.MONEY = money
                    request.session['MONEY'] = money
                    getUserinfo.save()
                    result = "승리"
            
            del request.session['com_num']
            del request.session['com_pattern']
            del request.session['user_num']
            del request.session['user_pattern']
            return render(request,'lowhigh/lowhighResult.html', {
                'result' : result,
                'com_num' : com_num,
                'com_pattern' : com_pattern,
                'user_num':user_num,
                'user_pattern':user_pattern,
                'selectLH':selectLH,
                'bet_money' : bet_money
                            })
        #return render(request,'lowhigh/lowhigh.html')
    else :
        return redirect('/')
    

@csrf_exempt
def resulLowhigh(request) :
    
    pass
    
@csrf_exempt 
def makePattern(card):
    tempCard = card[0]
    tempCard = int(tempCard)
    return tempCard

@csrf_exempt 
def makeNumber(card):
    tempCard = ''
    for i in range(1,len(card)) :
        tempCard += str(card)[i]
    tempCard = int(tempCard)
    return tempCard


@csrf_exempt 
def updateUser():
    return 0


@csrf_exempt  
def loginTF(request) :
    if request.session['loginOk'] is True :
        return True
    else :
        return False
# Create your views here.


