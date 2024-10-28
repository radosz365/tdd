from enum import Enum

# Definicja statusów transakcji 
class TransactionStatus(Enum):
    OCZEKUJĄCA = "OCZEKUJĄCA"     
    ZAKOŃCZONA = "ZAKOŃCZONA" 
    NIEUDANA = "NIEUDANA"       

# Klasa przechowująca wynik transakcji
class TransactionResult:
    def __init__(self, success, transaction_id, message=""):
        self.success = success 
        self.transaction_id = transaction_id
        self.message = message

# Definicje wyjątków dla płatności
class NetworkException(Exception):
    pass
class PaymentException(Exception):
    pass
class RefundException(Exception):
    pass

# Interfejs (abstract base class) PaymentGateway
class PaymentGateway:

    # Metoda obciążająca konto użytkownika
    def charge(self, user_id, amount):
        raise NotImplementedError()
    
    # Metoda wykonująca zwrot dla danej transakcji
    def refund(self, transaction_id):
        raise NotImplementedError()
    
    # Metoda sprawdzająca status danej transakcji
    def get_status(self, transaction_id):
        raise NotImplementedError()

# Klasa PaymentProcessor obsługująca płatności
class PaymentProcessor:
    def __init__(self, gateway):
        self.gateway = gateway
        
    # Metoda przetwarzająca płatność dla użytkownika na określoną kwotę
    def process_payment(self, user_id, amount):
        if not user_id or amount <= 0:
            raise ValueError("Nieprawidłowy ID użytkownika lub kwota")
        try:
            # Próba obciążenia użytkownika za pomocą PaymentGateway
            result = self.gateway.charge(user_id, amount)
            self.log_transaction("Płatność przetworzona", result)
            return result
        except (NetworkException, PaymentException) as e:
            # Obsługa wyjątków związanych z problemami sieciowymi lub błędami płatności
            self.log_error("Płatność nieudana", e)
            raise e

    def refund_payment(self, transaction_id):
        # Metoda dokonująca zwrotu dla podanej transakcji
        if not transaction_id:
            raise ValueError("Nieprawidłowy ID transakcji")
        try:
            # Próba dokonania zwrotu za pomocą PaymentGateway
            result = self.gateway.refund(transaction_id)
            self.log_transaction("Zwrot przetworzony", result)
            return result
        except (NetworkException, RefundException) as e:
            # Obsługa wyjątków związanych z problemami sieciowymi lub błędami zwrotu
            self.log_error("Zwrot nieudany", e)
            raise e
        
    # Metoda pobierająca status płatności dla określonej transakcji
    def get_payment_status(self, transaction_id):
        if not transaction_id:
            raise ValueError("Nieprawidłowy ID transakcji")
        try:
            # Próba pobrania statusu transakcji za pomocą PaymentGateway
            return self.gateway.get_status(transaction_id)
        except NetworkException as e:
            # Obsługa wyjątku sieciowego
            self.log_error("Pobieranie statusu nieudane", e)
            raise e

    # Funkcja pomocnicza do logowania sukcesów transakcji
    def log_transaction(self, message, result):
        print(f"{message}: {result.transaction_id}, sukces: {result.success}")

    # Funkcja pomocnicza do logowania błędów transakcji
    def log_error(self, message, exception):
        print(f"{message}: {str(exception)}")
