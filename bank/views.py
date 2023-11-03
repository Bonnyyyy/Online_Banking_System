from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.shortcuts import get_list_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from.models import *
import random
import string

# Create your views here.
def generate_random_string_with_number():
    letters = string.ascii_letters
    random_letters = ''.join(random.choice(letters) for _ in range(random.randint(5, 15)))  # Random length for alphabets
    
    numbers = string.digits
    random_numbers = ''.join(random.choice(numbers) for _ in range(5))  # Fixed length of 5 digits
    
    return random_letters + random_numbers

def generate_16_digit_number():
    # Generate a random 16-digit number
    random_number = random.randint(10**15, 10**16 - 1)
    random_number_str = str(random_number)
    
    return random_number_str

def generate_3_digit_number():
    # Generate a random 3-digit number
    random_number = random.randint(100, 999)
    
    return random_number

def home(request):
    return render(request,'index.html')

def sign_up(request):
    return render(request,'sign_up.html')
def custom(request):
    return render(request,'custom.html')

def sign_in(request):
    return render(request,'sign_in.html')

def register(request):
    min_value = 10**14
    max_value = 10**15 - 1
    random_number = random.randrange(min_value, max_value + 1)
    card_no=generate_16_digit_number()
    cvv_no=generate_3_digit_number()
    us=User_table()
    us.First_name=request.GET['fname']
    us.Middle_name=request.GET['mname']
    us.Last_name=request.GET['lname']
    us.Gender=request.GET['gen']
    us.Dob=request.GET['dob']
    us.Ph_no=request.GET['ph']
    us.Email=request.GET['email']
    us.Address=request.GET['add']
    us.City=request.GET['city']
    us.District=request.GET['dist']
    us.State=request.GET['state']
    us.Pin=request.GET['pin']
    us.Aadhaar=request.GET['an']
    us.PAN=request.GET['pan']
    us.passport=request.GET['pno']
    us.pic=request.GET['pic']
    if User_table.objects.filter(username=request.GET['uname']):
        a="Username Already exists"
        return render(request,'sign_up.html',{'m':a})
    us.username=request.GET['uname']
    us.password=request.GET['password']
    us.mpin=request.GET['mpin']
    us.ac_no=random_number
    us.question=request.GET['scq']
    us.answer=request.GET['sa']
    us.card=card_no
    us.cvv=cvv_no
    us.save()
    return render(request,'sign_in.html')

def login(request):
    a=request.GET['user']
    b=request.GET['password']

    if User_table.objects.filter(username=a,password=b):
        if User_table.objects.filter(flag=0):
            return HttpResponse('<h1>Your douments are under proess.. Please try after some time</h1>')
        z=User_table.objects.get(username=a)
        bal=z.balance
        acno = z.ac_no
        debit=Transection.objects.all().filter(fac_no=acno).last()
        credit=Transection.objects.all().filter(tac_no=acno).last()
        cr=0
        dr=0
        if credit:
            cr = credit.credit
        
        if debit:
            dr = debit.debit
        request.session['num']=acno
        #request.session['f_name']=f_name
        #request.session['l_name']=l_name
        request.session['bal']=bal

        return render(request,'user_dashboard.html',{'ac_no':acno,'bal':bal,'cr':cr,'dr':dr,'a':z})
    else:
        return render(request,'sign_in.html')

def user_dashboard(request):
    #f_name=request.session.get('f_name','Default value')
    #l_name=request.session.get('l_name','Default value')
    acno = request.session.get('num', 'Default value')
    z=User_table.objects.get(ac_no=acno)
    debit=Transection.objects.all().filter(fac_no=acno).last()
    credit=Transection.objects.all().filter(tac_no=acno).last()
    cr=0
    dr=0
    if credit:
        cr = credit.credit
        
    if debit:
        dr = debit.debit
    bal=User_table.objects.get(ac_no=acno)
    context={'ac_no':acno,'bal':bal.balance,'cr':cr,'dr':dr,'a':z}
    return render(request, 'user_dashboard.html', context)

def money_transfer(request):
    #f_name=request.session.get('f_name','Default value')
    #l_name=request.session.get('l_name','Default value')
    acno = request.session.get('num', 'Default value')
    z=User_table.objects.get(ac_no=acno)
    #bal=request.session.get('bal','Default value')
    context={'ac_no':acno,'a':z}
    return render(request, 'money_transfer.html', context)

