from rest_framework.authtoken.models import Token
from walletservice.custommessages import CustomMessage
from django.contrib.auth.models import User
from walletservice.models import Wallete
from walletservice.serializers import (WalletSerializer, 
                DepositSerializer, WithdrawSerializer)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class InitWalletAPIView(APIView):
    """
    create a wallet for a user
    """
    permission_classes = ()
    msg_ob = CustomMessage()

    def post(self, request):

        data = {}
        user_id = request.data.get('id')
        try:
            user_obj = User.objects.get(id=user_id)
        except: 
            return_dict = {'status':"fail",
                'msg':self.msg_ob.user_notfound, 
                'data':data}
            return Response(return_dict, 
                status=status.HTTP_404_NOT_FOUND)
        try:
            Wallete.objects.create(owner=user_obj)
            token_obj = Token.objects.create(user=user_obj)
            data['token'] = token_obj.key
            return_dict = {'status':"success", 
                'msg':self.msg_ob.wallet_create, 
                'data':data}
            return Response(return_dict, 
                status=status.HTTP_201_CREATED)
        except: 
            return_dict = {'status':"fail",
                'msg':self.msg_ob.userhas_wallet, 
                'data':data}
            return Response(return_dict, 
                status=status.HTTP_400_BAD_REQUEST)


class WalletAPIView(APIView):
    """
    Enable user wallet
    """
    model = Wallete
    msg_ob = CustomMessage()

    def get_queryset(self):
        try:
            wallet_obj = Wallete.objects.get(
                owner=self.request.user, is_enable=False)
        except: wallet_obj = None
        return wallet_obj

    def post(self, request):
        
        data = {}
        wallet_obj = self.get_queryset()
        if not wallet_obj:
            return_dict = {'status':"fail",
                'msg':self.msg_ob.no_disablewallet, 
                'data':data}
            return Response(return_dict, 
                status=status.HTTP_404_NOT_FOUND)
        serializer = WalletSerializer(wallet_obj, 
                data=request.data, fields=('id', 'owner_by', 
                    'status', 'enabled_at', 'balance'))
        if serializer.is_valid():
            serializer.update(wallet_obj, request.data)    
            data["wallet"] = serializer.data
            return_dict = {'status':"success", 
                'msg':self.msg_ob.walletenabled, 
                'data':data} 
            return Response(return_dict, 
                status=status.HTTP_201_CREATED)
        else:
            return_dict = {'status':"fail",
                'msg':self.msg_ob.form_error, 
                'data':serializer.errors}
            return Response(return_dict, 
                status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        
        data = {}
        try:
            wallet_obj = Wallete.objects.get(
                owner=self.request.user, is_enable=True)
        except: 
            return_dict = {'status':"fail",
                'msg':self.msg_ob.no_enabledwallet, 
                'data':data}
            return Response(return_dict, 
                status=status.HTTP_404_NOT_FOUND)
        serializer = WalletSerializer(wallet_obj, 
                data=request.data)
        if serializer.is_valid():
            data["wallet"] = serializer.data
            return_dict = {'status':"success", 
                'msg':self.msg_ob.balance_retrieved, 
                'data':data} 
            return Response(return_dict, 
                status=status.HTTP_200_OK)
        else:
            return_dict = {'status':"fail",
                'msg':self.msg_ob.form_error, 
                'data':serializer.errors}
            return Response(return_dict, 
                status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        
        data = {}
        try:
            wallet_obj = Wallete.objects.get(
                owner=self.request.user, 
                is_enable=True)
        except:
            return_dict = {'status':"fail",
                'msg':self.msg_ob.no_disablewallet, 
                'data':data}
            return Response(return_dict, 
                status=status.HTTP_404_NOT_FOUND)
        serializer = WalletSerializer(wallet_obj, 
                data=request.data, fields=('id', 'owner_by', 
                'status', 'disabled_at', 'balance',))
        if serializer.is_valid():
            serializer.update(wallet_obj, request.data)    
            data["wallet"] = serializer.data
            return_dict = {'status':"success", 
                'msg':self.msg_ob.walletdisabled, 
                'data':data} 
            return Response(return_dict, 
                status=status.HTTP_201_CREATED)
        else:
            return_dict = {'status':"fail",
                'msg':self.msg_ob.form_error, 
                'data':serializer.errors}
            return Response(return_dict, 
                status=status.HTTP_400_BAD_REQUEST)

class DepositsAPIView(APIView):
    msg_ob = CustomMessage()

    def post(self, request):

        data = {}
        try:
            wallet_obj = Wallete.objects.get(
                owner=self.request.user, is_enable=True)
        except: 
            return_dict = {'status': "fail",
                'msg':self.msg_ob.no_enabledwallet, 
                'data': data}
            return Response(return_dict, 
                status=status.HTTP_404_NOT_FOUND)
        serializer = DepositSerializer(data=request.data, 
                context={"wallet_obj": wallet_obj, "user":request.user})
        if serializer.is_valid():
            tranobj = serializer.create(serializer.validated_data)    
            serializer = DepositSerializer(tranobj)
            data["deposit"] = serializer.data
            return_dict = {'status': "success", 
                'msg':self.msg_ob.deposit_success, 
                'data': data} 
            return Response(return_dict, 
                status=status.HTTP_201_CREATED)
        else:
            return_dict = {'status': "fail",
                'msg':self.msg_ob.form_error, 
                'data': serializer.errors}
            return Response(return_dict, 
                status=status.HTTP_400_BAD_REQUEST)


class WithdrawalAPIView(APIView):
    msg_ob = CustomMessage()

    def post(self, request):
        data = {}
        try:
            wallet_obj = Wallete.objects.get(
                owner=self.request.user, is_enable=True)
        except: 
            return_dict = {'status': "fail",
                'msg':self.msg_ob.no_enabledwallet, 
                'data': data}
            return Response(return_dict, 
                status=status.HTTP_404_NOT_FOUND)
        serializer = WithdrawSerializer(data=request.data, 
                context={"wallet_obj": wallet_obj, "user":request.user})
        if serializer.is_valid():
            tranobj = serializer.create(serializer.validated_data)    
            serializer = WithdrawSerializer(tranobj)
            data["withdrawal"] = serializer.data
            return_dict = {'status': "success", 
                'msg':self.msg_ob.deposit_success, 
                'data': data} 
            return Response(return_dict, 
                status=status.HTTP_201_CREATED)
        else:
            return_dict = {'status': "fail",
                'msg':self.msg_ob.form_error, 
                'data': serializer.errors}
            return Response(return_dict, 
                status=status.HTTP_400_BAD_REQUEST)

