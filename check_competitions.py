import json
import urllib.request
from datetime import date, datetime
import os


def send_notification(message: str):
    channel = os.environ["NTFY_USER_CHANNEL"]
    full_message = f"{message}"
    req = urllib.request.Request(
        f"https://ntfy.sh/{channel}",
        data=full_message.encode("utf-8"),
        headers={
            "Title": "Yleisurheilua tulossa!",
            "Tags": "runner,calendar",
            "Priority": "urgent",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        print(f"  Lähetetty (HTTP {resp.status})")


def format_broadcast(comp: dict) -> str:
    tv_channel = comp.get("channel")
    time = comp.get("broadcast_start_time")
    if tv_channel and time:
        return f"📺 {tv_channel} klo {time}"
    elif tv_channel:
        return f"📺 {tv_channel} (lähetysaika ei tiedossa)"
    else:
        return "📺 Ei TV-lähetystietoa"



def build_message(comp: dict, days_until: int) -> str:
    name = comp["name"]
    broadcast = format_broadcast(comp)

    if days_until == 0:
        body = f"🔥 {name} — TÄNÄÄN!\n{broadcast}"
    elif days_until == 1:
        body = f"📅 {name} — HUOMENNA!\n{broadcast}"
    else:
        body = f"📅 {name} — {days_until} pv päästä\n{broadcast}"

    return body


def main():
    today = date.today()

    with open("competitions.json", encoding="utf-8") as f:
        competitions = json.load(f)

    notifications_sent = 0

    for comp in competitions:
        comp_date = datetime.strptime(comp["date"], "%Y-%m-%d").date()
        days_until = (comp_date - today).days

        if days_until < 0:
            continue

        if days_until not in comp["notify_days_before"]:
            print(f"Ei muistutusta tänään: {comp['name']} ({days_until} pv)")
            continue

        body = build_message(comp, days_until)
        print(f"Lähetetään: {body}")
        send_notification(body)
        notifications_sent += 1

    print(f"\nValmis. Lähetettiin {notifications_sent} notifikaatiota.")


if __name__ == "__main__":
    main()
