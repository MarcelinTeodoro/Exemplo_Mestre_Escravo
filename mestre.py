import socket
import json
import threading

# 1. Simulação da Base de Dados (ex: 50.000 registros de vacas)
# Cada registro tem um ID e os litros produzidos no dia
dados_totais = [{"id_vaca": i, "litros": 12 + (i % 10)} for i in range(1, 50001)]

TAMANHO_LOTE = 10000
# Divide a lista gigante em lotes menores (Grão Fino/Médio)
lotes = [dados_totais[i:i + TAMANHO_LOTE] for i in range(0, len(dados_totais), TAMANHO_LOTE)]

def lidar_com_escravo(conexao, endereco, id_lote):
    """Função que roda em paralelo para cada escravo conectado"""
    print(f"[MESTRE] Escravo {endereco} conectou. Despachando Lote {id_lote}...")
    try:
        # Codifica o lote em JSON e envia pela rede
        dados_json = json.dumps(lotes[id_lote]) + "<FIM>"
        conexao.sendall(dados_json.encode('utf-8'))
        

        # Aguarda a resposta (consolidação) do escravo
        resposta = conexao.recv(4096).decode('utf-8')
        resultado = json.loads(resposta)
        
        print(f"[MESTRE] Sucesso! Escravo {endereco} encontrou {resultado['anomalias']} anomalias no lote {id_lote}.")
    except Exception as e:
        print(f"[MESTRE] Erro na comunicação com {endereco}: {e}")
    finally:
        conexao.close()

def iniciar_mestre():
    # Criação do Socket TCP/IP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', 5000)) # Ouve em todas as interfaces na porta 5000
    servidor.listen(5)
    print(f"[MESTRE] Iniciado. Aguardando escravos na porta 5000 para {len(lotes)} lotes...\n")

    lote_atual = 0
    # Loop Assíncrono: Aceita conexões até acabar as tarefas
    while lote_atual < len(lotes):
        conexao, endereco = servidor.accept()
        
        # Cria uma Thread para não travar o Mestre (Interação Assíncrona)
        thread = threading.Thread(target=lidar_com_escravo, args=(conexao, endereco, lote_atual))
        thread.start()
        
        lote_atual += 1

    print("[MESTRE] Todos os lotes foram despachados!")

if __name__ == "__main__":
    iniciar_mestre()  