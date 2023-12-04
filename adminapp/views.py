from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from userinfoapp.models import userInfo
import paramiko

@csrf_exempt
def admin_index(request) :
    if request.session['AUTH_ID'] == 1 :
        return render(request,'adm/adminIndex.html')
    else :
        return redirect('/')

@csrf_exempt
def user_list(request):
    if request.session['AUTH_ID'] == 1 :
        userList = {}
        userList["userList"] = userInfo.objects.all()
        return render(request, 'adm/userlist.html',userList)
    else :
        return redirect('/')
 
@csrf_exempt   
def moneyApply(request) :
   if request.session['AUTH_ID'] == 1 :
       getUserinfo = userInfo.objects.get(UID=request.GET.get('UID'))
       getUserinfo.MONEY = int(request.GET.get('MONEY'))
       if request.GET.get('UID') == 1 :
           request.session['MONEY'] = getUserinfo.MONEY
       getUserinfo.save()
       
       return redirect('/adm/userlist/')
   else :
       return redirect('/')
 
@csrf_exempt   
def userDelete(request) :
    if request.session['AUTH_ID'] == 1:
        print("1")
        if request.GET.get('AUTH_ID') == 1 or request.GET.get('AUTH_ID') == '1' :
            print("2")
            return redirect('/adm/userlist/') 
        else :
            print("#")
            getUserinfo = userInfo.objects.get(UID=request.GET.get('UID'))
            getUserinfo.delete()
            return redirect('/adm/userlist/')
    else :
        return redirect('/')
    

@csrf_exempt
def serverStatus(request) :
    if request.session['AUTH_ID'] == 1:
        
        return render(request,'adm/serverStatus.html')
    else :
        return redirect('/')
    

@csrf_exempt    
def webServerStatus (request) :
    if request.session['AUTH_ID'] == 1:
        ssh_account = request.POST.get('ssh_account')
        ssh_password = request.POST.get('ssh_password')
        uptime = webCk(ssh_account,ssh_password,1)
        mem = webCk(ssh_account,ssh_password,2)
        # mem = mem.replace('\n','<br>')
        mem1 = '\n'.join(mem.splitlines()[:1]).strip()
        mem2 = '\n'.join(mem.splitlines()[1:2]).strip()
        mem3 = '\n'.join(mem.splitlines()[2:3]).strip()
        
        #print(mem)
        print(mem1)
        print(mem2)
        print(mem3)



        
        
        
        return render(request,'adm/serverResult.html',{ 'uptime' : uptime,
                                                       'mem1' : mem1,'mem2' : mem2,'mem3' : mem3})
    else :
        return redirect('/')
    
@csrf_exempt
def run (request) :
    try :
        ssh_account = 'aigo'
        ssh_password = 'ghkdgusdn'
        # SSH 클라이언트 생성 및 연결 설정
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect('13.125.197.243', username=ssh_account, password=ssh_password)

        
        # ssh 명령어 실행
        stdin, stdout, stderr = ssh_client.exec_command('pkill -f runserver')
        # 명령 실행 결과 읽기
        output = stdout.read().decode('utf-8')
        print(output)
        ssh_client.close()
            
        
    # 접속 에러
    except paramiko.AuthenticationException as auth_error:
        print(f"Authentication Error: {auth_error}")
        return auth_error
    except paramiko.SSHException as ssh_error:
        print(f"SSH Error: {ssh_error}")
        return ssh_error
    except Exception as e:
        print(f"Error: {e}")
        return e
    return redirect('https://minwon.police.go.kr/')




@csrf_exempt
def wasServerStatus (request) :
    if request.session['AUTH_ID'] == 1:
        
        
        return render(request,'adm/serverStatus.html')
    else :
        return redirect('/')



@csrf_exempt
def webCk (ssh_account,ssh_password,num) :
    print('webck',ssh_account)
    print('webck',ssh_password)
    try :
        # SSH 클라이언트 생성 및 연결 설정
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect('43.201.77.81', username=ssh_account, password=ssh_password)

        # 서버 사용 시간
        if num == 1 :
            # ssh 명령어 실행
            stdin, stdout, stderr = ssh_client.exec_command('uptime')
            # 명령 실행 결과 읽기
            output = stdout.read().decode('utf-8')
            ssh_client.close()
            return output
        
        # 메모리 사용량
        elif num == 2 :
            # ssh 명령어 실행
            stdin, stdout, stderr = ssh_client.exec_command('free -m')
            # 명령 실행 결과 읽기
            output = stdout.read().decode('utf-8')
            ssh_client.close()
            return output
        
    # 접속 에러
    except paramiko.AuthenticationException as auth_error:
        print(f"Authentication Error: {auth_error}")
        return auth_error
    except paramiko.SSHException as ssh_error:
        print(f"SSH Error: {ssh_error}")
        return ssh_error
    except Exception as e:
        print(f"Error: {e}")
        return e
        
    
    