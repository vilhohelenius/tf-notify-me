import json
import urllib.request
from datetime import date, datetime
import os


def send_notification(ntfy_channel: str, title: str, message: str):
    req = urllib.request.Request(
        f"https://ntfy.sh/{ntfy_channel}",
        data=message.encode("utf-8"),
        headers={
            "Title": title,
            "Tags": "runner,calendar",
        },
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
    ntfy_channel = os.environ["NTFY_CHANNEL"]
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
        send_notification(ntfy_channel, title, body)
        notifications_sent += 1

    print(f"\nValmis. Lähetettiin {notifications_sent} notifikaatiota.")


if __name__ == "__main__":
    main()