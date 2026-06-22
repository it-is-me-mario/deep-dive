import time
from jupyter_client.manager import start_new_kernel
t=time.time()
print("starting kernel mario-course ...", flush=True)
km, kc = start_new_kernel(kernel_name="mario-course")
print("kernel up in", round(time.time()-t,1),"s", flush=True)
t=time.time()
kc.execute_interactive("import mario; print('MARIO OK', mario.__version__ if hasattr(mario,'__version__') else '')", timeout=120)
print("import mario done in", round(time.time()-t,1),"s", flush=True)
km.shutdown_kernel(now=True)
