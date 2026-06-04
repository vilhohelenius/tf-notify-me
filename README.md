# tf-notify-me

Sends push notifications to your phone before athletics competitions — Diamond League, Finnish GP series, major championships, and more.

## How it works

A GitHub Actions workflow runs every morning and checks whether any competition in `competitions.json` is happening today or tomorrow. If it finds a match, it sends a push notification via [Pushover](https://pushover.net).

## Setup

### 1. Pushover

1. Create an account at [pushover.net](https://pushover.net) and note your **User Key**
2. Create a new application at [pushover.net/apps/build](https://pushover.net/apps/build) to get an **API Token**
3. Install the Pushover app on your phone and sign in

### 2. GitHub secrets

Add two secrets to your repo under **Settings → Secrets and variables → Actions**:

| Secret | Value |
|---|---|
| `PUSHOVER_APP_TOKEN` | Your Pushover API token |
| `PUSHOVER_USER_KEY` | Your Pushover user key |

### 3. Test it

Go to **Actions → Daily competition check → Run workflow** to trigger a manual run and verify you receive a notification.

## Notifications

The workflow runs daily at 07:00 UTC (09:00–10:00 Finnish time). Notifications look like this:

```
🏃 Yleisurheilua tulossa!
🔥 Diamond League — Rome — TODAY!
📺 MTV Urheilu at 22:00
```

## Adding competitions

Edit `competitions.json`. Each entry has the following fields:

```json
{
    "name": "Diamond League - Rome",
    "date": "2026-06-04",
    "broadcast_start_time": "22:00",
    "channel": "MTV Urheilu",
    "notify_days_before": [1, 0]
}
```

- `notify_days_before: [1, 0]` — notify the day before and on the day itself
- `notify_days_before: [7, 1, 0]` — also notify a week in advance
- Set `broadcast_start_time` and `channel` to `null` if the broadcast details are not yet known
