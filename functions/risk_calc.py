
def calc_risk(balance, stop_loss, risk_percent):
    
   try:
        risk_dollars = (risk_percent/100)* balance
        pip_value = risk_dollars /stop_loss
        lot_size = round(pip_value/10 , 2)

        return{
        'risk_dollars':round(risk_dollars, 2),
        'lot_size' : lot_size
        }
   except:
      return{
        'risk_dollars':0,
        'lot_size' : 0
        }
