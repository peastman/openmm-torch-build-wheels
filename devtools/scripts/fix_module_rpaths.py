from delocate import wheeltools
import os
import site
import subprocess

site_packages = site.getsitepackages()[0]
for filename in os.listdir('.'):
    if filename.endswith('.whl'):
        with wheeltools.InWheel(filename, filename):
            for libname in os.listdir('.'):
                if libname.startswith('_openmmtorch') and libname.endswith('.so'):
                    result = subprocess.run(['patchelf', '--print-rpath', libname], check=True, capture_output=True)
                    rpath = result.stdout.decode().strip().split(':')
                    rpath = [r.replace(site_packages, '$ORIGIN') for r in rpath]
                    subprocess.run(['patchelf', '--force-rpath', '--set-rpath', ':'.join(rpath), libname], check=True)
