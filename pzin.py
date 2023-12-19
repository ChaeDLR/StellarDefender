import os
import subprocess

from subprocess import CalledProcessError
from traceback import print_stack

venvstr = "VIRTUAL_ENV"
pizmospath = "/Users/chaedelarosa/Code/repos/pizmos/dist/pizmos-0.1.0-py3-none-any.whl"

if __name__ == "__main__":
    if venvstr in os.environ:
        for j in [
            ["pip uninstall pizmos"],
            [f"pip install {pizmospath}"],
            ["pip list"],
        ]:
            try:
                _cp: subprocess.CompletedProcess = subprocess.run(
                    j, shell=True, input="Y", timeout=2, capture_output=True, text=True
                )
                print(f"Process complete\n{_cp.stdout}\n")
            except (CalledProcessError, ChildProcessError) as ex:
                print_stack()
                raise ex
