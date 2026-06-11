import sys, venv, subprocess, os, pathlib, itertools

def get_command_and_args():
    return sys.argv[1], sys.argv[2:]

def find_venv():
    curdir = pathlib.Path.cwd()
    for parent in itertools.chain([curdir], curdir.parents):
        venv_path = (parent / ".venv")
        if venv_path.is_dir():
            return venv_path
    raise FileNotFoundError("venv dir not found")

def find_or_create_venv():
    try:
        return find_venv()
    except FileNotFoundError:
        venv.create(".venv", symlinks=True, with_pip=True)
        return ".venv"

def get_venv_env(venv_path):
    venv_env = os.environ.copy()
    if sys.platform == "win32":
        executables_path = venv_path / "Scripts"
    else:
        executables_path = venv_path / "bin"
    venv_env["PATH"] = f"{executables_path}{os.pathsep}{venv_env['PATH']}"
    venv_env["VIRTUAL_ENV"] = str(venv_path)
    venv_env.pop("PYTHONHOME", None) # idk if this helps
    return venv_env

def run_command_in_venv(venv_path, args):
    return subprocess.run(args, env=get_venv_env(venv_path)).returncode

def run_python_in_venv(venv_path, args):
    return run_command_in_venv(venv_path, ["python", *args])

def run_pip_in_venv(venv_path, args):
    return_code = run_command_in_venv(venv_path, ["pip", *args])
    with open(venv_path.parent / "requirements.txt", "wb") as f:
        f.write(subprocess.check_output(["pip", "freeze"], env=get_venv_env(venv_path)))
    return return_code

def main():
    command, args = get_command_and_args()
    if command in ("pip",):
        venv_path = find_or_create_venv()
        sys.exit(run_pip_in_venv(venv_path, args))
    elif command in ("init",):
        find_or_create_venv()
    elif command in ("run",):
        venv_path = find_or_create_venv()
        sys.exit(run_command_in_venv(venv_path, args))
    elif command in ("python", "py"):
        venv_path = find_or_create_venv()
        sys.exit(run_python_in_venv(venv_path, args))
    else:
        raise ValueError(f"command \"{command}\" unknown")

main()
