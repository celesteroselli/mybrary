import django
django.setup()
import catalog.models as model
from datetime import *
from django.core.mail import send_mail
from django.conf import settings

def scheduled_job():
    loans = model.LoanInstance.objects.all()
    today = date.today()
    for LoanInstance in loans:
        if (today < LoanInstance.due_date):
            LoanInstance.overdue = True
            LoanInstance.save()
            msg = ('Hello, ' + str(LoanInstance.loaner) + '! \n \n You currently have ' + str(LoanInstance.book_loaned) + ' loaned out from ' + str(LoanInstance.user) + '. It is 3 weeks overdue. Please returns this book as soon as possible!')
            send_mail(
            subject='Mybrary Overdue Books',
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[str(LoanInstance.loaner_email)]
            )

if __name__ == "__main__":
    scheduled_job()