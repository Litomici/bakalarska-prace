from django.urls import path,include
from . import views
from django.contrib.auth.views import LogoutView,PasswordResetDoneView,PasswordResetView,PasswordResetCompleteView,PasswordResetConfirmView


app_name = 'event'
urlpatterns = [
    path("listAll/<int:event_id>/",views.listAll,name="listAll_id_add"),
    path("listAll",views.listAll,name="listAll"),
    path("details/<int:event_id>/",views.details,name="details"),
    path("listCamps",views.listCamps,name="listCamps"),
    path("campRegister/<int:event_id>",views.campReg,name="campRegister"), # type: ignore
    path("eventTool",views.eventActions,name="tool"), # type: ignore
    path("eventTool/create",views.eventActionsCreate,name="tool-create"),
    path("eventTool/edit",views.eventActionEdit,name="tool-edit"),
    path("eventTool/attendance",views.eventActionAttendace,name="tool-attendace"),
    path("eventTool/attendanceOfEvent/<int:event_id>/",views.eventActionAttendace2Event,name="tool-attendace2Event"),
    path("eventTool/cancel",views.eventActionCancle,name="tool-cancel"),
    path("eventTool/cancelOfEvent/<int:event_id>",views.cancelingOfEvent,name="tool-cancelOfEvent"),#type: ignore
]
