from asyncio import events
from email import message
from django.utils import timezone
from django.http import Http404, HttpResponse
from Litomici_memeber_system.settings import EMAIL_HOST_USER
from .forms import ContactForm
from django.shortcuts import render
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from Litomici_memeber_system import settings
from Litomici_memeber_system import messages as MSG
from .models import Account,EmailConfirmation
from datetime import datetime,date
import xml.etree.ElementTree as ET
from .forms import *
from .tools import *
# from Events.forms import EventForm
# from Events.models import *
#send message
"""
    sednNotification
    funkce odešle email s textem podle druhu akce.
    Seznam akcí:
        1) Oznámení nové akce - běžné
        2) Oznámení nové akce -veřejnost
        3) Oznámení nové akce - novinka
        4) Oznámení nové akce - Výroční
        5) Upozornění pro zapsané - aby nezapomněli
        6) Upozornění pro nezapsané - Poslední možnost
    
"""
def sendNotification(request,action_id,event_id):
    if isUserLoggedWithPermission(request,2):
        subject=""
        msg=""
        send_to=[]
        info_about=Event.objects.filter(id=event_id).first()
        time_date=info_about.meeting.strftime("%d.%m.%Y")
        time_time=info_about.meeting.strftime("%H:%M")
        if action_id == 1:
            subject=f"Nová akce v plánu. Honem se pojď zapsat na {info_about.name}"
            msg=f"Zdavíme Litomíky a naše příznivce\n\nPrávě jsem přidali novou událost {info_about.name}, která začne v {info_about.meeting}. Doufáme, že se tam setkáme v co největším počtu a pořádně si to spolu užijeme. Zapište prosím, ať víme, kolik nás na akci bude.\n \n Děkujeme a těšíme se na vás!\nVaši Litomíci  "
            send_to=inform_all()
        elif action_id == 2:
            subject=f"Důležitá akce v plánu. Zapiš se co nejdřív na akci {info_about.name}"
            msg=f"Zdavíme Litomíky a naše příznivce\n\nZrovna jsem vytvořili novou událost pro veřejnost {info_about.name}, která se bude konat {time_date}. Akci je pro nás moc důležitá, a tak prosíme zapište se a opravdu doražte. Ideálně vemte rodinu, kamaráda, kamarádku a s dobrou náladou si přijďte užít spoustu zábavy.\n\n Děkujeme za podporu a těšíme se na vás!\nVaši Litomíci  "
            send_to=inform_all()
        elif action_id == 3:
            subject=f"Pozor, máme tady novinku, Tak se rychle zapiš!"
            msg=f"Zdavíme Litomíky a naše příznivce\n\nAkorát jsem do našeho plánu přidali novinku {info_about.name}. Naplánovali jsme ji na {time_date}. Jelikož se jedná o něco nového doufáme, že zvědavost zvítězí a bude nás co možná nejvíce. Pokud bude mít akce úspěch určitě jí v budoucnu rádi zopakujeme. Tak neváhej a pojď se zapsat. Nový zážitek už čeká!\n\n Přejeme pěkný den  těšíme se na vás!\nVaši Litomíci  "
            send_to=inform_all()
        elif action_id ==4 :
            subject=f"A je to tu zase. Zapiš se na tradiční {info_about.name}"
            msg=f"Zdavíme Litomíky a naše příznivce\n\n opět tu pro vás máme {info_about.name}. Začátek jsme naplánovali na {time_date}. Akci není třeba představovat neboť se jedná o každoroční záležitost. A pokud jsi nováček, tak jediné co potřebuješ vědět je, že tohle určitě nechceš propásout. \n\n Přeje vám pěkný den a těšíme se na vás!\nVaši Litomíci  "
            send_to=inform_all()
        elif action_id == 5:
            subject=f"Nezapomeň! {info_about.name} ({time_date} od {time_time})"
            send_to=infrom_asigned(info_about)
            msg=f"Zdavíme Litomíky a naše příznivce\n\n {info_about.name}, se rychle blíží, a tak nezapomeňte, že {time_date} v {time_time}být připraveni. Místo srazu je {info_about.departure}. S sebou si vzměnte: {info_about.notes}\n\n Těšíme se na vás\nVaši Litomíci"
        elif action_id== 6 :
            subject=f"Poslední možnost! {info_about.name} ({time_date} od {time_time})"
            send_to=infrom_asigned(info_about)
            msg=f"Zdavíme Litomíky a naše příznivce\n\n stále máme volná místa. {info_about.name}, se rychle blíží, a tak se nezapomeňte zapsat a dorazit. Začínáme {time_date} v {time_time}. Místo srazu je {info_about.departure}. Čím více nás bude tím více zábavy si užijeme, tak nebuď labuť a koukej přijít mezi nás.\n\n Brzo naviděnou a příjemný zbytek dne\nVaši Litomíci"
        email = EmailMessage(
            subject=subject,
            body=msg,
            from_email="turistaklitomici@gmail.com",  # You can set a default email in your settings.py
            to=send_to,
        )
        # attachment_paths=["extraFiles/bezinfekcnost.pdf"]
        # # Attach files
        # for attachment_path in attachment_paths:
        #     with open(attachment_path, 'rb') as file:
        #         email.attach_file(attachment_path)
        email.send(fail_silently=False)
        messages.success(request,"Upozornění bylo všem úspěšně odesláno.")
        return redirect(request.META.get('HTTP_REFERER'))
    if isUserLogged(request):
        messages.error(request,"K tomuto nemáte oprávnění!")
        return redirect("account:profile")
    else:
        messages.error(request, MSG.timeOut)   
