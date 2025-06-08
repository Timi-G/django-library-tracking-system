from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings

from django.utils import timezone
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
        today= timezone.now().date()
        overdue_loans= Loan.objects.filter(is_returned=False, due_date__lt=today)
        for loan in overdue_loans:
            member=loan.member.user
            send_mail(
                subject="Overdue Book Notification",
                message=f"Hello {member.username}\n\nYour loaned book '{loan.book.title}' is overdue since {loan.due_date}\nPlease return as soon as possible",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[member.email],
                fail_silently=False,
            )
            logger.info(f'Notification sent to {member.username} for overdue loan of book {loan.book.title}')
    except Loan.DoesNotExist:
        logger.warning('Loan object does not exist')
