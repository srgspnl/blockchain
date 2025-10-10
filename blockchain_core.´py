import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

# Removidas as importações do Flask e requests
# A classe requests não será mais usada para 'resolve_conflicts'
# já que o Streamlit irá rodar em um ambiente local e único para a demonstração

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Cria o bloco gênesis
        self.new_block(previous_hash='1', proof=100)
        
    def register_node(self, address: str):
        """
        Adiciona um novo nó à lista de nós.

        :param address: Endereço do nó. Ex: 'http://192.168.0.5:5000'
        """
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Aceita uma URL sem esquema como '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')


    def valid_chain(self, chain: list) -> bool:
        """
        Determina se uma dada blockchain é válida.
        (A parte do 'print' foi removida para simplificar a saída)
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            
            # 1. Verifica se o hash do bloco anterior está correto
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # 2. Verifica se o Proof of Work está correto
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    # NOTA: O resolve_conflicts original depende de requisições HTTP (requests).
    # Para fins DIDÁTICOS com Streamlit em ambiente local, este método será
    # SIMPLIFICADO ou REQUERERÁ uma implementação mais complexa de rede
    # fora do escopo inicial. Manteremos a estrutura, mas SEM a lógica de rede
    # HTTP por enquanto.

    def resolve_conflicts(self):
        """
        Algoritmo de consenso: Em um ambiente didático local, este método
        apenas demonstra a INTENÇÃO de resolução, sem as chamadas HTTP reais.
        """
        # Em um ambiente Streamlit de nó único, essa função apenas retornará False
        # a menos que seja mockada ou ligada a um serviço de rede.
        return False # Sempre False para demo local de nó único

    def new_block(self, proof: int, previous_hash: str = None) -> dict:
        """
        Cria um novo Bloco na Blockchain
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Zera a lista de transações atuais
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        """
        Cria uma nova transação para ir para o próximo Bloco minerado
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        # Retorna o índice do bloco que irá segurar esta transação
        return self.last_block['index'] + 1

    @property
    def last_block(self) -> dict:
        return self.chain[-1]

    @staticmethod
    def hash(block: dict) -> str:
        """
        Cria um hash SHA-256 de um Bloco
        """
        # Garante que o Dicionário seja Ordenado para hashes consistentes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block: dict) -> int:
        """
        Algoritmo Simples de Proof of Work:
        - Encontra um número p' tal que hash(pp') contenha 4 zeros iniciais.
        """
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int, last_hash: str) -> bool:
        """
        Valida o Proof: verifica se o hash resultante tem 4 zeros iniciais.
        """
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
