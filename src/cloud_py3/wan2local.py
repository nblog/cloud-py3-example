# /// script
# dependencies = [
#   
# ]
# requires-python = ">=3.9"
# ///
"""wan2local: orchestrate a local service + WAN tunnel."""

import argparse
import os


def _own_dist_name() -> str:
    """Resolve the distribution name that owns this package."""
    top = __package__.partition(".")[0] # type: ignore
    try:
        from importlib.metadata import packages_distributions
        return packages_distributions()[top][0]
    except ImportError:
        # Python < 3.11 fallback
        from importlib.metadata import distributions
        for d in distributions():
            if top in (d.read_text("top_level.txt") or "").split():
                return d.metadata["Name"]
    raise LookupError(f"no distribution found for {top!r}")


def discover_scripts() -> dict:
    """Discover all console_scripts registered by this package."""
    from importlib.metadata import distribution
    dist = distribution(_own_dist_name())
    return {
        ep.name: ep
        for ep in dist.entry_points
        if ep.group == "console_scripts" and ep.name != "wan2local"
    }


def load_and_run(name: str):
    """Load and execute a script's main() by entry point name."""
    scripts = discover_scripts()
    if name not in scripts:
        available = ", ".join(sorted(scripts.keys()))
        raise SystemExit(f"unknown script: {name}\navailable: {available}")
    scripts[name].load()()


def main():
    parser = argparse.ArgumentParser(
        description="local service + WAN tunnel orchestrator")
    parser.add_argument(
        "--local",
        default=os.getenv("TARGET_EXEC") or "frida-server",
        help="local service script name (default: frida-server)")
    parser.add_argument(
        "--wan",
        default=os.getenv("TARGET_WAN", "frpc"),
        help="WAN tunnel script name (default: frpc)")
    parser.add_argument(
        "--list", action="store_true",
        help="list available scripts")
    args = parser.parse_args()

    if args.list:
        scripts = discover_scripts()
        for name in sorted(scripts):
            print(f"  {name}")
        return

    print(f"[local] starting: {args.local}")
    load_and_run(args.local)

    print(f"[wan] starting: {args.wan}")
    load_and_run(args.wan)

    input()  # wait exit


if __name__ == "__main__":
    main()
