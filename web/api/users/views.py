from django.shortcuts import render

def balanse_validate(user, credit) -> bool:
    """
    Проверка достаточно ли у пользователя денег на счету
    """
    if user.balance >= credit:
        return True
    return False