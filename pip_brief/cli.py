import argparse
import sys
import subprocess
from pip_brief.core import run_pip_install, parse_pip_output, format_summary
from pip_brief.core import run_pip_uninstall, parse_uninstall_output, format_uninstall_summary

def main():
    parser = argparse.ArgumentParser(description="pip-brief: A clean summary for pip install/uninstall")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    install_parser = subparsers.add_parser('install', help='Install packages')
    install_parser.add_argument('packages', nargs='+', help='Package name(s)')
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
        if args.verbose:
            raw_output = run_pip_install(args.packages)
            print(raw_output)
        else:
            for i, package in enumerate(args.packages):
                raw_output = run_pip_install([package])
                parsed = parse_pip_output(raw_output)
                summary = format_summary(parsed, package)
                print(summary)
                if i < len(args.packages) - 1:
                    print("\n" + "="*50 + "\n")
    
    elif args.command == 'uninstall':
        if args.yes:
            raw_output = run_pip_uninstall(args.packages, auto_confirm=True)
            parsed = parse_uninstall_output(raw_output)
            summary = format_uninstall_summary(parsed, args.packages)
            print(summary)
        else:
            subprocess.run(["pip", "uninstall"] + args.packages, text=True)


if __name__ == "__main__":
    main()