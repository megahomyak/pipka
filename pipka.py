import sys, venv, subprocess, os, pathlib, itertools

# Getting args to proxy later:
args = sys.argv[1:]

# Finding or creating venv:
curdir = pathlib.Path.cwd()
for dir_ in itertools.chain([curdir], curdir.parents):
    venv_path = (dir_ / ".venv")
    if venv_path.is_dir():
        break
else:
    venv.create(".venv", symlinks=True, with_pip=True)
    venv_path = curdir / ".venv"

# Creating env vars for in-venv executions:
venv_env = os.environ.copy()
if sys.platform == "win32":
    executables_path = venv_path / "Scripts"
else:
    executables_path = venv_path / "bin"
venv_env["PATH"] = f"{executables_path}{os.pathsep}{venv_env['PATH']}"
venv_env["VIRTUAL_ENV"] = str(venv_path)
venv_env.pop("PYTHONHOME", None) # idk if this helps

# Running whatever there was the need to run *in* the venv:
return_code = subprocess.run(args, env=venv_env).returncode

# If we were messing with pip, we need to freeze the outcome:
if args[0] == "pip":
    with open(venv_path.parent / "requirements.txt", "wb") as f:
        f.write(subprocess.check_output(["pip", "freeze"], env=venv_env))

# And finally, proxying the return code:
sys.exit(return_code)
