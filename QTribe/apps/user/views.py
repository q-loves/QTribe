import json

from django.contrib import auth
from django.contrib.admin import action
from django.db import transaction
from django.db.models import F, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from haystack.query import EmptySearchQuerySet
from haystack.views import SearchView

from user.models import UserModel,FocusModel,FriendModel

from pieces_info.models import ImageModel,Message

from QTribe.tasks import send_message


class Register(View):

    def get(self,request):
        return render(request,'user/register.html')
    def post(self,request):
        state={'code':-1}
        username=request.POST.get('username')
        password=request.POST.get('password')
        phone=request.POST.get('phone')
        user=UserModel.objects.create_user(username=username,password=password,phone=phone)
        if user:
            state={'code':200}
            auth.login(request,user)
        return redirect('/index/home_index/')
#校验用户名
class CheckUsername(View):
    def get(self,request,username):
        count=UserModel.objects.filter(username=username).count()
        return JsonResponse({'count':count})
#校验电话号码
class CheckPhone(View):
    def get(self,request,phone):
        count=UserModel.objects.filter(phone=phone).count()
        return JsonResponse({'count':count})

#校验邮箱地址
class CheckEmail(View):
    def get(self,request,email):
        count=UserModel.objects.filter(email=email).count()
        return JsonResponse({'count':count})

# 校验密码
class CheckPassword(View):
    def post(self, request):
        data=json.loads(request.body)
        username=data.get('username')
        phone=data.get('phone')
        password=data.get('password')
        #用户名登陆时需要username，绑定qq，微信时需要手机号
        if not (username or phone):
            return JsonResponse({'code':4001,'errormsg':'缺少必传参数'})
        if username:
            user=UserModel.objects.filter(username=username)
            if user.check_password(password):
                return JsonResponse({'code':200})
            return JsonResponse({'code': 4002, 'errormsg': '用户名或密码错误'})
        if phone:
            user=UserModel.objects.get(phone=phone)
            print('user-->',user)
            if user.check_password(password):
                return JsonResponse({'code':200})
            return JsonResponse({'code': 4002, 'errormsg': '手机号或密码错误'})

#校验密码
class ResetPassword(View):
    def get(self,request):
        password=request.GET.get('password')

        if request.user.check_password(password):
            return JsonResponse({'code':200})
        return JsonResponse({'code':401})
    def post(self,request):
        try:
            data=json.loads(request.body)
            password=data['password']
            request.user.set_password(password)
            return JsonResponse({'code':200})
        except:
            return JsonResponse({'code':401})



class Login(View):
    def get(self,request):
        return render(request,'user/login.html')
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)
        if user:
            auth.login(request,user)
            return redirect('/index/home_index/')
        #其实下面这个return是不必写的，因为在之前已经做了用户名和密码校验，密码不正确程序根本无法到达login这个函数里面。
        return redirect('/index/no_find/')

class Logout(View):
    def get(self,request):
        auth.logout(request)
        return redirect('/user/login/')

class Transform(View):
    def get(self,request):
        type=request.GET.get('type')
        if type=='register':
            return render(request, 'user/login.html')
        if type=='login':
            return render(request, 'user/register.html')
        return render(request,'404.html')

class UpdateInformation(View):
    def get(self,request):
        return render(request,'user/update_information.html',{'user':request.user})
    def post(self,request):

        try:
            data=json.loads(request.body)
            #利用新字典接收不为空的数据
            dict={}
            for key in data:
                if data.get(key):
                    dict[key]=data.get(key)
            user=UserModel.objects.filter(id=request.user.id).update(**dict)
            return JsonResponse({'code':200})
        except:
            return JsonResponse({'code':401})

#上传用户头像
class UploadImage(View):
    def post(self,request):
        try:
            with transaction.atomic():
                image=request.FILES.get('image')
                request.user.icon=image
                request.user.save()
                img=ImageModel.objects.create(image=image,user=request.user)
                return JsonResponse({'code':200})
        except:
            return JsonResponse({'code':401})

#用户关注
class FocusUser(View):
    def get(self,request):
        o_id=request.GET.get('o_id')
        u_id=request.user.id
        is_focus=int(request.GET.get('is_focus'))
        focus_obj=FocusModel.objects.filter(user_id=u_id,focus_user_id=o_id)
        if not is_focus:#如果已经关注，就是取消关注的请求
            focus_obj.update(flag='0')
            return JsonResponse({'code':200})
        if  is_focus:
            if focus_obj:
                focus_obj.update(flag='1')
                data={'type_2':'focus','u_id':u_id,'p_id':o_id}
                send_message.delay(data)
                return JsonResponse({'code': 200})
            FocusModel.objects.create(user_id=u_id,focus_user_id=o_id,flag='1')
            return JsonResponse({'code':200})
        return JsonResponse({'code':400})

#用户添加好友
class MakeFriend(View):
    def get(self,request):
        o_id=request.GET.get('o_id')
        u_id=request.user.id
        is_friend=int(request.GET.get('is_friend'))
        friend_obj_1=FriendModel.objects.filter(user_id=u_id,friend_user_id=o_id)
        friend_obj_2=FriendModel.objects.filter(user_id=o_id,friend_user_id=u_id)
        if not is_friend:#如果已经是好友，就是删除好友的请求
            if friend_obj_1:
                friend_obj_1.update(flag='0')
                return JsonResponse({'code':200})
            if friend_obj_2:
                friend_obj_2.update(flag='0')
                return JsonResponse({'code':200})
        if  is_friend:
                data={'type_2':'friend_1','u_id':u_id,'p_id':o_id}
                send_message.delay(data)
                return JsonResponse({'code': 200})
            # FriendModel.objects.create(user_id=u_id,friend_user_id=o_id,flag='1')
            # return JsonResponse({'code':200})
        return JsonResponse({'code':400})
