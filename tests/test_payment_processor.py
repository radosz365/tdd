import unittest
from unittest.mock import Mock, MagicMock
from main import PaymentProcessor, PaymentGateway, TransactionResult, TransactionStatus, NetworkException, PaymentException, RefundException

# Tworzenie klasy testowej dla PaymentProcessor
class TestPaymentProcessor(unittest.TestCase):
    def setUp(self):
        self.gateway_mock = Mock(spec=PaymentGateway)
        self.processor = PaymentProcessor(self.gateway_mock)

    # Test dla udanego przetwarzania płatności
    def test_process_payment_success(self):
        self.gateway_mock.charge.return_value = TransactionResult(True, "txn123")
        result = self.processor.process_payment("user123", 100)
        self.assertTrue(result.success)
        self.assertEqual(result.transaction_id, "txn123")
        self.gateway_mock.charge.assert_called_once_with("user123", 100)

    # Test dla nieudanego przetwarzania płatności
    def test_process_payment_failure(self):
        self.gateway_mock.charge.side_effect = PaymentException("Niewystarczające środki")
        
        with self.assertRaises(PaymentException):
            self.processor.process_payment("user123", 100)
        
        self.gateway_mock.charge.assert_called_once_with("user123", 100)

