import requests
import csv
import os
from datetime import datetime
from zoneinfo import ZoneInfo


# -------------------------
# SETTINGS
# -------------------------

holdingAUDMoney = 100
ActiveStatus = "NOT ACTIVE"
oneMonth = 30
XRPCoin = 58

Status = "🟡 Collecting"

CSV_FILE = "data/price_history.csv"


# -------------------------
# SETUP CSV
# -------------------------

def setup_csv():

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(CSV_FILE):

        with open(CSV_FILE, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "timestamp",
                "xrp_usd",
                "usd_aud",
                "xrp_aud"
            ])


# -------------------------
# GET DAYS
# -------------------------

def get_days():

    with open(CSV_FILE, "r", newline="") as file:

        reader = csv.DictReader(file)

        first_row = next(reader, None)

    if first_row is None:
        return 0

    first_time = datetime.fromisoformat(
        first_row["timestamp"]
    )

    now = datetime.now(
        ZoneInfo("Australia/Melbourne")
    )

    difference = now - first_time

    days = difference.total_seconds() // 86400

    return int(days)


# -------------------------
# GET RECORD COUNT
# -------------------------

def get_record_count():

    with open(CSV_FILE, "r", newline="") as file:

        reader = csv.reader(file)

        next(reader, None)

        return sum(1 for row in reader)


# -------------------------
# GET USD → AUD
# -------------------------

def get_currency_rate():

    response = requests.get(
        "https://api.frankfurter.app/latest?from=USD&to=AUD",
        timeout=10
    )

    response.raise_for_status()

    return response.json()["rates"]["AUD"]


# -------------------------
# GET XRP DATA
# -------------------------

def GetXRPData():

    response = requests.get(
        f"https://api.coinlore.net/api/ticker/?id={XRPCoin}",
        timeout=10
    )

    response.raise_for_status()

    return response.json()[0]


# -------------------------
# SAVE PRICE
# -------------------------

def savePrice(data, usd_aud):

    xrp_usd = float(data["price_usd"])

    xrp_aud = round(
        xrp_usd * usd_aud,
        2
    )

    melbourne_time = datetime.now(
        ZoneInfo("Australia/Melbourne")
    ).isoformat()

    with open(CSV_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            melbourne_time,
            xrp_usd,
            usd_aud,
            xrp_aud
        ])

    return xrp_aud


# -------------------------
# PRINT OUTPUT
# -------------------------

def printOutPut(data, xrp_aud):

    days = get_days()

    records = get_record_count()

    if days >= oneMonth:

        status = "🟢 Ready"

    else:

        status = "🟡 Collecting"

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
    print(f"║ Strategy   : {ActiveStatus:<25} ║")

    print("╚══════════════════════════════════════╝")

    print()

    print(
        "Last check:",
        datetime.now(
            ZoneInfo("Australia/Melbourne")
        ).strftime("%d %b %Y, %I:%M:%S %p")
    )


# -------------------------
# MAIN
# -------------------------

def main():

    setup_csv()

    try:

        # Get USD → AUD rate
        usd_aud = get_currency_rate()

        # Get XRP data
        data = GetXRPData()

        # Save XRP price
        xrp_aud = savePrice(
            data,
            usd_aud
        )

        # Display dashboard
        printOutPut(
            data,
            xrp_aud
        )

    except requests.RequestException as error:

        print()
        print("🔴 API ERROR")
        print(error)

    except Exception as error:

        print()
        print("🔴 ERROR")
        print(error)


if __name__ == "__main__":
    main()