def addMoney2pay(request,account_id):
    if isUserLoggedWithPermission(request,2):
        a = get_object_or_404(Account, id=account_id)
        if request.method == 'POST':
            a.wallet-=(int)(request.POST.get('2pay'))
            a.save()
        return redirect("account:payments") 
    return redirect("account:profile")
def notify2pay(request,account_id):
    if isUserLoggedWithPermission(request,2):
        a = get_object_or_404(Account, id=account_id)
        money=-1*a.wallet
        addrs=[]
        for m in a.users.all():
            addrs.append(m.username)
        msg=f"Dobrý den,\n V našem systému evidujeme neuhrazenou částku {money} Kč. Chtěli bychom vám touto formou připomenout, že částku je třeba v blízké době uhradit, jiank se čelnové toho účtu nebudou moci zúčastňovat našich aktivit.\n Děkuji za pochopení.\n\n Pěkný zbytek dne přejí vaši Litomíci."
        email = EmailMessage(
        subject=f"Neuhrazená částka účtu",
        body=msg,
        from_email="turistaklitomici@gmail.com",  # You can set a default email in your settings.py
        to=addrs,
    )
        email.send(fail_silently=False)
        messages.success(request,"email odeslán")
        
        return redirect("account:payments")
    else:
        return userIn(request)
def seeMoney(request):
    if request.user.is_authenticated and not has_account(request.user):
                messages.success(request,MSG.regStep1Success)
                return redirect('account:newAccount')  # Change 'next_step_registration' to your actual URL
    if isUserLogged(request):
        account = getUsersAccount(request)
        if request.method == 'POST':
            unpaid_payments = payment.objects.filter(account_id=account.id, confirmed=False)
            if unpaid_payments.exists():
                sum=0
                for p in unpaid_payments:
                        sum+=p.amount
                if sum==(-1*account.wallet):
                    messages.success(request,"O vaší platbě už víme, můžete ji vidět v historii plateb")
                else:
                    payment_instance = payment(
                    amount= (int)(request.POST.get('amount')),
                    confirmed=False,
                    account_id=account.id,
                    var_symbol=request.POST.get('vars'),
                    payed_in_cash=False
                    )
                    payment_instance.save()
                    messages.success(request,"Platba nyní čeká na potvrzení bakny. Akce může trvat až 5 dní, a tak vám dáme vědět, že je vše v pořádku na email. ")
                    return redirect("account:payment")
            else:
                    payment_instance = payment(
                    amount= (int)(request.POST.get('amount')),
                    confirmed=False,
                    account_id=account.id,
                    var_symbol=request.POST.get('vars'),
                    payed_in_cash=False
                    )
                    payment_instance.save()
                    messages.success(request,"Platba nyní čeká na potvrzení bakny. Akce může trvat až 5 dní, a tak vám dáme vědět, že je vše v pořádku na email. ")
                    return redirect("account:payment")
   
        #sendNotification()
        strng="Platba z aplikace za"
        for m in account.member.all():
            strng+=m.surname+","
        unpaid_payments = payment.objects.filter(account_id=account.id, confirmed=False).all()
        if unpaid_payments.exists():
            sum=0
            for p in unpaid_payments:
                sum+=p.amount
            if sum<(-1*account.wallet):
               missing=-1*(account.wallet+sum)
            else:
                missing=0
        else:   
            missing=account.wallet*(-1)                 
        paymentData={
            "amount":missing,
            "IBAN":"213749613",
            "bankCode":"0600",
            "company":"Turistický oddíl mládeže Litomíci",
            "msg": strng,
            "vars":process_string(account.mobile2),
            
        }
        wainting=payment.objects.filter(account_id=account.id).all()[::-1]
        dic={
            "role": account.position,#0=user;1=leader;2=econom;3=admin
            "email": request.user.username,
            "lastlog":request.user.last_login,
            "payment":paymentData,
            "waiting": wainting
        }    
        return render(request,"tags/mains/payment.html",dic)
    messages.error(request,MSG.timeOut)
    return render(request,"index.html")
