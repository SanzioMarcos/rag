import os
import json
import requests
from dotenv import load_dotenv

# Carrega variáveis definidas no arquivo .env.
load_dotenv()

# Obtém chave da API pelas variáveis.
API_KEY = os.getenv("API_KEY")

def send_llm_request_with_debug(prompt, checagem = True):        
    # Define endereço para enviar mensagens.
    url = "https://router.huggingface.co/v1/chat/completions"

    # Configura cabeçalhos exigidos pela requisição.
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # Monta dados enviados para o modelo.
    payload = {
        "model": "Qwen/Qwen3-8B",
        "messages": [
            {
                "role": "user",
                # "content": "Say only: Hello, World!"
                "content": (prompt)
            }
        ],
        "max_tokens": 1200,
        "extra_body": {
            "chat_template_kwargs": {
                "enable_thinking": False,
            }
        }
    }

    # Envia requisição HTTP para a API.
    response = requests.post(url, headers=headers, json=payload)

    # Verifica sucesso antes de processar resposta.
    if response.status_code == 200:
        # Converte resposta JSON para dicionário Python.
        data = response.json()

        # Extrai conteúdo retornado pelo modelo.
        content = data["choices"][0]["message"].get("content", "")

        # Remove espaços extras antes da impressão.
        print("RESPOSTA:")
        # print(content.strip())
        # Em vez de: print(content.strip())

        # Faça isso (Verifica se content existe antes de dar .strip()):
        if content:
            print(content.strip())
        else:
            print("Erro: O conteúdo retornado está vazio (None).")
        print("----------------------")
            
        if checagem:
            # Checagem.
            print("\n->Exibe resposta completa durante depuração opcional.")
            print("print(json.dumps(data, indent=2, ensure_ascii=False))")
            print(json.dumps(data, indent=2, ensure_ascii=False))

            print("\n->Raciocínio interno quando disponível.")        
            print('print(data["choices"][0]["message"].get("reasoning_content"))')
            print(data["choices"][0]["message"].get("reasoning_content"))

            print("\n->Motivo final da geração.")
            print('print(data["choices"][0]["finish_reason"])')
            print(data["choices"][0]["finish_reason"])

            print("\n->Estatísticas sobre tokens utilizados.")
            print('print(data["usage"])')
            print(data["usage"])

            print("\n->Conteúdo com caracteres especiais visíveis.")
            print('print(repr(content))')
            print(repr(content))

            print("\n->Armazenando motivo final para verificações.")
            print('finish_reason = data["choices"][0]["finish_reason"]')
            finish_reason = data["choices"][0]["finish_reason"]

            if finish_reason == "length":            
                print("\n ---> AVISO: resposta truncada por max_tokens.")

            print("\n->Inspencionando as chaves disponíveis:")
            print('message = data["choices"][0]["message"]')
            message = data["choices"][0]["message"]
            print('print(message.keys())')
            print(message.keys())

    else:
        # Exibe código retornado em caso erro.
        print("Erro:", response.status_code)

        # Exibe detalhes fornecidos pela API.
        print(response.text)

while True:
    print("\n ---> Para sair digite: sair\n")
    ask = input("Faça a sua pergunta: ")

    if ask == 'sair':
        print("Tchau.")
        break

    send_llm_request_with_debug(ask, checagem = False)