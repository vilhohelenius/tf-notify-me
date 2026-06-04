import json
import urllib.request
import urllib.parse
from datetime import date, datetime
import os


def send_notification(title: str, message: str, recipient: str):
    payload = urllib.parse.urlencode({
        "token": os.environ["PUSHOVER_APP_TOKEN"],
        "user": recipient,
        "title": title,
        "message": message,
        "priority": 1,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.pushover.net/1/messages.json",
        data=payload,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        print(f"  Lähetetty (HTTP {resp.status})")


def send_to_all(title: str, message: str):
    recipients = {
        "user": os.environ["PUSHOVER_USER_KEY"],
        "group": os.environ["PUSHOVER_GROUP_KEY"],
    }
    for name, key in recipients.items():
        print(f"  → {name}")
        send_notification(title, message, key)


def format_broadcast(comp: dict) -> str:
    channel = comp.get("channel")
    time = comp.get("broadcast_start_time")
    if channel and time:
        return f"📺 {channel} klo {time}"
    elif channel:
        return f"📺 {channel} (lähetysaika ei tiedossa)"
    else:
        return "📺 Ei TV-lähetystietoa"


def build_message(comp: dict, days_until: int) -> tuple[str, str]:
    name = comp["name"]
    broadcast = format_broadcast(comp)

    if days_until == 0:
        body = f"🔥 {name} — TÄNÄÄN!\n{broadcast}"
    elif days_until == 1:
        body = f"📅 {name} — HUOMENNA!\n{broadcast}"
    else:
        body = f"📅 {name} — {days_until} pv päästä\n{broadcast}"

    return "📅🏃 Yleisurheilua tulossa!", body


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

        title, body = build_message(comp, days_until)
        print(f"Lähetetään: {title} | {body}")
        send_to_all(title, body)
        notifications_sent += 1

    print(f"\nValmis. Lähetettiin {notifications_sent} notifikaatiota.")


if __name__ == "__main__":
    main()