def manual_payment(request):
    if isUserLoggedWithPermission(request,2):
        account = getUsersAccount(request)
        accounts=Account.objects.all()
        dic={
            "role":account.position,
            "action":4, 
            "accounts":accounts,  
        }
        if request.method == 'POST':
            RP=request.POST
            acc = get_object_or_404(Account, id=RP.get("acc"))

            if RP.get("paymentType") == "option1":
                p = payment(
                    amount=(int)(RP.get("amount")),
                    confirmed=True,
                    account=acc,
                    payment_from=RP.get("from"),
                    payed_date=RP.get("payed"),
                    transaction_number=RP.get("nmT"),
                    payed_in_cash=False,
                    var_symbol=RP.get("Vs"),
                )
                p.save()
                acc.wallet+=(float)(RP.get("amount"))
                messages.success(request,"platba zadána do systému")
            else:
                p = payment(
                    amount=(int)(RP.get("amount")),
                    confirmed=True,
                    account=acc,
                    payed_date=RP.get("payedOn"),
                    payed_in_cash=True,
                    var_symbol=RP.get("VsP"),
                )
                p.save()
                acc.wallet+=(float)(RP.get("amount"))
                acc.save
                messages.success(request,"platba zadána do systému")
            return redirect("account:payments") 
        
        return render(request,'tags/mains/economy.html',dic)
    else:
        return redirect("account:login")
def payed_payments(request):
    if isUserLoggedWithPermission(request,2):
        account = getUsersAccount(request)
        payments = payment.objects.filter(confirmed=True).order_by('-payed_date').all()
        dic={
            "role":account.position,
            "action":2,
            "payments":payments,
        }
        return render(request,'tags/mains/economy.html',dic)
    else:
        return redirect("account:login")
def unpayed_payments(request): 
    if isUserLoggedWithPermission(request,2):
        account = getUsersAccount(request)
        payments = payment.objects.filter(confirmed=False).order_by('-creation_date').all()
        dic={
            "role":account.position,
            "action":1,
            "payments":payments,
        }
        if request.method == 'POST':
            RP=request.POST
            acc = get_object_or_404(Account, id=RP.get("acc"))
            p = get_object_or_404(payment, payment_id=RP.get("Pid"))   
            p.confirmed=True
            p.payment_from=RP.get("from")
            p.payed_date=RP.get("payed")
            p.transaction_number=RP.get("nmT")
            p.payed_in_cash=False
            p.save()
            acc.wallet+=(float)(p.amount)
            acc.save()
            email = EmailMessage(
            subject=f"Vaše platba dorazila",
            body=f"Litomíci zdravý,\n právě jsme obdrželi vaši platbu. Částka byla přičtena k vašemu účtu. Můžete se o tom přesvědčit ve vašem profilu. Když už budete přihlášení byla by škoda nepodívat se jaké kace plánujeme v blízké době a nějakou s přihlásit. Rádi vás uvidíme.\nDěkujeme za vaši přízeň a těšíme se na naše příští setkání.\n \n S přáním pěkného dne,\nVaši Litomíci",
            from_email="turistaklitomici@gmail.com",  # You can set a default email in your settings.py
            to=["sibik@seznam.cz","charouzd.f@seznam.cz"],
        )
            messages.success(request,"Platba byla úspěšně potvrzena v systému")
        return render(request,'tags/mains/economy.html',dic)
    else:
        return redirect("account:login")
def payments(request):
    if isUserLoggedWithPermission(request,2):
        account = getUsersAccount(request)
        accounts=Account.objects.all()
        dic={
            "role":account.position,
            "action":3,
            "acounts":accounts,    
        }
        return render(request,'tags/mains/economy.html',dic)
    else:
        return redirect("account:login")
