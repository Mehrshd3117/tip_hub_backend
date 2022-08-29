from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('5634733849745A4D6F76426C4555456F6B2F6D6A6D2F5474736E797472737868375941755262365A4B66453D')
        params = {
            'sender': '',
            'receptor': str(phone_number),
            'message': f"You're verify code is {code}"
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)