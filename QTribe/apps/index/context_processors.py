from django.db.models import Q
from pieces_info.models import Message

#判断登陆用户是否设置头像，若没有，则用默认头像代替
def set_icon_flag(request):
    content={}
    if request.user.is_authenticated:
        flag=0
        if request.user.icon:
            flag=1
        content['a']={'flag':flag}
    else:
        pass
    return content
#用于获取新消息
def get_message(request):
    content={}
    if request.user.is_authenticated:
        messages=Message.objects.filter(user_2_id=request.user.id,status=0).exclude(Q(type_1='3')|Q(type_1='5')|Q(type_1='6')|Q(type_1='7')).all()
        comments=Message.objects.filter(user_2_id=request.user.id,type_1='3',status=0).all()
        friends=Message.objects.filter(user_2_id=request.user.id,status=0).filter(Q(type_1='5')|Q(type_1='6')|Q(type_1='7')).all()
        m_count=messages.count()
        c_count=comments.count()
        f_count=friends.count()

        content={'messages':messages,'m_count':m_count,'comments':comments,'c_count':c_count,'friends':friends,'f_count':f_count}
    else:
        pass
    return content