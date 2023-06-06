

def set_flag(request):
    content={}
    if request.user.is_authenticated:
        flag=0
        if request.user.icon:
            flag=1
        content['a']={'flag':flag}
    else:
        pass
    return content