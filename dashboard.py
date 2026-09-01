from main import get_record_count,GetXRPData, get_days, GetStatus,get_currency_rate
from datetime import datetime
from zoneinfo import ZoneInfo

def Dashboard():
    data = GetXRPData()
    oneMonth = 30
    days = get_days()
    records = get_record_count()
    status = GetStatus()
    xrp_aud = get_currency_rate()
    print()

    print("╔══════════════════════════════════════╗")
    print("║            🪙 XRP BOT                ║")
    print("╠══════════════════════════════════════╣")

    print(f"║ Name       : {data['name']:<22} ║")
    print(f"║ XRP/AUD    : ${xrp_aud:<21.2f} ║")

    print("╠══════════════════════════════════════╣")

    print(f"║ History    : {days}/{oneMonth} days              ║")
    print(f"║ Records    : {records:<22} ║")

    print("╠══════════════════════════════════════╣")

    print(f"║ 1h Change  : {data['percent_change_1h']:<21}% ║")
    print(f"║ 24h Change : {data['percent_change_24h']:<21}% ║")
    print(f"║ 7d Change  : {data['percent_change_7d']:<21}% ║")

    print("╠══════════════════════════════════════╣")

    print(f"║ Status     : {status:<25} ║")
    

    print("╚══════════════════════════════════════╝")

    print()

    print(
        "Last check:",
        datetime.now(
            ZoneInfo("Australia/Melbourne")
        ).strftime("%d %b %Y, %I:%M:%S %p")
    )

def testing():
    print("hello world")
    Dashboard()




testing()