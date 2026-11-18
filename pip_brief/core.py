import re
import subprocess


class Colors:
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


def remove_duplicates(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def clean_name(text):
    """Strip version specifiers and extras: 'colorama>=0.3.4' -> 'colorama'"""
    return re.split(r"[<>=!~\[;]", text)[0]


# ---------------------------------------------------------------- install

def run_pip_install(packages):
    if isinstance(packages, str):
        packages = [packages]
    result = subprocess.run(
        ["pip", "install"] + packages,
        capture_output=True,
        text=True
    )
    return result.stdout + result.stderr


def parse_pip_output(output):
    skipped = []
    installed = []
    already_satisfied = []
    warnings = []
    errors = []
    dependencies = []
    

    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue

        if "Successfully installed" in line:
            match = re.search(r"Successfully installed (.+)", line)
            if match:
                for package in match.group(1).split():
                    if '-' in package:
                        name, version = package.rsplit('-', 1)
                        installed.append(f"{name} ({version})")
                    else:
                        installed.append(package)

        elif "Requirement already satisfied:" in line:
            match = re.search(r"Requirement already satisfied:\s+(\S+)", line)
            if match:
                name = clean_name(match.group(1))
                ver = re.search(r"\(([^()\s]+)\)\s*$", line)
                already_satisfied.append(f"{name} ({ver.group(1)})" if ver else name)

        elif "WARNING:" in line:
            warning = line.replace("WARNING:", "").strip()
            if "Ignoring invalid distribution" in warning:
                match = re.search(r"Ignoring invalid distribution (\S+)", warning)
                if match:
                    warnings.append(
                        f"Corrupted package installation detected ({match.group(1)}) "
                        f"- consider cleaning pip cache"
                    )
            else:
                warning = re.sub(r"\s+", " ", warning)
                if warning:
                    warnings.append(warning)

        elif "ERROR:" in line:
            error = re.sub(r"\s+", " ", line.replace("ERROR:", "").strip())
            if error:
                errors.append(error)

        elif line.startswith("Ignoring") and "markers" in line:
            match = re.match(r"Ignoring\s+([^:\s]+):", line)
            if match:
                skipped.append(f"{match.group(1)} (marker does not match this environment)")        

        elif line.startswith("Collecting"):
            match = re.search(r"Collecting\s+([^\s(]+)", line)
            if match:
                dependencies.append(clean_name(match.group(1)))

    errors = remove_duplicates(errors)
    # Keep only the key message when pip reports the same failure twice
    if any("Could not find a version" in e for e in errors):
        errors = [e for e in errors if "No matching distribution found" not in e]

    return {
        "installed": remove_duplicates(installed),
        "already_satisfied": remove_duplicates(already_satisfied),
        "warnings": remove_duplicates(warnings),
        "errors": errors,
        "dependencies": remove_duplicates(dependencies),
        "skipped": remove_duplicates(skipped),
    }


def format_summary(data, package_name):
    has_installed = len(data["installed"]) > 0
    has_satisfied = len(data["already_satisfied"]) > 0
    has_errors = len(data["errors"]) > 0

    if has_errors and not has_installed and not has_satisfied:
        title = f"Summary of {package_name} attempt:"
    else:
        title = f"Summary of {package_name} installation:"

    lines = [
        f"{Colors.BOLD}{Colors.CYAN}{title}{Colors.END}",
        "=" * len(title),
        "",
    ]

    sections = [
        ("Installed", data["installed"]),
        ("Already Satisfied", data["already_satisfied"]),
        ("Skipped", data.get("skipped", [])),
        ("Warnings", data["warnings"] if (has_installed or has_satisfied) else []),
        ("Errors", data["errors"]),
        ("Dependencies", data["dependencies"]),
    ]

    point = 1
    for label, values in sections:
        if values:
            lines.append(f"{point}) {label}:")
            lines.append(", ".join(values))
            lines.append("")
            lines.append("")
            point += 1

    while lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines)


# -------------------------------------------------------------- uninstall

def run_pip_uninstall(packages, auto_confirm=False):
    if isinstance(packages, str):
        packages = [packages]
    cmd = ["pip", "uninstall"] + packages
    if auto_confirm:
        cmd.append("-y")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout + result.stderr


def parse_uninstall_output(output):
    uninstalled = []
    errors = []

    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue

        if "Successfully uninstalled" in line:
            match = re.search(r"Successfully uninstalled (.+)", line)
            if match:
                uninstalled.extend(match.group(1).split(", "))

        elif "not installed" in line.lower():
            errors.append(line.replace("WARNING:", "").strip())

        elif "ERROR:" in line:
            errors.append(re.sub(r"\s+", " ", line.replace("ERROR:", "").strip()))

    return {
        "uninstalled": remove_duplicates(uninstalled),
        "errors": remove_duplicates(errors),
    }


def format_uninstall_summary(data, package_names):
    if isinstance(package_names, list) and len(package_names) > 1:
        title = f"Summary of {len(package_names)} packages uninstall:"
    else:
        name = package_names[0] if isinstance(package_names, list) else package_names
        title = f"Summary of {name} uninstall:"

    lines = [
        f"{Colors.BOLD}{Colors.CYAN}{title}{Colors.END}",
        "=" * len(title),
        "",
    ]

    point = 1
    if data["uninstalled"]:
        lines.append(f"{point}) Uninstalled:")
        lines.append(", ".join(data["uninstalled"]))
        lines.append("")
        lines.append("")
        point += 1

    if data["errors"]:
        lines.append(f"{point}) Errors:")
        lines.append(", ".join(data["errors"]))

    while lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines)