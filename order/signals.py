from django.dispatch import Signal


order_confirmed = Signal()
order_cancelled = Signal()
transaction_failed = Signal()

