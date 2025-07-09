
from functions.sessions import get_sessions
from functions.risk_calc import calc_risk
from functions.pip_val_calc import calculate_pip_value
from functions.timezone_converter import convert_timezone
from functions.create_tool_func import create_tool_template
from datetime import datetime
import pytz


#FOREX SESSIONS FUNCTION
def forex_sessions(tool, request):
    current_utc = datetime.utcnow().strftime("%H:%M:%S")
    sessions = get_sessions()
    return{"title" :'FOREX SESSIONS', "time":current_utc, "sessions":sessions }


#PIP VALUE CALCULATOR FUNCTION
def pip_value_calc(tool, request):
    result = None
    if request.method == 'POST':
        pair = request.form['pair'].upper()
        lot_size = request.form['lot_size']
        price = request.form['price']
        result = calculate_pip_value(pair, lot_size, price)
    return {'result':result, 'title':'PIP VALUE CALC'}

#Timezones function

def timezone(tool,request):
    result = None
    if request.method == 'POST':
        input_time = request.form['input_time']
        from_tz = request.form['from_tz']
        to_tz = request.form['to_tz']
        result = convert_timezone(input_time, from_tz, to_tz)
    timezones = pytz.all_timezones
    return { 'result':result, 'timezones':timezones}


#Economic Calendar function
def economic_calendar(tool, request):
    return {'result': 'forex corelation page'}


#risc calculator function
def risk_calc(tool, request):
     result= None
     if request.method == 'POST':
        balance = float(request.form['balance'])
        stop_loss = float(request.form['stop_loss'])
        risk_percent = float(request.form['risk_percent'])
        result = calc_risk(balance, stop_loss, risk_percent)
        return { 'title': 'RISK CALCULATOR','result':result}
     else:
        return { 'title': 'RISK CALCULATOR'} 

#forex corelation function
def forex_corelation(tool, request):
    return {'result': 'forex corelation page'}