from .models import Referrals
from users.models import Users
from tokens.models import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from users.views import balanse_validate


def refferal_validate(refferal_obj) -> bool:
    if refferal_obj.status == "0" or refferal_obj.status == "2":
        return False
    return True

def referral_activate(user_id, obj_refferal):
    user = Users.objects.get(id = user_id)

    obj_refferal.status = '2'
    user_boss = Users.objects.get(id = obj_refferal.user.id)

    user.bossid = user_boss.id
    if balanse_validate(user_boss, obj_refferal.balance):
        user_boss.balance = user_boss.balance - obj_refferal.balance
        user.balance = user.balance + obj_refferal.balance

    user_boss.save()
    user.save()
    obj_refferal.save()

    return status.HTTP_202_ACCEPTED


class ReferralActivate(APIView):
    def post(self, request, *args, **kwargs):
        
        user_id = request.data.get("user_id")
        referral_code = request.data.get("referral_code")

        try:
            obj_token = Token.objects.get(token = referral_code)
        except Token.DoesNotExist:
            raise Http404("Реферальный код не найден")

        try:
            obj_refferal = Referrals.objects.get(code = obj_token)
        except Referrals.DoesNotExist:
            raise Http404("Реферальный код не найден")

        if refferal_validate(obj_refferal):
            res = referral_activate(user_id, obj_refferal)

            return Response(res)
        
        return Response(status.HTTP_202_ACCEPTED)



