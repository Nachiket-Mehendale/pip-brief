import argparse
import os
import subprocess
import sys
from pip_brief.core import (
    run_pip_install, parse_pip_output, format_summary,
    run_pip_uninstall, parse_uninstall_output, format_uninstall_summary,
)


def main():
    parser = argparse.ArgumentParser(description="pip-brief: A clean summary for pip install/uninstall")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    install_parser = subparsers.add_parser('install', help='Install packages')
    install_parser.add_argument('packages', nargs='*', help='Package name(s)')
    install_parser.add_argument('-r', '--requirement', action='append', metavar='FILE',
                                help='Install from a requirements file')
    install_parser.add_argument('--verbose', action='store_true', help='Show full output')

    uninstall_parser = subparsers.add_parser('uninstall', help='Uninstall packages')
    uninstall_parser.add_argument('packages', nargs='+', help='Package name(s)')
    uninstall_parser.add_argument('--yes', '-y', action='store_true', help='Skip confirmation')
    uninstall_parser.add_argument('--verbose', action='store_true', help='Show full output')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'install':
        if not args.packages and not args.requirement:
            install_parser.error("provide package name(s) or -r <file>")

        # Each entry: (pip arguments, name shown in summary title)
        jobs = []
        for pkg in args.packages:
            jobs.append(([pkg], pkg))

        for req in (args.requirement or []):
            if not os.path.isfile(req):
                data = {"installed": [], "already_satisfied": [], "warnings": [],
                        "errors": [f"Requirements file not found: {req}"], "dependencies": []}
                jobs.append((None, req, data))
            else:
                jobs.append((["-r", req], req))

        for i, job in enumerate(jobs):
            if job[0] is None:
                print(format_summary(job[2], job[1]))
            else:
                raw_output = run_pip_install(job[0])
                if args.verbose:
                    print(raw_output)
                else:
                    print(format_summary(parse_pip_output(raw_output), job[1]))
            if i < len(jobs) - 1:
                print("\n" + "=" * 50 + "\n")

    elif args.command == 'uninstall':
        if args.yes:
            raw_output = run_pip_uninstall(args.packages, auto_confirm=True)
            if args.verbose:
                print(raw_output)
            else:
                parsed = parse_uninstall_output(raw_output)
                print(format_uninstall_summary(parsed, args.packages))
        else:
            subprocess.run(["pip", "uninstall"] + args.packages, text=True)


if __name__ == "__main__":
    main()