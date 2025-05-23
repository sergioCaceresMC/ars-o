import subprocess
import sys

# Ejecutar ordenes escritas
def ejecutar_str(st="", capture=False, chec=False, tex=False):
    l_str = st.split()
    out = subprocess.run(l_str, capture_output=capture, check=chec, text=tex)
    return out

# def ejecutar_popen(st="", tex=False):
#     l_str = st.split()
#     out = subprocess.Popen(l_str, text=tex, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, stderr = out.communicate()
#     return stdout, stderr

def ejecutar_popen(st="", tex=False):
    l_str = st.split()
    out = subprocess.Popen(l_str, text=tex, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = out.communicate()
    print(stdout)
    print(stderr, file=sys.stderr)
    return stdout, stderr