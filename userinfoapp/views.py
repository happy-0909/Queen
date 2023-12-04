from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from userinfoapp.models import userInfo
import requests

# Create your views here.

def index(request):
    login_ck = loginTF(request)
    if login_ck :
        return render(request,'mainmenu.html')
    else :
        return render(request, 'index.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')


def user_list(request):
    
    userList = {}
    userList["userList"] = userInfo.objects.all()
    return render(request, 'userlist.html',userList)

@csrf_exempt
def userInsert(request) :
    # 회원가입
    
    # post 타입으로 넘어온 데이터 받기
    _LOGIN_ID = request.POST.get("LOGIN_ID")
    _NICK = request.POST.get("NICK")
    _PASSWORD = request.POST.get("PASSWORD")
    _PASSWORD = str(_PASSWORD)
    _EMAIL = request.POST.get("EMAIL")
    
    # 만약 중복된 LOGIN_ID나 NICK이나 email 이면
    if userInfo.objects.filter(LOGIN_ID=_LOGIN_ID).exists() :
        return render( request, 'signup.html', {'error' : '이미 사용중인 아이디 입니다.'} )
    
    elif userInfo.objects.filter(NICK=_NICK).exists() :
        return render( request, 'signup.html', {'error' : '이미 사용중인 닉네임 입니다.'} )
    
    elif userInfo.objects.filter(EMAIL=_EMAIL).exists() :
        return render( request, 'signup.html', {'error' : '이미 사용중인 이메일 입니다.'} )
    
    # 중복된 LOGIN_ID나 NICK 이 없으면 회원가입
    else : 
        query = userInfo.objects.create(LOGIN_ID=_LOGIN_ID, NICK=_NICK, PASSWORD=_PASSWORD, EMAIL=_EMAIL)
        return redirect('/login/')


 
@csrf_exempt   
def cklogin(request) :
    # print(request.session['loginOk'])
    request.session['loginOk'] = False
    if request.method == 'POST' or request.method == 'post' :
        _LOGIN_ID = request.POST.get("LOGIN_ID")
        _PASSWORD = request.POST.get("PASSWORD")
        
        if userInfo.objects.filter(LOGIN_ID=_LOGIN_ID).exists() :
            print("아이디 있음")
            getUserInfo = userInfo.objects.get(LOGIN_ID=_LOGIN_ID)
            if getUserInfo.PASSWORD == _PASSWORD :
                print("로그인 성공")
                request.session["loginOk"] = True
                request.session["UID"] = getUserInfo.UID; # 로그인 하면 uid를 들고다니면서 계속 데이터베이스와 비교해서 사용할거임
                request.session["NICK"] = getUserInfo.NICK
                request.session["MONEY"] = getUserInfo.MONEY
                request.session["AUTH_ID"] = getUserInfo.AUTH_ID
                print(request.session["UID"])
                # del request.session["UID"] # 세션 삭제 
                if getUserInfo.AUTH_ID == 1 :
                    return render(request,'adm/adminIndex.html')
                else :
                    #return render(request,'mainmenu.html')
                    return redirect("/mainmenu/")
            else :
                request.session['loginOk'] = False
                return render(request, 'login.html',{ 'error' : '비밀번호가 틀렸습니다' })
        
        
        
        # if user is not None :
        #     print("로그인 확인")
        # elif user is None :
        #     print("로그인 실패")
        
        
        print(_LOGIN_ID)
        print(_PASSWORD)
    return redirect('/login/')


@csrf_exempt  
def cklogout(request) :
    request.session.clear() #모든 세션 삭제
    request.session['loginOk'] = False
    
    
    return redirect('/')

@csrf_exempt  
def ckMainmenu(request) :
    if request.session['loginOk'] is True :
        if request.session['AUTH_ID'] == 1 :
            return redirect('/adm/queenAdmin/')
        else :
            return render(request,'mainmenu.html')
    else :
        return redirect('/')
    

    
@csrf_exempt  
def loginTF(request) :
    if request.session['loginOk'] is True :
        return True
    else :
        return False
 
 




