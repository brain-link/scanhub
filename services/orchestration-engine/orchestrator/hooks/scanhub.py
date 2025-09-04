# orchestrator/hooks/recon_hooks.py
from pathlib import Path

from dagster import HookContext, success_hook
from scanhub_libraries.resources import NOTIFIER_KEY


@success_hook(required_resource_keys={NOTIFIER_KEY})
def notify_dag_success(context: HookContext) -> None:
    """Check if data has been written and notify backend."""
    # Expect the asset to return an IDataContext
    result = next(iter(context.op_output_values.values()), None)
    if result is None:
        context.log.warning("NOTIFY-HOOK: No return value; skipping.")
        return
    dag_cfg = getattr(result, "dag_config", None)
    out_dir = getattr(dag_cfg, "output_directory", None)
    if not out_dir:
        context.log.warning("NOTIFY-HOOK: No output_directory; skipping.")
        return

    p = Path(out_dir)
    files = [str(f) for f in p.glob("**/*") if f.is_file()]
    if not files:
        context.log.warning(f"NOTIFY-HOOK: No files in {p}; skipping.")
        return

    notifier = getattr(context.resources, NOTIFIER_KEY)
    notifier.send_dag_success(success=True)
