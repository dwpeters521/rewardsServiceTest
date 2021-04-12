from django.db import models
from pointsTracker.exceptions import (
    InvalidInputException,
    NotEnoughBalanceException,
)
from pointsTracker.forms import TransactionForm

from server.pointsTracker.forms import SpendForm


class Transaction(models.Model):
    payer = models.CharField(max_length=256)
    points = models.IntegerField()
    timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):
        """
        Override the default save method to adjust overall PayerBalance
        whenever a Transaction is created for a payer
        """
        # If this is an update to an existing Transaction, get the pre-update
        # points value
        previous_points = 0
        if self.pk:
            previous_points = Transaction.objects.get(id=self.pk).points

        # Save to Database
        super(Transaction, self).save(*args, **kwargs)

        # Find the amount the Transaction points are changing by
        changing_points = self.points - previous_points

        # Update or create a Payer object in the DB for this Transaction's
        # payer, post save
        payer_obj = PayerBalance.objects.filter(payer=self.payer).first()
        if payer_obj:
            payer_obj.points += changing_points
            payer_obj.save()
        else:
            PayerBalance.objects.create(
                payer=self.payer,
                points=self.points,
            )

    @classmethod
    def create(cls, request_data):
        transaction_form = TransactionForm(request_data)
        if not transaction_form.is_valid():
            raise InvalidInputException(transaction_form.errors)

        form_data = transaction_form.cleaned_data
        payer = form_data['payer']
        incoming_points = form_data['points']
        is_negative_transaction = incoming_points < 0
        if is_negative_transaction:
            _, error_message = (
                PayerBalance.objects.get_balance_info(
                    payer=payer,
                    incoming_points=abs(incoming_points)
                )
            )
            if error_message:
                raise NotEnoughBalanceException(error_message)
            else:
                cls.handle_processing(abs(incoming_points), payer=payer)
        else:
            cls.objects.create(**form_data)

    @classmethod
    def spend_points(cls, request_data):
        spend_form = SpendForm(request_data)
        if not spend_form.is_valid():
            raise InvalidInputException(spend_form.errors)

        points_to_spend = spend_form.cleaned_data['points']

        _, error_message = PayerBalance.objects.get_total_balance_info(
            points_to_spend
        )
        if error_message:
            raise NotEnoughBalanceException(error_message)
        else:
            return cls.handle_processing(points_to_spend)

    @staticmethod
    def serialize(payers_and_points):
        serialized_results = []
        for payer_obj, points in payers_and_points.items():
            serialized_results.append(
                {
                    'payer': payer_obj.payer,
                    'points': -points
                }
            )
        return serialized_results

    @classmethod
    def handle_processing(cls, points_to_process, payer=None):
        """
        Record all payers and their points spent as a result of this action,
        then mass update once all necessary transactions are iterated through
        :param points_to_process: Total points to deduct from a set of
        Transactions

        :param payer: Optional player to filter Transactions by
        :return: Dictionary of each Player object and the points being
        subtracted from each
        """
        query_kwargs = {
            'points__gt': 0,
        }
        if payer:
            query_kwargs.update({
                'payer': payer
            })

        payers_and_points = {}
        open_transactions = cls.objects.filter(**query_kwargs).order_by(
            'timestamp'
        )
        for transaction in open_transactions:
            payer_obj = PayerBalance.objects.get(payer=transaction.payer)
            if payer_obj not in payers_and_points:
                payers_and_points[payer_obj] = 0

            points_to_subtract = min(
                points_to_process, transaction.points, payer_obj.points
            )
            if not points_to_subtract:
                continue

            transaction.points = transaction.points - points_to_subtract
            transaction.save()

            payers_and_points[payer_obj] += points_to_subtract

            points_to_process -= points_to_subtract
            if points_to_process <= 0:
                break

        return payers_and_points


class CustomManager(models.Manager):
    def get_balance_info(self, payer, incoming_points):
        try:
            payer_balance = self.get(payer=payer).points
        except self.model.DoesNotExist:
            payer_balance = 0

        has_enough_balance = (payer_balance - incoming_points) >= 0
        if has_enough_balance:
            error_message = ''
        else:
            error_message = f'Cannot transact -{incoming_points} ' \
                            f'points. Only {payer_balance} are' \
                            f' available'

        return payer_balance, error_message

    def get_total_balance_info(self, incoming_points):
        total_balance = sum(
            self.all().values_list('points', flat=True)
        )
        if incoming_points > total_balance:
            error_message = f'Cannot spend {incoming_points} points. ' \
                            f'Only {total_balance} are available'
        else:
            error_message = ''

        return total_balance, error_message

    def get_balance_ordered_by_payer(self, payer=None):
        if payer:
            balance = self.filter(payer=payer)
        else:
            balance = self.all()

        return balance.order_by('payer')


class PayerBalance(models.Model):
    payer = models.CharField(max_length=256)
    points = models.IntegerField()

    objects = CustomManager()

    @staticmethod
    def serialize(balance):
        return {
            balance.payer: balance.points
            for balance in balance
        }
