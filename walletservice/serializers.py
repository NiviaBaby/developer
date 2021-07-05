from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from walletservice.models import Wallete, Transactions
from datetime import datetime


class WalletSerializer(serializers.ModelSerializer):
    owner_by = serializers.SerializerMethodField("_owner_")
    status = serializers.SerializerMethodField("_status_")

    def _owner_ (self, obj):
        try:
            token = Token.objects.get(user=obj.owner)
            return token.key
        except: return ""
    
    def _status_(self, obj):
        if obj.is_enable:
            return "enabled"
        else:  return "desabled"
         
    class Meta:
        model = Wallete
        fields = ['id', 'owner_by', 'status', 
                'enabled_at', 'balance', 'disabled_at']
    
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(WalletSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def update(self, instance, validated_data):
        is_disabled = validated_data.get("is_disabled")
        if is_disabled == "true":
            instance.is_enable=False
            instance.disabled_at = datetime.now()
        else:
            instance.is_enable=True
            instance.enabled_at = datetime.now()
        instance.save()
        return instance


class DepositSerializer(serializers.ModelSerializer):
    deposited_by = serializers.SerializerMethodField("_deposited_by_")
    status = serializers.SerializerMethodField("_status_")
    deposited_at = serializers.SerializerMethodField("_deposited_at_")
    amount = serializers.CharField(required=True, max_length=255)
    reference_id = serializers.CharField(required=True, 
                max_length=100, validators=[
                UniqueValidator(
                queryset=Transactions.objects.filter(type="deposit"), 
                message="Reference id already exists")])

    def validate(self, attrs):
        amount = attrs.get('amount')
        if float(amount) <= 0:
            raise serializers.ValidationError(
                "Deposit an amount greater than zero")
        return attrs

    def _deposited_at_ (self, obj):
        try:
            return obj.datetime
        except: return ""

    def _deposited_by_ (self, obj):
        try:
            token = Token.objects.get(user=obj.user)
            return token.key
        except: return ""
    
    def _status_(self, obj):
        if obj.is_success:
            return "Success"
        else:  return "Fail"
         
    class Meta:
        model = Transactions
        fields = ['id', 'deposited_by', 'status', 
                'deposited_at', 'amount', 'reference_id']

    def create(self, validated_data):
        user =  self.context.get('user')
        wallet_obj = self.context.get('wallet_obj')
        amount = validated_data.get("amount")
        reference_id = validated_data.get("reference_id")
        transaction_obj = Transactions.objects.create(amount=amount,
                reference_id=reference_id, 
                type='deposit', user=user, wallet=wallet_obj, 
                datetime=datetime.now(), 
                is_success=True)
        wallet_obj.balance = float(wallet_obj.balance) + float(amount)
        wallet_obj.save()
        return transaction_obj


class WithdrawSerializer(serializers.ModelSerializer):
    withdraw_by = serializers.SerializerMethodField("_withdraw_by_")
    status = serializers.SerializerMethodField("_status_")
    withdraw_at = serializers.SerializerMethodField("_withdraw_at_")
    amount = serializers.CharField(required=True, max_length=255)
    reference_id = serializers.CharField(required=True, 
                max_length=100, validators=[
                UniqueValidator(
                queryset=Transactions.objects.filter(
                type="withdraw"), 
                message="Reference id already exists")])

    def validate(self, attrs):
        amount = attrs.get('amount')
        wallet_obj = self.context.get('wallet_obj')
        if float(wallet_obj.balance) < float(amount):
            raise serializers.ValidationError(
                "Insufficient balance. Your balance is {balance}".format(
                balance=wallet_obj.balance))
        return attrs

    def _withdraw_at_ (self, obj):
        try:
            return obj.datetime
        except: return ""

    def _withdraw_by_ (self, obj):
        try:
            token = Token.objects.get(user=obj.user)
            return token.key
        except: return ""
    
    def _status_(self, obj):
        if obj.is_success:
            return "Success"
        else:  return "Fail"
         
    class Meta:
        model = Transactions
        fields = ['id', 'withdraw_by', 'status', 
                'withdraw_at', 'amount', 'reference_id']

    def create(self, validated_data):
        user =  self.context.get('user')
        wallet_obj = self.context.get('wallet_obj')
        amount = validated_data.get("amount")
        reference_id = validated_data.get("reference_id")
        transaction_obj = Transactions.objects.create(amount=amount,
                reference_id=reference_id, 
                type='withdraw', user=user, wallet=wallet_obj, 
                datetime=datetime.now(), 
                is_success=True)
        wallet_obj.balance = float(wallet_obj.balance) - float(amount)
        wallet_obj.save()
        return transaction_obj