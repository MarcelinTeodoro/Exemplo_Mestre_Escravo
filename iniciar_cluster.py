import subprocess
import time
import sys 

NUM_ESCRAVOS = 5
processos = []

print(f"🚀 Iniciando {NUM_ESCRAVOS} escravos simultaneamente...")

for i in range(NUM_ESCRAVOS):
    
    p = subprocess.Popen([sys.executable, "-u", "escravo.py"])
    processos.append(p)

print("✅ Todos os escravos foram lançados! Verifique o terminal do Mestre.")

for p in processos:
    p.wait()

print("🏁 Todos os processos escravos foram encerrados.")