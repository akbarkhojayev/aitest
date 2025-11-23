from django import template

register = template.Library()

@register.filter
def sum_questions(tests):
    """Barcha testlardagi savollar sonini hisoblash"""
    total = 0
    for test in tests:
        total += test.questions.count()
    return total

@register.filter
def sum_attempts(tests):
    """Barcha testlardagi urinishlar sonini hisoblash"""
    total = 0
    for test in tests:
        total += test.attempts.count()
    return total