def sendmoney(request):
    num = generate_random_string_with_number()
    num1 = generate_random_string_with_number()
    ac_no=request.session.get('num','Default Value')
    mpin=request.GET['mpin']
    person = User_table.objects.get(ac_no=ac_no)  # Use get() instead of filter()
    debit = float(request.GET['bal'])  # Convert the debit to float
    if person.balance <= debit:
        b="Insufficient Balance"
        return render(request,'money_transfer.html',{'a':person,'ac_no':ac_no,'msg':b})
    person.balance -= debit
    if User_table.objects.filter(mpin=mpin,ac_no=ac_no):
        person.save()
    tac_no=request.GET['tac']
    t = Transection()
    t1 = Transection()
    if User_table.objects.filter(ac_no=tac_no):
        t_person=User_table.objects.get(ac_no=tac_no)
        credit=float(request.GET['bal'])
        if t_person.balance==None:
            t_person.balance=0
        t_person.balance=credit+t_person.balance
        t1.fac_no=request.GET['fac']
        t1.tac_no=''
        t1.debit=debit
        t1.tr_id=num
        t1.balance=person.balance
        t.fac_no = ''
        t.tac_no = request.GET['tac']
        t.credit = credit
        t.tr_id = num1
        t.balance = t_person.balance 
        if User_table.objects.filter(ac_no=ac_no,mpin=mpin):
            t1.save()
            t.save()
            t_person.save()

    else:
        t.fac_no = request.GET['fac']
        t.tac_no = request.GET['tac']
        t.debit = debit
        t.tr_id = num
        t.balance = person.balance 
        if User_table.objects.filter(ac_no=ac_no,mpin=mpin):
            t.save()
    if User_table.objects.filter(ac_no=ac_no,mpin=mpin):
        a="Success"
    else:
        a="Invalid mpin"
    context={'a':person,'ac_no':ac_no,'msg':a}

    return render(request,'money_transfer.html',context)

def stmt(request):
    #f_name=request.session.get('f_name','Default value')
    #l_name=request.session.get('l_name','Default value')
    acno = request.session.get('num', 'Default value')
    person = User_table.objects.get(ac_no=acno)
    x = Transection.objects.all().filter(fac_no=acno) | Transection.objects.all().filter(tac_no=acno)
    context={'ac_no':acno,'t':x,'a':person}
    return render(request, 'statement.html', context)

def statement(request):
    #f_name=request.session.get('f_name','Default value')
    #l_name=request.session.get('l_name','Default value')
    acno = request.session.get('num', 'Default value')
    person = User_table.objects.get(ac_no=acno)
    context={'ac_no':acno,'a':person}
    return render(request,'statement.html',context)

def cus_stmt(request):
    #f_name=request.session.get('f_name','Default value')
    #l_name=request.session.get('l_name','Default value')
    ac_no = request.session.get('num', 'Default value')
    person = User_table.objects.get(ac_no=ac_no)
    x=request.GET['from-date']
    y=request.GET['to-date']
    z=Transection.objects.all().filter(fac_no=ac_no,date__range=(x,y)).values() | Transection.objects.all().filter(tac_no=ac_no,date__range=(x,y)).values()
    context={'ac_no':ac_no,'b':z,'from':x,'to':y,'a':person}
    return render(request, 'custom.html',context)

def custom(request):
    #f_name=request.session.get('f_name','Default value')
    #l_name=request.session.get('l_name','Default value')
    acno = request.session.get('num', 'Default value')
    person = User_table.objects.get(ac_no=acno)
    context={'ac_no':acno,'a':person}
    return render(request,'custom.html',context)

def admin_panel(request):
    users = User_table.objects.all()  # Assuming you have a User model
    transactions = Transection.objects.all()  # Assuming you have a Transaction model

    context = {
        'users': users,
        'transactions': transactions,
    }

    return render(request, 'admin_panel.html', context)

def validate_user(request, user_id):
    if request.method == 'POST':
        user = User_table.objects.get(id=user_id)
        user.flag = 1
        user.save()
        return redirect('admin_panel')  # Redirect back to the user panel page
    return JsonResponse({'success': False})

