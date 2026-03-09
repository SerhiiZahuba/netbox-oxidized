"""Dashboard widgets for the NetBox Oxidized plugin."""

import logging
from datetime import datetime, timezone

from django import forms
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from extras.dashboard.utils import register_widget
from extras.dashboard.widgets import DashboardWidget, WidgetConfigForm

logger = logging.getLogger(__name__)


@register_widget
class OxidizedBackupStatusWidget(DashboardWidget):
    """Dashboard widget showing backup freshness summary from Oxidized."""

    default_title = _("Oxidized Backup Status")
    description = _("Display backup freshness summary from Oxidized.")
    template_name = "netbox_oxidized/widgets/backup_status.html"
    width = 4
    height = 3

    class ConfigForm(WidgetConfigForm):
        cache_timeout = forms.IntegerField(
            min_value=60,
            max_value=3600,
            initial=300,
            required=False,
            label=_("Cache timeout (seconds)"),
            help_text=_("How long to cache Oxidized node data (60-3600 seconds)."),
        )
        stale_hours = forms.IntegerField(
            min_value=1,
            max_value=168,
            initial=24,
            required=False,
            label=_("Stale threshold (hours)"),
            help_text=_("Backups older than this are considered stale."),
        )
        critical_hours = forms.IntegerField(
            min_value=1,
            max_value=720,
            initial=168,
            required=False,
            label=_("Critical threshold (hours)"),
            help_text=_("Backups older than this are considered critical (default 7 days)."),
        )

    def render(self, request):
        stale_hours = self.config.get("stale_hours", 24)
        critical_hours = self.config.get("critical_hours", 168)
        cache_timeout = self.config.get("cache_timeout", 300)

        return render_to_string(
            self.template_name,
            {
                "stale_hours": stale_hours,
                "critical_hours": critical_hours,
                "cache_timeout": cache_timeout,
            },
        )


def get_backup_status_context(stale_hours=24, critical_hours=168):
    """Build backup status context from Oxidized API data."""
    from .client import get_client

    client = get_client()
    if not client:
        return {"error": "Oxidized not configured. Set oxidized_url in plugin settings."}

    nodes = client._get_all_nodes()

    if not nodes:
        return {"error": "Failed to retrieve nodes from Oxidized."}

    now = datetime.now(timezone.utc)
    recent = 0
    stale = 0
    critical = 0
    failed = 0
    never = 0

    for node in nodes:
        status = node.get("status", "")

        if status == "never":
            never += 1
            continue

        if status in ("no_connection", "timeout"):
            failed += 1
            continue

        # Parse last backup time
        last_end = node.get("last", {}).get("end") if isinstance(node.get("last"), dict) else None
        backup_time = last_end or node.get("time")

        if not backup_time:
            never += 1
            continue

        try:
            # Oxidized returns times like "2026-03-09 10:18:59 UTC"
            time_str = str(backup_time).replace(" UTC", "").replace("Z", "")
            dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            dt = dt.replace(tzinfo=timezone.utc)
            age_hours = (now - dt).total_seconds() / 3600

            if age_hours > critical_hours:
                critical += 1
            elif age_hours > stale_hours:
                stale += 1
            else:
                recent += 1
        except (ValueError, TypeError):
            never += 1

    statuses = [
        {
            "key": "recent",
            "label": f"< {stale_hours}h",
            "count": recent,
            "bg_class": "bg-success",
            "text_class": "text-white",
        },
        {
            "key": "stale",
            "label": f"> {stale_hours}h",
            "count": stale,
            "bg_class": "bg-warning",
            "text_class": "text-dark",
        },
        {
            "key": "critical",
            "label": f"> {critical_hours // 24}d",
            "count": critical,
            "bg_class": "bg-danger",
            "text_class": "text-white",
        },
        {
            "key": "failed",
            "label": "Failed",
            "count": failed,
            "bg_class": "bg-dark",
            "text_class": "text-white",
        },
    ]

    # Only include 'never' if there are any
    if never > 0:
        statuses.append(
            {
                "key": "never",
                "label": "Never",
                "count": never,
                "bg_class": "bg-secondary",
                "text_class": "text-white",
            }
        )

    config = client.config
    oxidized_url = config.get("oxidized_external_url") or config.get("oxidized_url", "")

    return {
        "statuses": statuses,
        "total": len(nodes),
        "oxidized_url": oxidized_url,
    }
