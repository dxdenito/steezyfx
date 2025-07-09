from datetime import datetime, time

def get_sessions():
    utc_now = datetime.utcnow().time()

    def in_range(start, end):
        if start < end:
            return start <= utc_now < end
        else:
            return utc_now>=start or utc_now < end
        
    sessions =[
        {
            "name":"Sydney", "open":time(22,0), "close":time(7,0), "pairs":["AUD/USD","NZD/USD"]
        },
        {
            "name":"Tokyo", "open":time(0,0), "close":time(9,0), "pairs":["USD/JPY","AUD/JPY"]
        },
        {
            "name":"London", "open":time(8,0), "close":time(17,0), "pairs":["EUR/USD","GBP/USD"]
        },
        {
            "name":"New York", "open":time(13,0), "close":time(22,0), "pairs":["USD/CAD","USD/CHF"]
        }
            
        ]
    
    for session in sessions:
        session["active"] = in_range(session["open"], session["close"])
    return sessions