from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Expense(models.Model):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    ExpenseType = (
        (CREDIT, "CREDIT"),
        (DEBIT, "DEBIT")
    )

    amount = models.PositiveIntegerField(null=False)
    expense_type = models.CharField(choices=ExpenseType, default=DEBIT, max_length=6, null=False)
    descriptions = models.CharField(max_length=1024, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

