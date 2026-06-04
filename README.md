# tf-notify-me

Sends push notifications to your phone before athletics competitions — Diamond League, Finnish GP series, major championships, and more.

## How it works

A GitHub Actions workflow runs every morning and checks whether any competition in `competitions.json` is happening today or tomorrow. If it finds a match, it sends a push notification via [ntfy](https://ntfy.sh).

## Setup

### 1. ntfy

1. Install the ntfy app on your phone ([Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy) / [iOS](https://apps.apple.com/app/ntfy/id1625396347))
2. Subscribe to the channel in the app: tap **+** and enter the channel name: **tf-ntfy-me**

## Notifications

The workflow runs daily at 07:00 UTC (09:00–10:00 Finnish time). Notifications look like this:

```
Yleisurheilua tulossa!
🔥 Diamond League — Rome — TODAY!
📺 MTV Urheilu at 22:00
```