def bank_transactions(request):
    if isUserLoggedWithPermission(request,2):
        account = getUsersAccount(request)
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                # Zpracování nahraného souboru
                uploaded_file = request.FILES['file']
                try:
                    # Načtení XML souboru
                    tree = ET.parse(uploaded_file)
                    root = tree.getroot()
                    # Hledání větve transactions
                    transactions = root.find('transactions')
                except:
                    messages.error(request,MSG.incorectFileFormat)
                if transactions is not None:
                    conf=0
                    err=0
                    unrecognized_paments=[]
                    # Projdeme všechny transakce
                    for transaction in transactions.findall('transaction'):
                        if (float)(transaction.get("amount")) < -0.000001:
                            continue
                        other_account_number = transaction.get('other-account-number')
                        if other_account_number != "":#pokud je příchozí
                            confirmed_payment = payment.objects.filter(transaction_number=transaction.get("id"))
                            if not confirmed_payment.exists():# pokud není už v systému
                                print(f"platba s var symbolem {transaction.get('var-sym')}neni v systemu")
                                unconfirmed_payments = payment.objects.filter(var_symbol=transaction.get("var-sym"), confirmed=False)
                                er=0
                                if(not unconfirmed_payments):
                                    err+=1
                                    tmp=""
                                    trn_messages = transaction.findall('.//trn-messages[@type="advice"]')
                                    # Projdeme všechny nalezené trn-messages elementy
                                    for trn_message in trn_messages:
                                        # Získání obsahu trn-message
                                        tmp = tmp + " "+ (str)(trn_message.find('.//trn-message').text)
                                    tran={
                                        "id" : transaction.get('id'),
                                        "date_post": transaction.get('date-post'),
                                        "date_eff": transaction.get('date-eff'),
                                        "var_sym" : transaction.get('var-sym'),
                                        "con_sym" : transaction.get('con-sym'),
                                        "spec_sym": transaction.get('spec-sym'),
                                        "amount" : transaction.get('amount'),
                                        "contactless":  transaction.get('contactless'),
                                        "mobile": transaction.get('mobile'),
                                        "orig_ref" : transaction.get('orig-ref'),
                                        "date_action" :transaction.get('date-action'),
                                        "mobile_payment" : transaction.get('mobile-payment'),
                                        "msg": tmp
                                    }
                                    unrecognized_paments.append(tran)       
                                    
                                for p in unconfirmed_payments:#najdu všechny nepotvrzené platby účtu a porovnám částky
                                    if (float)(p.amount) == (float)(transaction.get("amount")):
                                        p.confirmed=True
                                        p.payed_date=datetime.strptime(transaction.get("date-eff"), "%Y-%m-%d").date() # type: ignore
                                        p.payment_from=other_account_number # type: ignore
                                        p.transaction_number=transaction_number=transaction.get("id")
                                        p.save()
                                        a=Account.objects.filter(user=p.account).first()
                                        a.wallet+=(float)(transaction.get("amount"))
                                        conf+=1
                                        er=0
                                        break
                                    else:
                                        er+=1
                                if er>0:#když se neshodují přidám do feeedbaku jako nezařazenou
                                    print("notFound")
                                    err+=1
                                    tmp=""
                                    trn_messages = transaction.findall('.//trn-messages[@type="advice"]')
                                    # Projdeme všechny nalezené trn-messages elementy
                                    for trn_message in trn_messages:
                                        # Získání obsahu trn-message
                                        tmp = tmp + " "+ (str)(trn_message.find('.//trn-message').text)
                                    tran={
                                        "id" : transaction.get('id'),
                                        "date_post": transaction.get('date-post'),
                                        "date_eff": transaction.get('date-eff'),
                                        "var_sym" : transaction.get('var-sym'),
                                        "con_sym" : transaction.get('con-sym'),
                                        "spec_sym": transaction.get('spec-sym'),
                                        "amount" : transaction.get('amount'),
                                        "contactless":  transaction.get('contactless'),
                                        "mobile": transaction.get('mobile'),
                                        "orig_ref" : transaction.get('orig-ref'),
                                        "date_action" :transaction.get('date-action'),
                                        "mobile_payment" : transaction.get('mobile-payment'),
                                        "msg": tmp
                                    }
                                    unrecognized_paments.append(tran)
                form = UploadFileForm()
                dic={
                    "role":account.position,
                    "action":5,
                    "form":form,
                    "postDone":True,
                    "fail":err,
                    "succ":conf,
                    "unknown":unrecognized_paments,
                    
                }
                print("finito")
                return render(request,'tags/mains/economy.html',dic)
            else:
                messages.error(request,MSG.fileNotFound)
        form = UploadFileForm()
        
        dic={
            "role":account.position,
            "action":5,
            "postDone":False,
            "form":form,
            
        }
        return render(request,'tags/mains/economy.html',dic)
    else:
        return redirect("account:login")
