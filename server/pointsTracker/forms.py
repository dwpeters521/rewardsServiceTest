from django.forms import CharField, DateTimeField, Form, IntegerField


class SpendForm(Form):
    points = IntegerField()


class TransactionForm(Form):
    payer = CharField(max_length=256)
    points = IntegerField()
    timestamp = DateTimeField()
