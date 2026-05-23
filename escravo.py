import socket
import json
import time

# Configurações para conectar ao Mestre
IP_MESTRE = '127.0.0.1' # Se for em outra máquina, coloque o IP do Mestre
PORTA_MESTRE = 5000

def processar_dados(lote):
    """Simula a carga de trabalho de processamento"""
    print(f"[ESCRAVO] Recebi lote com {len(lote)} registros. Iniciando cálculos...")
    
    anomalias = 0
    # Simula um processamento complexo que exige CPU (ex: 2 segundos)
    time.sleep(2) 
    
    # Regra de negócio fictícia: Auditoria buscando vacas com menos de 15 litros
    for registro in lote:
        if registro['litros'] < 15:
            anomalias += 1
            
    return {"anomalias": anomalias, "processados": len(lote)}

def iniciar_escravo():
    # Cria o socket TCP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 1. Conecta ao Mestre
        cliente.connect((IP_MESTRE, PORTA_MESTRE))
        print("[ESCRAVO] Conectado ao Mestre com sucesso.")

        # 2. Recebe a tarefa em pedaços até achar o fim
        dados_recebidos = ""
        while "<FIM>" not in dados_recebidos:
            pedaco = cliente.recv(4096).decode('utf-8')
            if not pedaco: # Proteção extra: Mestre fechou antes de mandar tudo
                break
            dados_recebidos += pedaco
            
        # Remove a marcação <FIM> antes de converter para JSON
        dados_recebidos = dados_recebidos.replace("<FIM>", "")
        lote_para_processar = json.loads(dados_recebidos)

        # 3. Executa o trabalho pesado
        resultado_final = processar_dados(lote_para_processar)

        # 4. Devolve apenas a consolidação
        cliente.sendall(json.dumps(resultado_final).encode('utf-8'))
        print(f"[ESCRAVO] Processamento concluído. Resultados enviados ao Mestre.\n")
        
    except ConnectionRefusedError:
        print("[ESCRAVO] O Mestre não está online.")
    except ConnectionResetError:
        # TRATAMENTO ADICIONADO AQUI
        print("[ESCRAVO] Fila esgotada! O Mestre encerrou a conexão antes de enviar os dados.")
    except json.decoder.JSONDecodeError:
        # TRATAMENTO CASO RECEBA VAZIO
        print("[ESCRAVO] Não recebi dados válidos. O lote provavelmente acabou.")
    finally:
        cliente.close()

if __name__ == "__main__":
    iniciar_escravo()