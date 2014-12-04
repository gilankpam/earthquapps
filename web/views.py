from flask import request, render_template, redirect, url_for, flash
from app import app
from models import Phone, Verification, check_verification_code
from utils import send_verification_code


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        phone_number = request.form['number']
        phone = Phone.query.filter_by(number=phone_number).first()
        if phone is None:
            phone = Phone.insert_phone(phone_number)
            verification = Verification.generate_ver_code(phone)
            send_verification_code(phone, verification)
            return redirect(url_for('verify', phone_number=phone_number), code=302)
        else:
            if not phone.active:
                if phone.unsub:
                    verification = Verification.generate_ver_code(phone)
                    send_verification_code(phone, verification)

                return redirect(url_for('verify', phone_number=phone_number), code=302)
            else:
                flash('Phone number already registered', 'danger')

    return render_template('index.html')


@app.route('/unsubscribe', methods=["GET", "POST"])
def unsubscribe():
    if request.method == 'POST':
        phone_number = request.form['number']
        phone = Phone.query.filter_by(number=phone_number).first()
        if phone is not None and phone.unsub is False:
            phone.unsubscribe()
            flash('Successfull unsubscribe', 'success')
            redirect(url_for('index'), code=302)
        else:
            flash('Phone number is not registered', 'danger')

    return render_template('unsubscribe.html')


@app.route('/verify/<phone_number>', methods=["GET", "POST"])
def verify(phone_number):
    resend = False
    phone = Phone.query.filter_by(number=phone_number).first_or_404()
    if request.method == 'POST':
        if check_verification_code(phone, request.form['code']):
            phone.activate()
            flash('Your number is now active', 'success')
            return redirect(url_for('index'), code=302)
        else:
            flash('Wrong code', 'danger')
            resend = True

    return render_template('verify.html', resend=resend, phone_number=phone_number)


@app.route('/verify/<phone_number>/resend', methods=['GET', 'POST'])
def resend_verification_code(phone_number):
    phone = Phone.query.filter_by(number=phone_number).first_or_404()
    code = Verification.generate_ver_code(phone)
    send_verification_code(phone, code)
    flash('Verification code sent', 'success')
    return redirect(url_for('verify', phone_number=phone_number), code=302)
