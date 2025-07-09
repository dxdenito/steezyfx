def calculate_pip_value(pair, lot_size, price, account_currency="USD"):
    #NORMALIZE INPUTS
    lot_size = float(lot_size)
    price = float(price)

    if "JPY" in pair:
        pip=0.01
    else:
        pip = 0.0001

    pip_value = (pip * lot_size *100000)/price
    return round(pip_value,2)