#是否同意添加该好友
class ResponseFriend(View):
    def get(self,request):
        m_id = request.GET.get('m_id')
        u2_id = request.GET.get('u2_id')
        u1_id = request.GET.get('u1_id')
        friend_obj_1 = FriendModel.objects.filter(user_id=u2_id, friend_user_id=u1_id)
        friend_obj_2 = FriendModel.objects.filter(user_id=u1_id, friend_user_id=u2_id)
        data = {'type_2': 'friend_2', 'u_id': u2_id, 'p_id': u1_id}
        try:
            with transaction.atomic():
                Message.objects.filter(id=m_id).update(status=1)
                if friend_obj_1:
                    friend_obj_1.update(flag='1')
                    send_message.delay(data)
                    return JsonResponse({'code': 200})
                elif friend_obj_2:
                    friend_obj_2.update(flag='1')
                    send_message.delay(data)
                    return JsonResponse({'code': 200})
                else:
                    FriendModel.objects.create(user_id=u1_id, friend_user_id=u2_id, flag='1')
                    return JsonResponse({'code': 200})
        except:
            return JsonResponse({'code': 500})
class RefuseFriend(View):
    def get(self,request):
        try:
            m_id = request.GET.get('m_id')
            u2_id = request.GET.get('u2_id')
            u1_id = request.GET.get('u1_id')
            Message.objects.filter(id=m_id).update(status=1)
            data = {'type_2': 'friend_3', 'u_id': u2_id, 'p_id': u1_id}
            send_message.delay(data)
            return JsonResponse({'code':200})
        except:
            return JsonResponse({'code': 400})
class ReadMessage(View):
    def get(self,request):
        u2_id=request.user.id
        type_=request.GET.get('type_')
        # try:
        if type_=='pieces':
            msgs=Message.objects.filter(Q(type_1='1')|Q(type_1='2')|Q(type_1='4')|Q(type_1='8')).filter(user_2_id=u2_id,status=0).all()
            for msg in msgs:
                msg.status=1
            Message.objects.bulk_update(msgs,['status'])
        elif type_=='comments':
            msgs=Message.objects.filter(user_2_id=u2_id,status=0,type_1='3').all()
            for msg in msgs:
                msg.status=1
            Message.objects.bulk_update(msgs,['status'])
        elif type_=='friend':
            msgs=Message.objects.filter(Q(type_1='6')|Q(type_1='7')).filter(user_2_id=u2_id,status=0).all()
            for msg in msgs:
                msg.status=1
            Message.objects.bulk_update(msgs,['status'])
        return JsonResponse({'code': 200})
        # except:
        #     return JsonResponse({'code':400})




#搜索引擎
class UserSearchView(SearchView):

    template = 'search/user_search.html'
    results = EmptySearchQuerySet()
    results_per_page = 2
    def __init__(self):
        from haystack.query import SearchQuerySet
        sqs=SearchQuerySet().using('user')
        super(UserSearchView, self).__init__(searchqueryset=sqs)
    def get_query(self):
        queryset=super(UserSearchView, self).get_query()
        return queryset
    def get_results(self):
        result=[]
        for obj in self.form.search():
            if obj.model_name == 'usermodel':
                result.append(obj)
        return result
    def get_context(self):
        (paginator, page) = self.build_page()
        num_pages = paginator.num_pages
        page_number=int(self.request.GET.get('page',1))
        # 获取页码数列，用于前端遍历
        if paginator.num_pages > 5:
            if page_number - 2 <= 1:
                page_list = range(1, 6)
            elif page_number + 2 >= num_pages:
                page_list = range(num_pages - 4, num_pages + 1)
            else:
                page_list = range(page_number - 1, page_number + 4)

        else:
            page_list = paginator.page_range
        user_list=[]
        focus_ids=[]
        friend_ids=[]
        icon_ids = []
        for user in page:
            user_list.append(user.object)
            if user.object.icon:
                    icon_ids.append(user.object.id)
        focus_objs=self.request.user.focusmodel_set.all()
        for obj in focus_objs:
            if obj.flag=='1':
                focus_ids.append(obj.focus_user_id)
        friend_objs=self.request.user.friendmodel_set.all()
        for obj in friend_objs:
            if obj.flag=='1':
                friend_ids.append(obj.friend_user_id)
        context = {
            "query": self.query,
            "form": self.form,
            "page": page,
            "page_list":page_list,
            "user_list": user_list,
            'current_page': page.number,
            'num_pages': num_pages,
            "paginator": paginator,
            "q":self.get_query(),
            "suggestion": None,
            "focus_ids":focus_ids,
            "friend_ids":friend_ids,
            "icon_ids":icon_ids,
        }

        if (
            hasattr(self.results, "query")
            and self.results.query.backend.include_spelling
        ):
            context["suggestion"] = self.form.get_suggestion()
        return context

