from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('784E75426D524657384E52514130557257775842463357506B44352B44786141506B595664317630576D633D')
        params = { 'sender' : '', 'receptor': phone_number, 'message' :f'{code}.وب سرویس پیام کوتاه کاوه نگار' }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


class IsUserAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin








