
class StatusExeption(Exception):
    """
    Exeption raise while proccesing order and check 
    Card state is 'Overdue' or 'Not Active'
    """
    message = 'Card is overdue or not active, can\'t, procces this order!'
    
    @classmethod
    @property
    def status_message(cls) -> str:
        return cls.message