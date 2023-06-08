import json

from celery import shared_task

from pieces_info.models import Message,LifeModel,ArticleModel,CommentModel

from user.models import FocusModel


@shared_task()
def send_message(data):
    try:
        u_id=data.get('u_id')
        type_2=data.get('type_2')
        p_id=data.get('p_id')
        if type_2=='LifeModel':
            u2_id=LifeModel.objects.get(id=p_id).user.id
            Message.objects.create(user_1_id=u_id,life_id=p_id,user_2_id=u2_id,type_1='3')
        elif type_2=='ArticleModel':
            u2_id=ArticleModel.objects.get(id=p_id).user.id
            Message.objects.create(user_1_id=u_id,article_id=p_id,user_2_id=u2_id,type_1='3')
        elif type_2=='CommentModel':
            u2_id = CommentModel.objects.get(id=p_id).user.id
            Message.objects.create(user_1_id=u_id, comment_id=p_id, user_2_id=u2_id,type_1='3')
        elif type_2=='focus':

            Message.objects.create(user_1_id=u_id, user_2_id=p_id,type_1='4')
    except:
        pass
