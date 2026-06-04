import json
import urllib.request
import urllib.parse
from datetime import date, datetime
import os


def send_notification(title: str, message: str):
    app_token = os.environ["PUSHOVER_APP_TOKEN"]
    user_key = os.environ["PUSHOVER_USER_KEY"]

    payload = urllib.parse.urlencode({
        "token": app_token,
        "user": user_key,
        "title": title,
        "message": message,
        "priority": 1,  # high — ääni ja ilmoitus läpi hiljaisesta tilasta
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.pushover.net/1/messages.json",
        data=payload,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        print(f"  Notifikaatio lähetetty (HTTP {resp.status})")


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
        title = f"🔥 {name} — TÄNÄÄN!"
    elif days_until == 1:
        title = f"📅 {name} — HUOMENNA!"
    else:
        title = f"📅 {name} — {days_until} pv päästä"

    return title, broadcast


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
        send_notification(title, body)
        notifications_sent += 1

    print(f"\nValmis. Lähetettiin {notifications_sent} notifikaatiota.")


if __name__ == "__main__":
    main()
