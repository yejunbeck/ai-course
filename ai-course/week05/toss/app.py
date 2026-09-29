import os
import base64
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# 4. 키 설정
SECRET_KEY = os.environ.get('TOSS_SECRET_KEY', 'test_gsk_docs_OaPz8L5KdmQXkzRz3y47BMw6')

def get_auth_header():
    """토스페이먼츠 API 인증을 위한 Authorization 헤더 생성"""
    # SecretKey: 뒤에 콜론을 붙이고 Base64로 인코딩
    auth_str = f"{SECRET_KEY}:"
    encoded_auth = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    return {"Authorization": f"Basic {encoded_auth}"}

@app.route('/')
def index():
    # 16. GET / : index.html
    return render_template('index.html')

@app.route('/success')
def success():
    # 17. GET /success
    payment_key = request.args.get('paymentKey')
    order_id = request.args.get('orderId')
    amount = request.args.get('amount')

    # 19. amount 검증 (1000원인지 확인)
    try:
        if int(amount) != 1000:
            return render_template('success.html', success=False, 
                                   error_code="INVALID_AMOUNT", 
                                   error_message=f"결제 금액이 일치하지 않습니다. (요청: {amount}, 기대: 1000)"), 400
    except (ValueError, TypeError):
        return render_template('success.html', success=False, 
                               error_code="INVALID_AMOUNT_FORMAT", 
                               error_message="금액 형식이 잘못되었습니다."), 400

    # 결제 승인 API 호출
    # Endpoint: POST https://api.tosspayments.com/v1/payments/{paymentKey}/confirm
    url = f"https://api.tosspayments.com/v1/payments/{payment_key}/confirm"
    payload = {
        "orderId": order_id,
        "amount": int(amount)
    }

    try:
        response = requests.post(url, json=payload, headers=get_auth_header())
        response_data = response.json()

        if response.status_code == 200:
            # 승인 성공
            return render_template('success.html', 
                                   success=True, 
                                   payment=response_data, 
                                   payment_json=response.text)
        else:
            # 승인 실패 (API 에러)
            return render_template('success.html', 
                                   success=False, 
                                   error_code=response_data.get('code', 'UNKNOWN_ERROR'), 
                                   error_message=response_data.get('message', '알 수 없는 에러가 발생했습니다.'))
    except Exception as e:
        return render_template('success.html', 
                               success=False, 
                               error_code="SERVER_ERROR", 
                               error_message=str(e)), 500

@app.route('/fail')
def fail():
    # 18. GET /fail
    code = request.args.get('code')
    message = request.args.get('message')
    return render_template('fail.html', code=code, message=message)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
