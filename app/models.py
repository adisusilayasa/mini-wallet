from mongoengine.queryset.manager import queryset_manager
from mongoengine import DecimalField, Document, StringField, DateTimeField, ListField, ReferenceField
from mongoengine.queryset.base import BaseQuerySet
from datetime import datetime

class Transaction(Document):
    id = StringField(primary_key=True)
    deposited_by = StringField()
    withdrawn_by = StringField()
    status = StringField(required=True)
    deposited_at = DateTimeField()
    withdrawn_at = DateTimeField()
    amount = DecimalField(required=True, precision=2)
    reference_id = StringField(required=True)

    def save(self, *args, **kwargs):
        if not self.deposited_at:
            self.deposited_at = datetime.utcnow()  # Set current time if not provided
        return super(Transaction, self).save(*args, **kwargs)

class Wallet(Document):
    customer_id = StringField(required=True, unique=True)
    status = StringField(required=True, default='enabled')
    created_at = DateTimeField(required=True)
    balance = DecimalField(required=True, precision=2, default=0)
    enabled_at = DateTimeField()  # New field for enabling time
    disabled_at = DateTimeField()  # New field for disabling time

    @classmethod
    def calculate_balance(cls):
        # Perform aggregation to calculate balance
        pipeline = [
            {'$group': {'_id': None, 'total_deposits': {'$sum': '$amount'}}}
        ]
        cursor = cls.objects.aggregate(*pipeline)

        # Check if the result is empty
        if isinstance(cursor, BaseQuerySet):
            result = list(cursor)
            total_deposits = result[0]['total_deposits'] if result else 0
        else:
            total_deposits = 0

        return total_deposits

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.utcnow()  # Set current time if not provided
        if not self.balance:
            self.balance = self.calculate_balance()
        return super(Wallet, self).save(*args, **kwargs)
