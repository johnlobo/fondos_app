from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible  # only if you need to support Python 2
class Fund(models.Model):
    fund_name = models.CharField(max_length=200)
    fund_ISIN = models.CharField(max_length=30)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
       return self.fund_name
