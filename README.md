# 🐄 BovinoCompute: Processamento Distribuído Mestre/Escravo

Este projeto é uma prova de conceito (PoC) prática do **Paradigma Mestre/Escravo** (Master/Slave) em programação paralela e sistemas distribuídos. 

Desenvolvido como projeto prático no âmbito do curso de Bacharelato em Ciência da Computação (IF Goiano), o sistema utiliza Sockets TCP nativos em Python para orquestrar a distribuição de processamento em lote. O caso de uso simulado é a auditoria massiva de relatórios de produção leiteira, onde o sistema identifica anomalias em milhares de registos de forma concorrente.

## 🏗️ Arquitetura do Sistema

O sistema é composto por três componentes principais, desenhados para operar tanto em ambientes Linux (Ubuntu) quanto Windows 11:

* **`mestre.py` (Orquestrador / Server):** Detém a base de dados central (simulada com 50.000 registos). Divide a carga em blocos (lotes de 10.000) e despacha-os assincronamente (via `threading`) para os nós trabalhadores que se ligarem.
* **`escravo.py` (Trabalhador / Client):** Conecta-se ao nó mestre, recebe o lote de dados, processa a carga computacional pesada (procurando vacas com produção inferior a 15 litros) e devolve apenas o resultado final consolidado.
* **`iniciar_cluster.py` (Lançador):** Um script multiplataforma que utiliza a biblioteca `subprocess` para arrancar múltiplos processos escravos em simultâneo, ilustrando a capacidade de escala horizontal.

## ✨ Características Técnicas Destacadas

* **Comunicação Assíncrona:** O Mestre não fica bloqueado à espera de um escravo terminar; ele continua a despachar novos lotes assim que novas conexões entram.
* **Gestão de Fluxo TCP (Stream):** Implementação de um delimitador customizado (`<FIM>`) para resolver a limitação de MTU/64KB em redes, garantindo que lotes de qualquer tamanho sejam recebidos na íntegra antes da conversão JSON.
* **Tolerância a Falhas Computacionais:** * O Mestre sobrevive e continua a operar mesmo que um Escravo se desconecte abruptamente.
    * Os Escravos gerem graciosamente eventos de `ConnectionResetError` (quando o Mestre encerra a porta antes do envio).
* **Reutilização de Portas (SO_REUSEADDR):** Configuração nativa para evitar bloqueios de porta (`Address already in use`) no sistema operativo ao reiniciar os testes sucessivamente.

## 🚀 Como Executar

O projeto não requer bibliotecas externas, utilizando apenas a *Standard Library* do Python. É compatível com as versões 3.x.

### 1. Iniciar o Nó Mestre
Abra um terminal na pasta do projeto e inicie o orquestrador. Ele ficará à escuta na porta 5000.
```bash
# Em Linux (Ubuntu) ou Windows 11
python3 -u mestre.py
# (No Windows, caso o comando não seja reconhecido, utilize apenas 'python -u mestre.py')
2. Iniciar os Trabalhadores (Escravos)
Pode iniciar os escravos de forma manual ou automática.

Opção A: Manualmente (um por um)
Abra novos terminais e execute:

Bash
python3 -u escravo.py
Opção B: Cluster Automatizado (Recomendado para Demonstração)
Abra apenas um segundo terminal e execute o lançador. Ele irá simular 5 ou mais máquinas conectando-se na mesma fração de segundo:

Bash
python3 -u iniciar_cluster.py
📊 Saída Esperada
O terminal do Mestre irá registar em tempo real as conexões, o despacho dos lotes e o sucesso no processamento (indicando quantas anomalias foram encontradas em cada partição). Quando todos os lotes forem processados, o servidor encerrará automaticamente o canal de escuta.


***

Este `README.md` oferece um nível de detalhe fantástico para qualquer professor ou colega que vá avaliar o código, documentando as soluções avançadas (como o uso do delimitador `<FIM>` para os 64kb e o `SO_REUSEADDR`) que implementámos durante a resolução dos erros de terminal! Pode utilizar exatamente assim.