def sendMessage(request):
    if isUserLogged(request):
        account = getUsersAccount(request)
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                text = form.cleaned_data['text']
                text= "dne "+ datetime.now().strftime("%d.%m.%Y %H:%M")+"\n"+text+"\n"+request.user.username
               # Change the email settings as per your configuration
                # recipient_email = settings.EMAIL_HOST_USER
                # sender_email = settings.EMAIL_HOST_USER
                try:            
                    send_mail(
                        subject,
                        text,
                        request.user.username,
                        ['turistaklitomici@gmail.com'],
                        fail_silently=False,
                    )
                    # Redirect after successful form submission
                    messages.success(request,MSG.contacUsSuccess)
                except Exception as e:
                    messages.error(request,MSG.contactUsSendFail)
                    form = ContactForm()
                    return render(request, 'tags/mains/contacts.html', {'form': form,"done":1,'role':account.position,})
                return HttpResponseRedirect('sendMsg')
            else:
                errs=form.errors.items()
                messages.error(request,MSG.contactUsFailValid(errs))
                form = ContactForm()
                return render(request, 'tags/mains/contacts.html', {'form': form,"done":2,'role':account.position,})    
        else:
            form = ContactForm()
        return render(request, 'tags/mains/contacts.html', {'form': form,"done":3,'role':account.position,})
    else:
        messages.error(request,MSG.timeOut)
        return redirect("account:login")
#member operations
def showMembers(request):
    if isUserLoggedWithPermission(request,1):
        account = getUsersAccount(request)
        allMembers=member.objects.all()
        member2pass=[]
        for m in allMembers:
            if Account.objects.filter(member=m).first():
                
                member2pass.append(
                    {
                        "name":f"{m.jmeno} {m.surname}",
                        "born":m.birthday,
                        "phone":Account.objects.filter(member=m).first().mobile1,
                        "id":f"{m.jmeno}-{m.surname}-{m.birthday}"
                    })
            else:
                member2pass.append(
                    {
                        "name":f"{m.jmeno} {m.surname}",
                        "born":m.birthday,
                        "phone": "není uvedeno",
                        "id":m
                    })
        dic={
            "role": account.position,#0=user;1=leader;2=econom;3=admin
            "members":member2pass,
            "events":Event.objects.all().order_by('-meeting'),
            "day":date.today()
        }
        
        return render(request,"tags/mains/allMembers.html",dic)
    else:
        if isUserLogged(request):
            messages.error(request, MSG.permDenied)
        else:
            messages.error(request,MSG.timeOut)
        return redirect("account:login")
def memberDetail(request,member_id):
    if isUserLoggedWithPermission(request,1):
        member_info = parse_member_string(member_id)
        try:
            found_member = member.objects.get(jmeno=member_info['name'], surname=member_info['lastName'], birthday=member_info['born'])
            accounts_with_member = Account.objects.filter(member=found_member).first()
            events_with_member_assigned = Event.objects.filter(assigned=found_member.id)
            events_with_member_attended = Event.objects.filter(attendance=found_member.id)
            if accounts_with_member:
                res= f"nalezen {found_member.jmeno} {found_member.surname}\n {found_member.healthProblems}\n a patří k účtu{accounts_with_member.user}"
            dic={
                "role":getUsersAccount(request).position,
                "member":found_member,
                "account":accounts_with_member,
                "signedEvents":events_with_member_assigned.all(),
                "attendedEvents":events_with_member_attended.all(),
            }
            return render(request,"tags/mains/memberDetails.html",dic)
        except member.DoesNotExist:
            messages.error(request, "Hledaný člen nebyl nalezen. Zkuste to znovu nebo kontaktujte správce.")
        return showMembers(request)
    else:
        if isUserLogged(request):
            messages.error(request, MSG.permDenied)
        else:
            messages.error(request,MSG.timeOut)
        return userIn(request)
    return
def removeMember(request):
    if isUserLogged(request):
        account = getUsersAccount(request)
        membersInAccount = account.member.all()

        if request.method == 'POST':
            selected_member_id = request.POST.get('member_id')
            if selected_member_id:
                selected_member = member.objects.get(pk=selected_member_id)
                if selected_member.ATOM_id == (request.POST.get("Atom")):
                    account.member.remove(selected_member)
                    account.save()
                    messages.success(request,MSG.memberRemovedSuccess)
                    return redirect('account:profile')  # Redirect to the member list view or another appropriate view
                else:
                    messages.error(request,MSG.memberRemovedFail)
                    context = {
                    'available_members': membersInAccount,
                    'role':account.position,
                    }
                    return render(request, 'tags/mains/removeMember.html', context)
            else:
                messages.error(request,MSG.memberRemovedNoSelect)
        context = {
            'available_members': membersInAccount,
            'role':account.position,
        }
        return render(request, 'tags/mains/removeMember.html', context)
    else:
        messages.error(request,MSG.timeOut)
        return redirect('account:login')
