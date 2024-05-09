from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView,PasswordResetDoneView,PasswordResetView,PasswordResetCompleteView,PasswordResetConfirmView
from Litomici_memeber_system import settings as STS

app_name = 'account'
urlpatterns = [
    #administration
    path("showMembers&Accounts",views.showMembers, name="showMembers"), # type: ignore
    path("semberDetail/<str:member_id>",views.memberDetail,name="memberDetail"), # type: ignore
    path("payment",views.seeMoney,name="payment"),
    path("economy",views.unpayed_payments,name="economy"),
    path("bankTransactions",views.bank_transactions,name="bankTransactions"),
    path("payed",views.payed_payments,name="payed"),
    path("payments",views.payments,name="payments"),
    path("notify2pay/<str:account_id>",views.notify2pay,name="notify2pay"),
    path("addMoney2pay/<str:account_id>",views.addMoney2pay,name="need2pay"),
    path("manualPayment",views.manual_payment,name="manualP"),
    #sending an email
    path("sendNotification/<int:action_id>/<int:event_id>",views.sendNotification,name="sendEmail"),#type: ignore
    path("sendMsg",views.sendMessage,name="sendMSG"),#simple message from user
    path("addNewUser",views.addUserToAccount,name="addNewUser"),#adding new user to account # type: ignore
    path("setPassword/<str:token>/",views.invitedUser,name="setPasswd"),
    #account operations
    path("account",views.userIn, name="logged"),
    path("profileInfo",views.userData, name="profile"),
    path("removeMember",views.removeMember,name="removeMemeber"),
    path("addMember",views.add_member_to_account,name="addMember"),
    path("changeData", views.changeData, name="changeData"),
    #creating new entity
    path("register",views.signUp, name="signUp"),
    path('newAccount',views.NewAccount, name='newAccount'),
    path("addEvent",views.userData, name="addEvent"),
    path("createMemeber",views.newMember,name="newMember"),
    #loging
    path("login",views.signIn, name="login"),
    path("logout",LogoutView.as_view(next_page=STS.LOGOUT_REDIRECT_URL), name="logout"),
    #password reset 
    path('password_reset/', PasswordResetView.as_view(template_name='registration/resetPass.html',from_email='turistaklitomici@gmail.com', html_email_template_name='registration/password_reset_email.html',email_template_name='registration/password_reset_email.html',success_url="done"), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='registration//password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    #errors
    path("",views.signIn, name="404"),
    #development only 
    # path("test",views.tester,name="test"),
    # path("testF",views.testF,name="testF"),
    

]
