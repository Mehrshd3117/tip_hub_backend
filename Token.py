from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('39323830396D706764342B6B582F393372644837556376464C4D4962744E52516B364F5A78375A543742493D')
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