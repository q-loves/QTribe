import json

from celery import shared_task

from pieces_info.models import Message,LifeModel,ArticleModel,CommentModel,VideoModel

from user.models import FocusModel


@shared_task()
def send_message(data):
    try:
        u_id=data.get('u_id')
        type_2=data.get('type_2')
        p_id=data.get('p_id')
        c_id=data.get('c_id')
        if type_2=='comment_life':
            u2_id=LifeModel.objects.get(id=p_id).user.id
            Message.objects.create(user_1_id=u_id,life_id=p_id,user_2_id=u2_id,type_1='3',comment_1_id=c_id)
        elif type_2=='comment_article':
            u2_id=ArticleModel.objects.get(id=p_id).user.id
            Message.objects.create(user_1_id=u_id,article_id=p_id,user_2_id=u2_id,type_1='3',comment_1_id=c_id)
        elif type_2=='CommentModel':
            u2_id = CommentModel.objects.get(id=p_id).user.id
            Message.objects.create(user_1_id=u_id, comment_2_id=p_id, user_2_id=u2_id,type_1='3',comment_1_id=c_id)
        elif type_2=='focus':
            Message.objects.create(user_1_id=u_id, user_2_id=p_id,type_1='4')
        elif type_2=='star_life':
            u2_id = LifeModel.objects.get(id=p_id).user.id
            Message.objects.create(user_1_id=u_id, user_2_id=u2_id,type_1='1',life_id=p_id)
        elif type_2=='collect_life':
            u2_id = LifeModel.objects.get(id=p_id).user.id
            Message.objects.create(user_1_id=u_id, user_2_id=u2_id,type_1='2',life_id=p_id)
        elif type_2=='star_article':
            u2_id = ArticleModel.objects.get(id=p_id).user.id
            Message.objects.create(user_1_id=u_id, user_2_id=u2_id,type_1='1',article_id=p_id)
        elif type_2=='collect_article':
            u2_id = ArticleModel.objects.get(id=p_id).user.id
            Message.objects.create(user_1_id=u_id, user_2_id=u2_id,type_1='2',article_id=p_id)
        elif type_2=='star_video':
            u2_id = VideoModel.objects.get(id=p_id).user.id
            Message.objects.create(user_1_id=u_id, user_2_id=u2_id,type_1='1',video_id=p_id)
        elif type_2=='collect_video':
            u2_id = VideoModel.objects.get(id=p_id).user.id
            Message.objects.create(user_1_id=u_id, user_2_id=u2_id,type_1='2',video_id=p_id)
        elif type_2=='friend_1':
            Message.objects.create(user_1_id=u_id, user_2_id=p_id, type_1='5')
        elif type_2=='friend_2':
            Message.objects.create(user_1_id=u_id, user_2_id=p_id, type_1='6')
        elif type_2=='friend_3':
            Message.objects.create(user_1_id=u_id, user_2_id=p_id, type_1='7')
    except:
        pass