def add_balance(request, user_id):
    num = generate_random_string_with_number()
    if request.method == 'POST':
        user = User_table.objects.get(id=user_id)
        amount = float(request.POST.get('amount', 0))
        user.balance += amount
        user.save()
        
        t = Transection()
        t.fac_no = "self"
        t.tac_no = user.ac_no
        t.debit = 0
        t.tr_id = num
        t.credit = amount
        t.balance = user.balance 
        t.save()

        return redirect('admin_panel')  # Redirect back to the user panel page
    return JsonResponse({'success': False})

def ad_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            admin = AdminDb.objects.get(username=username, password=password)
            # Successful login, redirect to admin panel
            return redirect('admin_panel')
        except AdminDb.DoesNotExist:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'ad_login.html', {'error_message': error_message})
    
    return render(request, 'ad_login.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            admin = AdminDb.objects.get(username=username, password=password)
            # Assuming you have a user_panel.html template in the templates folder
            return render(request, 'admin_panel.html', {'admin': admin})
        except AdminDb.DoesNotExist:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'ad_login.html', {'error_message': error_message})
    return render(request, 'ad_login.html')

def my_profile(request):
    #f_name=request.session.get('f_name','Default value')
    #l_name=request.session.get('l_name','Default value')
    acno = request.session.get('num', 'Default value')
    z=User_table.objects.get(ac_no=acno)
   # bal=request.session.get('bal','Default value')
    context={'ac_no':acno,'a':z}
    return render(request, 'my_profile.html', context)

def user_edit(request):
    #f_name=request.session.get('f_name','Default value')
    #l_name=request.session.get('l_name','Default value')
    acno = request.session.get('num', 'Default value')
    z=User_table.objects.get(ac_no=acno)
   # bal=request.session.get('bal','Default value')
    context={'ac_no':acno,'a':z}
    return render(request, 'user_edit.html', context)

def change_details(request):
    #num = generate_random_string_with_number()
    ac_no=request.session.get('num','Default Value')
    p = User_table.objects.get(ac_no=ac_no)  # Use get() instead of filter()
    p.First_name = request.GET['First_name']
    p.Last_name = request.GET['Last_name']
    p.Ph_no = request.GET['Ph_no']
    p.Email = request.GET['Email']
    p.save()

    #f_name=request.session.get('f_name','Default value')
    #l_name=request.session.get('l_name','Default value')
    context={'ac_no':ac_no,'a':p}

    return render(request,'user_edit.html',context)

def recover_password(request):
    return render(request,'recover_password.html')

def fgtpass(request):
    scq=request.GET['scq']
    ans=request.GET['sa']
    un=request.GET['uname']
    request.session['qs']=scq
    request.session['sa']=ans
    request.session['un']=un
    if User_table.objects.filter(question=scq,answer=ans,username=un):
        a=1
    else:
        a=0
    return render(request,'recover_password.html',{'a':a})

def resetpass(request):
    x=request.GET['pass']
    y=request.GET['c_pass']
    scq=request.session.get('qs','Default value')
    sa=request.session.get('sa','Default value')
    un=request.session.get('un','Default value')
    if x==y:
        z=User_table.objects.get(question=scq,answer=sa,username=un)
        z.password=x
        z.save()
        return render(request,'sign_in.html')

def forgot_mpin(request):
    return render(request,'forgot_mpin.html')

def fgtmpin(request):
    scq=request.GET['scq']
    ans=request.GET['sa']
    un=request.GET['uname']
    request.session['qs']=scq
    request.session['sa']=ans
    request.session['un']=un
    if User_table.objects.filter(question=scq,answer=ans,username=un):
        a=1
    else:
        a=0
    return render(request,'forgot_mpin.html',{'a':a,'x':scq,'y':ans,'z':un})

def resetmpin(request):
    x=request.GET['pass']
    y=request.GET['c_pass']
    scq=request.session.get('qs','Default value')
    sa=request.session.get('sa','Default value')
    un=request.session.get('un','Default value')
    if x==y:
        z=User_table.objects.get(question=scq,answer=sa,username=un)
        z.mpin=x
        z.save()
        return render(request,'sign_in.html')
    
def card(request):
    ac_no=request.session.get('num','Default Value')
    p = User_table.objects.get(ac_no=ac_no)
    number=p.card
    number_str = str(number)
    part_a = number_str[:4]
    part_b = number_str[4:8]
    part_c = number_str[8:12]
    part_d = number_str[12:]
    return render(request,'card.html',{'a':p,'1st':part_a,'2nd':part_b,'3rd':part_c,'4th':part_d})