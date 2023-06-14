import json

from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.views import View

from pieces_info.models import CommentModel,LifeModel

from QTribe.tasks import send_message


class Comment_life(View):
    def post(self,request):
        try:
            user=request.user
            data_=json.loads(request.body)
            comment=data_['comment']
            l_id=int(data_['l_id'])
            with transaction.atomic():
                comm=CommentModel.objects.create(content=comment,life_id=l_id,user=user)
                LifeModel.objects.filter(id=l_id).update(comment_count=F('comment_count')+1)
            data={'u_id' : user.id, 'type_2': 'comment_life', 'p_id' : l_id,'c_id':comm.id}
            send_message.delay(data)

            return JsonResponse({'code':200})
        except:
            return JsonResponse({'code':500})