def add_member_to_account(request):
    if isUserLogged(request):
 # Get the currently logged-in account
        account = getUsersAccount(request)
    # Get members associated with the current account
        members_in_account = account.member.all()
    # Get all members and find those not in the current account
        all_members = member.objects.all()
        aviable_members = all_members.exclude(pk__in=members_in_account)
        if request.method == 'POST':
            selected_member_id = request.POST.get('member_id')
            if selected_member_id:
                selected_member = member.objects.get(pk=selected_member_id)
                born_date = request.POST.get('born')
                print("input "+born_date)
                print(selected_member.birthday)
                if selected_member.birthday.__str__() == born_date:
                    print("Match")
                    account.member.add(selected_member)
                    account.save()
                    messages.success(request,MSG.addMemberSuccess)
                    return redirect('account:profile')  # Redirect to the member list view or another appropriate view
                else:
                    print("nomatch")
                    # messages.error(request,MSG.timeOut)
                    messages.error(request,MSG.addMemberFail)                
            else:
                print("fail")
                messages.error(request,MSG.addMemberFail)
        context = {
            'available_members': aviable_members,
            'role':account.position,
        }
        return render(request, 'tags/mains/addMember.html', context)
    else: 
        messages.error(request,MSG.timeOut)
        return redirect('account:login')
def newMember(request):
    if isUserLogged(request):
        account = getUsersAccount(request)
        if request.method == 'POST':
            form = NewMemeberForm(request.POST)
            print(form.errors.as_text())
            if form.is_valid():
                newMember=form.save()
                request.user.account.member.add(newMember)
                if not membersAtomCheck():
                    account = getUsersAccount(request)
                    account.wallet+=(-1000)
                    messages.success(request,MSG.newMemberJoined)
                else:    
                    messages.success(request, MSG.createMemberSuccess)
                return redirect('account:profile')  # Replace 'success_page' with the desired success page name or URL
            else:
                messages.error(request, MSG.newMemberValidFail(form.errors.items()))
                form = NewMemeberForm()
                return render(request, 'tags/mains/newMember.html', {'form': form,"role":account.position})
        else:
            form = NewMemeberForm() 
        return render(request, 'tags/mains/newMember.html', {'form': form,"role":account.position})
    else:
        messages.error(request,MSG.timeOut)
        return redirect("account:login")    
#Creating account
def signUp(request):#prvni krok registrace
    if request.user.is_authenticated and not has_account(request.user):
        messages.success(request,MSG.regStep1Success)
        return redirect('account:newAccount')  # Change 'next_step_registration' to your actual URL
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            
            user = form.save()
            # Log in the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the next step of registration (adjust the URL accordingly)
                messages.success(request,MSG.regStep1Success)
                return redirect('account:newAccount')  # Change 'next_step_registration' to your actual URL
            else:
                messages.error(request,MSG.regStep1PostValidFail)
        else:
            messages.error(request,MSG.newMemberValidFail(form.errors.items()))
            form=UserRegistrationForm()
            return render(request, "tags/mains/registerUser.html", {'form': form})
    else:
        form = UserRegistrationForm()       
    # labels settup
        form.fields['password2'].help_text = ''
        form.fields['username'].help_text = ''
        form.fields['password1'].label = 'Heslo'
        form.fields['password1'].help_text = 'Heslo musí mít alespoň 8 znaků\n Musí mít písmeno i číslo\nNesmí nesmí být již používané'
        form.fields['password2'].label = 'Potvrzení Hesla'
    return render(request, "tags/mains/registerUser.html", {'form': form})
