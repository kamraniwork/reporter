import random
import string


def generate_email_name_and_password(length):
    """
    generate random email_name and random password
    """
    letters: str = string.ascii_letters  # 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(letters) for i in range(length))


def get_rand_emails(no_of_emails, length):
    """
    generate random email that use generate_email_name
    """
    return [generate_email_name_and_password(length) + '@' + "gmail.com" for i in range(no_of_emails)]


