# pipka

is a tiny CLI tool to make Python project venv and "requirements.txt" management simpler without having to rely on Poetry or other big tools

the main point of "pipka" is it's just a proxy that runs commands in your venv, and its only side effects are slight env var modifications and the modification of "requirements.txt" after your every "pip" invocation

## usage

### command execution

venv will be created in the current directory's ".venv" child if it didn't exist (in there or in any of the parent directories), the command will be executed in the venv:

```
pipka your-command-here arg1 arg2 arg3 ...
```

### venv creation

to force venv creation, you can use:

```
pipka true
```

... or any other command that does nothing

### pip interactions

when you run anything with "pip", pipka automatically rewrites the "requirements.txt" near ".venv":

```
pipka pip your-args-here
```