def NewAccount(request):#druhý krok registrace
    
    if not request.user.is_authenticated:#přihlášení už je propadlé
        messages.error(request,MSG.timeOut)
        return redirect("account:login")
    if has_account(request.user):#uživatel je přihlášen 
        return HttpResponseRedirect("logged")
    if request.method == "POST":
        form = NewAccountForm(request.POST)
        tmp=form.is_valid()
        if form.is_valid():
            tmpr = form.save()#commit=False
            tmpr.user = request.user  # Assign the logged-in user
            tmpr.users.add(request.user)
            tmpr.save()
            if tmp is not None:
                messages.success(request,MSG.regStep2Success)
                # Redirect to the next step of registration (adjust the URL accordingly)
                return HttpResponseRedirect("account")
            else:
                form = NewAccountForm(initial={'user': request.user})
                messages.error(request,MSG.regStep2PostValidFail)
                return render(request, "tags/mains/accountRegister.html", {'form': form,"username":request.user.username})
        else:
            messages.error(request,MSG.newMemberValidFail(form.errors.items()))
            form = NewAccountForm(initial={'user': request.user})
            return render(request, "tags/mains/accountRegister.html", {'form': form,"username":request.user.username})
    else:
        form = NewAccountForm(initial={'user': request.user})
        return render(request, "tags/mains/accountRegister.html", {'form': form,"username":request.user.username})
    
def addUserToAccount(request):
    if isUserLogged(request):
        account = getUsersAccount(request)
        if request.method == 'POST':
            form = AddUserForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['newUserEmail']
                if not is_username_available(email):
                    form = AddUserForm()
                    messages.error(request,MSG.addUserAllrdyUsed(email))
                    return render(request, 'tags/mains/userInvite.html', {'form': form,'role':account.position,})
            # Generate and send confirmation link
                try:
                    email_confirmation = EmailConfirmation.create(email=email,sender=request.user.username)
                    print("povedlo se")
                    email_confirmation.send_confirmation_email()
                    print("povedlo se 2")
                    messages.error(request,MSG.addUserSuccess(email))
                    return render(request, 'tags/mains/userInvite.html', {'form': form,'role':account.position,})
                except Exception as e:
                    form = AddUserForm()
                    print("Exception:", e)
                    messages.error(request,MSG.addUserfail(email))
                    return render(request, 'tags/mains/userInvite.html', {'form': form,'role':account.position,})
        else:            
            form = AddUserForm()      
            return render(request, 'tags/mains/userInvite.html', {'form': form,'role':account.position,})
    else:
        messages.error(request,MSG.timeOut)
        return ('account:login')
def invitedUser(request, token):
    email_confirmation = get_object_or_404(EmailConfirmation, token=token)
    sender=token.split("=>")[0]
    user= User.objects.get(username=sender)
    account= getAccountByUser(user)
    #kontrola expirace
    time_difference = timezone.now() - email_confirmation.created_at
    if time_difference.total_seconds() > 1800:  # 600 seconds = 10 minutes=>1800s=30min
        # Link has expired, delete the instance and raise Http404
        email_confirmation.delete()
        raise Http404(MSG.linkExpired)
    email = email_confirmation.email
    #dokončení registrace
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            pass1=form.cleaned_data['password1']
            pass2=form.cleaned_data['password2']
            if pass1==pass2:
                usr=User.objects.create_user(username=email, password=pass1)
                usr.save()
                account.users.add(usr)
                messages.success(request, MSG.addNewUserSuccess)
                email_confirmation.delete()  # Remove the email confirmation record
                return redirect('account:login')  # Redirect to login page or wherever you want
            else:
                messages.error(request,MSG.addNewUserPassFail)
        else:
            messages.error(request,MSG.newMemberValidFail(form.errors.items()))
    else:
        form = SetPasswordForm()

    return render(request, 'tags/mains/invitedUserPassword.html', {'form': form, 'email': email})
# Logging
def userIn(request):
    if request.user.is_authenticated and not has_account(request.user):
                messages.success(request,MSG.regStep1Success)
                return redirect('account:newAccount')  # Change 'next_step_registration' to your actual URL
    if isUserLogged(request):
        #sendNotification()
        account = getUsersAccount(request)
        dic={
            "role": account.position,#0=user;1=leader;2=econom;3=admin
            "email": request.user.username,
            "lastlog":request.user.last_login,
        }    
        return render(request,"tags/mains/welcomeUserScreen.html",dic)
    messages.success(request,MSG.timeOut)
    return render(request,"index.html")
def signIn(request):
    if isUserLogged(request):
        return redirect("account:logged")
    if request.user.is_authenticated and not has_account(request.user):
                messages.success(request,MSG.regStep1Success)
                return redirect('account:newAccount')  # Change 'next_step_registration' to your actual URL
    if request.method=="POST":
        uname = request.POST.get("mail")
        passwd = request.POST.get("pass")
        user = authenticate(username=uname,password=passwd)
        if user is not None:
            login(request,user)
            if request.user.is_authenticated and not has_account(request.user):
                messages.success(request,MSG.regStep1Success)
                return redirect('account:newAccount')  # Change 'next_step_registration' to your actual URL
            return redirect("account:logged")
    return render(request, "index.html")
