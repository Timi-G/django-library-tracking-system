from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings

from datetime import timezone
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
        logger.info(f'The book {book_title} was loaned, loan notification sent for loan id: {loan_id}')
    except Loan.DoesNotExist:
        logger.warning('Loan object does not exist')

@shared_task
def check_overdue_loans():
    try:
        loans=Loan.objects.all()
        for loan in loans:
            if loan.is_returned and timezone.now().date() > loan.due_date:
                send_loan_notification.delay(loan.id)
    except:
        pass