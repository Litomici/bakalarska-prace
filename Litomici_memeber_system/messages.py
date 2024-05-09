"""
    Tento soubor obsahuje chybové hlášky a zprávy o dokončení
"""
from venv import create
import re
permDenied="Pokusili jste se navšívit stránku, pro kterou nemáte oprávnění. Museli jsme vás převést jinam"
timeOut="je nám líto, ale platnost vašeho přihlášení vypršela. Přihlaste se prosím znovu."
loginFail="Heslo a email se neschodují"
regStep1Success = "První krok registrace byl úspěšný"
regStep1PostValidFail="Chyba při registraci: zadané hodnoty obsahovali nepovolené znaky"
regStep2Success = "Druhý krok registrace byl úspěšný"
regStep2PostValidFail="Jenám líto, ale z technických důvodů se registraci nepodařilo dokončit. Odhlaste se nebo počkej a zkuste to znovu."
contacUsSuccess="Vaše zpráva byl úspěšně odeslána na centrum Litomíků."
contactUsSendFail="Omlouváme se, ale email se z technických důvodů nepodařilo odeslat. Zkuste to později nebo kontaktujte správce"
memberRemovedSuccess ="Zvolený člen byl úspěšně odebrán z vašeho účtu."
memberRemovedFail="Zadali jste nesprávný osobní kód."
memberRemovedNoSelect="Odebrání selhalo! Člen je buď již odstraněný nebo byl adminem přidělen k tomuto účtu."
addMemberSuccess="Člen byl úspěšně přidák k vašemu účtu."
addMemberFail="Je nám líto, ale podle data narození asi myslíte jiného člena."
newMemberJoined="Vypadá to, že vámi vytvořený člen není na seznamu členů se zaplaceným členským příspěvkem. Odečetli jsme vám proto cenu členství z virtuální peněženky. \n Pokud víte, že jste platili napište nám a společně to vyřešíme."
createMemberSuccess="Člen byl úspěšně vytvořen a přidán k vašemu účtu."
linkExpired="Tento odkaz již není platný. Překročil životnost 30 min nebo byl již využit."
addNewUserSuccess= "Váš účet byl úspěšně vytvořen a přidán. Prosím nyní se řádně přihlašte."
addNewUserPassFail="Vámi zadaná hesla se neshodují Zkus to znovu"
logOut="Uživatel je nyní bezpečně odhlášen"
dataChangeSuccess="Data byla úspěšně změněna."
eventEditSuccess="Změny události byly uloženy"
eventCreateSuccess="Aktivita byla úspěšně vytvořena přidána do rozvrhu"
eventCreateFail="Ups! Z technických problémů nebylo možné vytvořit událost. Zkuste to znovu nebo kontaktujte správce"
fileNotFound="Soubor je poškozený nebo došlo k chybě při jeho nahrávání."
incorectFileFormat="Nahraný soubor není ve správné formátu. Zkontroljte, že se jedná o .XML a soubor obsahuje sekci <transactions>"
def addUserfail(email):
    return f"Z technických důvodé nebylo možné kontaktovat adresu {email}. Zkuste to prosím znovu. Narážíte-li na problém opakovaně kontaktujte správce."
def addUserSuccess(email):
    return f"Pozvánka byla zaslána na {email} a má platnost 30 min. Řekněte vlastnííkovi, ať nezapomene potvrdit pozvání. "
def addUserAllrdyUsed(email):
    return f"Uživatel s emailem {email} již existuje a má svůj vlastní účet. Zkontrolujte adresu zkuste to znovu.Nebojte se nás v případě potřeby kontaktovat."

def newMemberValidFail(errors):
    msg=f"Chybně zadané informace:\n"
    regex_pattern = r'<li>(.*?)</li>'
    # Hledání shody s regulárním výrazem v HTML vstupu
    for e in errors:
        tmp=f"{e[1]}"
            # Pokud je chyba objekt ValidationError, zpracujte ji pomocí regulárního výrazu
        match = re.search(regex_pattern, tmp)
        if match:
            msg += f"{match.group(1)}\n"
        else:
            msg+=f"{e[1]}"
    return msg
def contactUsFailValid(errors):
    msg="Systém zaznamenal následující chyby:\n"
    for e in errors:
        msg+=f" {e[0]} {e[1]}\n"
    return msg
def ActionFormsInvalid(errors):
    msg="Ups! Špatně jste uvedli některé informace:"
    for e in errors:
        msg+=f" {e[0]} {e[1]}\n"
    return msg