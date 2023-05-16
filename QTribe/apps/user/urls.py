from django.urls import path, re_path

from user.views import Register, Login ,CheckUsername, CheckPhone,Transform,UpdateInformation,CheckEmail,ResetPassword,CheckPassword


urlpatterns=[
   path('register/',Register.as_view()),
   path('login/',Login.as_view()),
   re_path('check_username/(?P<username>[A-Za-z][A-Za-z0-9]{2,7})/',CheckUsername.as_view()),
   re_path('check_phone/(?P<phone>1[3589]\d{9})/',CheckPhone.as_view()),
   re_path('check_password/',CheckPassword.as_view()),
   re_path('check_email/(?P<email>[a-z0-9A-Z]+[- | a-z0-9A-Z . _]+@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-z]{2,})/',CheckEmail.as_view()),
   path('transform/', Transform.as_view()),
   path('update_information/', UpdateInformation.as_view()),
   path('reset_password/', ResetPassword.as_view()),

]