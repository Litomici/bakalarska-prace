from .models import *
import csv
from datetime import datetime,timedelta
from django.db.models import Q
from Events.models import Event
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

def has_account(user):
    """
        if user is already bound to accocunt return true
    """
    try:
        # Check if the user is associated with any account
        return Account.objects.filter(users=user).exists()
    except Account.DoesNotExist:
        return False
def is_username_available(username):
    """ check function for username

    Args:
        username (string): username of new user

    Returns:
        bool: True if username is aviable
    """
    try:
        # Try to get a user with the given username
        user = User.objects.get(username=username)
        return False  # Username already exists
    except User.DoesNotExist:
        return True  # Username is available
def add_spaces(input_string):
    """ Phone number formater. from n-lenght nubers in string will make a fromat of +xx ... xxx xxx

    Args:
        input_string (string): string containing numbers

    Returns:
        string: pnone number with extra spaces
    """
    reversed_string = input_string[::-1]  # Reverse the string
    spaced_string = ' '.join(reversed_string[i:i+3] for i in range(0, len(reversed_string), 3))

    # Reverse the spaced string back to its original order
    result_string = spaced_string[::-1]
    return result_string
def isUserLogged(request):
    """function verify if user is logged

    Args:
        request (request): current request from templace

    Returns:
        bool: True if user is logged in
    """
    if request.user.is_authenticated:
        if has_account(request.user):
            return True
        else:
            return False
    return False
def send_email_with_attachments(subject, message, from_email, recipient_list, attachments=[]):
    """
    function to send and email with or with out attachments

    Args:
        subject (string): mail subject(headline)
        message (string): mail body
        from_email (string): mail to be send from
        recipient_list (list, strings): list of all emails i want to send to
        attachments (list, optional): list of path to files i want to send Defaults to [].
    """
    email = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list,
    )

    # Attach files to the email
    for attachment in attachments:
        email.attach_file(attachment)

    # Send the email
    email.send()
def isUserLoggedWithPermission(request,perm):
    """verify a user and his permission to access certain parts

    Args:
        request (request): current request
        perm (int): degree of safetty

    Returns:
        bool: True if user is logged and allowed to do such actions
    """
    if request.user.is_authenticated:
        print("user in")
        if has_account(request.user):
            print("user has account")
            # try:
            print("searching for account data")
            account = Account.objects.get(users=request.user)

            print(account.position)
            print("data loaded")
            
            if account.position >= perm:
                return True
            else:
                return False
            # except:
            #     print("unable to read data")
            #     return False
    return False
def membersAtomCheck():
    """
    function will check if newly created member is already register in assotiation of turistics. Also it means his fee was already paid. If true member will be given his ATOM_Id.
    Returns:
        bool: True if succesfuly find memeber in register and give him a Atom ID
    """
    try:
        with open("extraFiles/export.csv", 'r', encoding='Windows 1250') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            for row in csv_reader:
                matching_member = member.objects.filter(ATOM_id=row['id'])
                if not matching_member.exists():    
                    jmeno = row['Jméno']
                    surname = row['Příjmení']
                    # Query the Member model to check if a member with the given name and surname exists
                    matching_members = member.objects.filter(jmeno=jmeno, surname=surname, ATOM_id="")
                    if matching_members.exists():
                        tmpMEM = matching_members.first()
                    # Assuming the CSV has a column named 'id', update the 'id' in the CSV row
                        tmpMEM.ATOM_id=row['id']
                        tmpMEM.save()
    except Exception as e:
        return False
    return True
def getAccountByUser(user):
    return get_object_or_404(Account,users=user)
def getUsersAccount(request):
    account = get_object_or_404(Account, users=request.user)
    return account
def get_upcoming_events():
    """
    querry over Event table. Looking only for not outdated actions also sorts them by date.

    Returns:
        array[Event]: array of Evetns objects
    """
    current_date = datetime.now()
    upcoming_events = Event.objects.filter(
        Q(meeting__gte=current_date) | Q(ending__gte=current_date)
    ).order_by('meeting').distinct()

    return upcoming_events
def get_filtered_events(attributes):
    """
    filtering function for evetns by given atributes. atributes must be names of params of Event table. also sorted by meeting date

    Args:
        attributes (array[string]): array of strings representations of atributes of Event table

    Returns:
        array[Event]: array of Evetns objects
    """
    current_date = datetime.now()
    
    # Construct the dynamic filters based on the provided attributes
    dynamic_filters = Q()
    for attribute in attributes:
        filter_param = {f"{attribute}__gte": current_date}
        dynamic_filters |= Q(**filter_param)

    # Apply the filters and order by meeting datetime
    filtered_events = Event.objects.filter(dynamic_filters).order_by('meeting').distinct()

    return filtered_events