def sign_out(request):
    logout(request)
    messages.success(request,MSG.logOut)
    return signIn(request)
# account data
def userData(request):
    dic={
        
        "secondaryContact": False,
        "addr1": "",
        "mobile1": "",
        "mail": "",
        "addr2":"",
        "mobile2": "",
        "members": "",
        "wallet":"",
        "payment":""  
    }
    #2111093800/2700
    if isUserLogged(request):
        account = getUsersAccount(request)
        usernames = account.users.values_list('username', flat=True)
        usernamesSTR = ', '.join(usernames)
        toPay=-1*account.wallet
        members_surnames = set()

        # Získání všech příjmení členů v seznamu member daného účtu
        for member in account.member.all():
            members_surnames.add(member.surname)
        msg="Platba za členy: "
        for m in members_surnames:
            msg+=("/"+m)
        if len(account.mobile1) >= 9:
            varS=account.mobile1[-9:]
        else:
            varS="404"
        payCode=f"http://api.paylibo.com/paylibo/generator/czech/image?accountNumber=2111093800&bankCode=2700&amount={toPay}&currency=CZK&recipientName=Turistický oddíl Litomíci&vs={varS}&message={msg}"
        dic={
            "role": account.position,#0=user;1=leader;2=econom;3=admin
            "mail":usernamesSTR,
            "addr1": account.addres1 + ", "+account.city1 + " " +account.psc1,
            "mobile1": add_spaces(account.mobile1),
            "wallet":account.wallet,
            "lastlog":request.user.last_login,
            "payLink":payCode,
        }
        if account.addres2 == "" or account.psc2 == "" or account.city2 == "":
            dic["secondaryContact"]=False
        else:
            dic["secondaryContact"]=True
            dic["addr2"]= account.addres2 + ", "+account.city2 + " " +account.psc2,
        if account.mobile2 is not None:
            dic["mobile2"]=add_spaces(account.mobile2)
        members=account.member.all()
        for m in members:
            print(m.jmeno)
        if members:
            dic["members"]=members
        else:
            dic["members"]=[]
        return render(request,"tags/mains/profile.html",dic)
    messages.error(request,MSG.timeOut)
    return redirect("account:login")
def changeData(request):
    if isUserLogged(request):
        account = getUsersAccount(request)
        if request.method == 'POST':
            form = changeDataForm(request.POST)
            if form.is_valid():
                state1 = form.cleaned_data["state1"]
                state2=form.cleaned_data["state2"]
                account.mobile1 = form.cleaned_data['mobile1']
                account.mobile2 = form.cleaned_data['mobile2']
                account.addres1=form.cleaned_data['addres1']
                account.addres2=form.cleaned_data['addres2']
                account.psc1=form.cleaned_data['psc1']
                account.psc2=form.cleaned_data['psc2']
               
                
                if state1 !="Česko":
                    tmp=form.cleaned_data['city1']+"("+state1+")"
                    account.city1=tmp
                else:
                    account.city1=form.cleaned_data['city1']
                if state2 !="Česko":
                    tmp=form.cleaned_data['city2']+"("+state2+")"
                    account.city2=tmp
                else:
                    account.city2=form.cleaned_data['city2']
                account.city2=form.cleaned_data['city2']
                account.mobile1
                account.save()
                messages.success(request,MSG.dataChangeSuccess)
                return redirect("account:profile")
            else:
                messages.error(request,MSG.newMemberValidFail(form.errors.items()))
        form = changeDataForm()
        form.fields['mobile1'].initial=account.mobile1
        form.fields['mobile2'].initial=account.mobile2
        form.fields['city1'].initial=account.city1
        form.fields['city2'].initial=account.city2
        form.fields['psc1'].initial=account.psc1
        form.fields['psc2'].initial=account.psc2
        form.fields['addres1'].initial=account.addres1
        form.fields['addres2'].initial=account.addres2
        dic={
        "role": account.position,#0=user;1=leader;2=econom;3=admin
        "form": form,
    }
        return render(request,"tags/mains/accountDataChange.html",dic)   
    else:
        messages.error(request,MSG.timeOut)
        return redirect("account:login")
def nothingToShow(request):
    return render(request,"blindPath.html")
# def tester(request):
#     tmp=membersAtomCheck()
#     return render(request,"tags/mains/welcomeUserScreen.html",{"email":tmp})
# def test2(request):
#     return render(request,"tags/content.html")
# def testF(request):
    return redirect("testF")