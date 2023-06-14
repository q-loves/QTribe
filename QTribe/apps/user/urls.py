from django.urls import path, re_path

from user.views import Register, Login ,CheckUsername, CheckPhone,Transform,UpdateInformation,CheckEmail,ResetPassword,\
                       CheckPassword,UploadImage,Logout,FocusUser,UserSearchView,MakeFriend,ResponseFriend,RefuseFriend,\
                       ReadMessage



urlpatterns=[
   path('register/',Register.as_view()),
   path('login/',Login.as_view()),
   re_path('check_username/(?P<username>[A-Za-z][A-Za-z0-9]{2,7})/',CheckUsername.as_view()),
   re_path('check_phone/(?P<phone>1[3589]\d{9})/',CheckPhone.as_view()),
   re_path('check_password/',CheckPassword.as_view()),
   re_path('check_email/(?P<email>[a-z0-9A-Z]+[- | a-z0-9A-Z . _]+@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-z]{2,})/',CheckEmail.as_view()),
   path('transform/', Transform.as_view()),
   path('update_information/', UpdateInformation.as_view()),
   path('upload_image/',UploadImage.as_view()),
   path('reset_password/', ResetPassword.as_view()),
   path('logout/', Logout.as_view()),
   path('focus/', FocusUser.as_view()),
   path('make_friend/', MakeFriend.as_view()),
   path('response_friend/', ResponseFriend.as_view()),
   path('refuse_friend/', RefuseFriend.as_view()),
   path('read_message/', ReadMessage.as_view()),
   path('search_user/', UserSearchView()),

]