def signedMembers4Event(event):
    assigned_members = event.assigned.all()
    attending_members = event.attendance.all()

    # Získání všech členů, kteří jsou zúčastněni a přiřazeni na události
    signed_members = member.objects.filter(Q(id__in=assigned_members) & Q(id__in=attending_members))
    #signed_members = member.objects.filter(id__in=assigned_members, id__in=attending_members)

    # Vytvoření pole tuple (member, bool)
    result = [(member, member in attending_members) for member in assigned_members]


    # Přidání členů, kteří jsou buď zúčastněni nebo přiřazeni, ale ne oboje
    additional_members = member.objects.exclude(id__in=signed_members).filter(Q(id__in=assigned_members) | Q(id__in=attending_members))
    result += [(member, False) for member in additional_members]

    return result
def getMailsFromEvent(event):
    """function returns all emails connected to members asigned for given event

    Args:
        event (model): event object

    Returns:
        set: all mails that are conected to this event
    """
    # Získání seznamu všech členů přihlášených k této události
    members = event.assigned.all()
    # Pro každého člena získat všechny účty, které spravuje
    accounts = give_accounts(members)
    # Sbírání unikátních e-mailových adres těchto účtů
    emails = set()
    for account in accounts:
        emails.add(account.user.username)

    return list(emails)
def notSignedMembers(event):
    assigned_members = event.assigned.all()
    attending_members = event.attendance.all()

    # Získání všech členů, kteří nejsou přiřazeni ani zúčastněni na události
    not_signed_members = member.objects.exclude(id__in=assigned_members).exclude(id__in=attending_members)

    # Seřazení abecedně podle jména
    sorted_members = not_signed_members.order_by('jmeno')

    return sorted_members
def give_accounts(members):
    accounts = Account.objects.filter(member__in=members).distinct()
    return accounts
def thisWeekEvents():
    # Získání dnešního data
    today = datetime.now().date()
    # Vypočítání data za 7 dní
    seven_days_from_now = today + timedelta(days=7)
    # Filtrování událostí, které mají meeting za 7 a méně dní a nejsou starší než dnešní datum
    upcoming_events = Event.objects.filter(meeting__lte=seven_days_from_now, meeting__gte=today)
    
    return upcoming_events
def parse_member_string(member_str):
    parts = member_str.split("-")  # Rozdělení řetězce podle pomlček
    name = parts[0]  # Jméno je první část
    lastName = parts[1]  # Příjmení je druhá část
    year = int(parts[2])  # Rok je třetí část (převedeno na celé číslo)
    month = int(parts[3])  # Měsíc je čtvrtá část (převedeno na celé číslo)
    day = int(parts[4])  # Den je pátá část (převedeno na celé číslo)
    born = datetime(year, month, day).date()  # Vytvoření objektu datetime.date z rok-měsíc-den

    return {'name': name, 'lastName': lastName, 'born': born}
def inform_all():
  # Získání všech účtů, které mají uživatele
    all_accounts = Account.objects.all()
    # Inicializace prázdného seznamu pro e-maily
    all_emails=[]
    # Procházení všech účtů
    for account in all_accounts:
        for user in account.users.all():
            if not (user.username in all_emails):
                all_emails.append(user.username)
    return all_emails
def infrom_asigned(event):
    mails = []
    for m in event.assigned.all():
        acc=Account.objects.filter(member=m).first()
        if acc is not None:
            for user in acc.users.all():
                    if not (user.username in mails):
                        mails.append(user.username)
    return mails 
def process_string(input_string):
    if len(input_string) < 7 or len(input_string) > 13:
        raise ValueError("Input string must be between 7 and 13 characters long.")
    reversed_first_7_chars = input_string[-7:][::-1]  # Odzadu prvních 7 znaků
    remaining_chars = '024' * (10 - len(reversed_first_7_chars))  # Doplnění zbylých znaků čísly "024"
    result_string = reversed_first_7_chars + remaining_chars
    return result_string[:10]  # Oříznutí výsledného řetězce na délku 10
def getMailForAllAsigned(event):
    mails=set()
    for m in event.assigned.all():
        acc=Account.objects.filter(member=m).first()
        for u in acc.users.all():
            mails.add(u.username)
    return list(mails)




