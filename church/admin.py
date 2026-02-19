from django.contrib import admin

# Register your models here.
from .models import Department, ExpenseCategory, Member, IncomeCategory, Expense, Income
admin.site.register(Member)
admin.site.register(Department)
admin.site.register(ExpenseCategory)
admin.site.register(IncomeCategory)
admin.site.register(Expense)
admin.site.register(Income)