import subprocess
import time

NUM_ESCRAVOS = 5
processos = []

print(f"🚀 Iniciando {NUM_ESCRAVOS} escravos simultaneamente...")

# Dispara todos os escravos em paralelo
for i in range(NUM_ESCRAVOS):
    # Popen executa o script sem travar o código atual (assíncrono)
    p = subprocess.Popen(["python3", "-u", "escravo.py"])
    processos.append(p)

print("✅ Todos os escravos foram lançados! Verifique o terminal do Mestre.")

# Mantém este script rodando até que todos os escravos terminem
for p in processos:
    p.wait()

print("🏁 Todos os processos escravos foram encerrados.")