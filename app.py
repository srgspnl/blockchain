import streamlit as st
import json
from uuid import uuid4
from datetime import datetime
from blockchain_core import Blockchain # Importa a classe Blockchain

# --- Configuração Inicial e Estado da Sessão ---

# Inicializa o nó e a blockchain na sessão do Streamlit
# Isso garante que a blockchain persista durante as interações do usuário.
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()
    st.session_state.node_identifier = str(uuid4()).replace('-', '')

blockchain = st.session_state.blockchain
node_identifier = st.session_state.node_identifier

st.title("🔗 RegeNet - Blockchain Didática")
st.caption(f"ID do Nó: {node_identifier}")
st.write("Um projeto didático para entender os conceitos de Blocos, Transações e Mineração.")

# --- Menu Principal (Sidebar) ---

st.sidebar.title("🛠️ Ações da Blockchain")
menu_selection = st.sidebar.radio(
    "Selecione a Operação",
    ["Mineração (Proof of Work)", "Nova Transação", "Visualizar a Cadeia", "Consenso/Nós"]
)

# --- Funções do Frontend (Baseadas nos endpoints Flask originais) ---

# 1. Mineração
if menu_selection == "Mineração (Proof of Work)":
    st.header("⛏️ Minerar Novo Bloco")
    st.write("Execute o Proof of Work para validar as transações pendentes e receber uma recompensa.")

    if st.button("Iniciar Mineração"):
        # 1. Executa o PoW
        last_block = blockchain.last_block
        proof = blockchain.proof_of_work(last_block)

        # 2. Recebe a recompensa (transação de recompensa)
        blockchain.new_transaction(
            sender="Recompensa (0)",
            recipient=node_identifier[:8], # Mostrar apenas o início do ID
            amount=1,
        )

        # 3. Forja o novo Bloco
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)

        st.success("✅ **Novo Bloco Forjado!**")
        st.json({
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'][:30] + '...',
        })
        st.balloons()

# 2. Nova Transação
elif menu_selection == "Nova Transação":
    st.header("💸 Criar Nova Transação")
    st.write("Adicione uma transação que será incluída no próximo bloco minerado.")
    
    with st.form("new_transaction_form"):
        sender = st.text_input("Remetente", value="Endereço_A")
        recipient = st.text_input("Destinatário", value="Endereço_B")
        amount = st.number_input("Quantia (Tokens)", min_value=1, value=10)
        
        submitted = st.form_submit_button("Criar Transação")

        if submitted:
            # Cria a nova Transação
            index = blockchain.new_transaction(sender, recipient, amount)
            st.success(f"✅ Transação adicionada. Será incluída no Bloco **{index}**.")
            st.info(f"Transações Pendentes: {len(blockchain.current_transactions)}")

# 3. Visualizar a Cadeia
elif menu_selection == "Visualizar a Cadeia":
    st.header(f"⛓️ Cadeia Completa (Total de Blocos: {len(blockchain.chain)})")

    # Transações Pendentes
    st.subheader(f"📝 Transações Pendentes ({len(blockchain.current_transactions)})")
    if blockchain.current_transactions:
        st.json(blockchain.current_transactions)
    else:
        st.info("Nenhuma transação pendente. Hora de minerar!")

    st.markdown("---")
    st.subheader("Blocos Registrados")

    # Exibe os blocos
    for block in reversed(blockchain.chain):
        # Formatando o timestamp para legibilidade
        timestamp_dt = datetime.fromtimestamp(block['timestamp'])
        
        with st.expander(f"Bloco #{block['index']} - Minerado em {timestamp_dt.strftime('%H:%M:%S %d/%m/%Y')}", expanded=False):
            st.json(block)
            st.markdown(f"**Hash Anterior:** `{block['previous_hash'][:20]}...`")
            st.markdown(f"**Prova (PoW):** `{block['proof']}`")
            st.markdown(f"**Nº de Transações:** `{len(block['transactions'])}`")

# 4. Consenso/Nós
elif menu_selection == "Consenso/Nós":
    st.header("🌎 Configuração de Rede e Consenso")
    
    st.subheader("Adicionar Novo Nó")
    new_node_address = st.text_input(
        "Endereço do Nó (Ex: 192.168.0.5:5000)", 
        key="node_address"
    )
    if st.button("Registrar Nó"):
        try:
            blockchain.register_node(new_node_address)
            st.success(f"Nó '{new_node_address}' registrado com sucesso.")
        except ValueError as e:
            st.error(f"Erro ao registrar: {e}")

    st.subheader("Nós Registrados")
    if blockchain.nodes:
        st.code(list(blockchain.nodes))
    else:
        st.info("Nenhum nó vizinho registrado ainda.")

    st.subheader("Resolução de Conflitos (Consenso)")
    st.warning("⚠️ Nota: Em um ambiente Streamlit local de nó único, o consenso é apenas demonstrativo e retorna a cadeia local como autoritativa.")
    if st.button("Executar Resolução de Conflitos"):
        replaced = blockchain.resolve_conflicts()
        if replaced:
            st.success("A cadeia foi substituída pela mais longa da rede.")
            st.json({'Nova Cadeia': [b['index'] for b in blockchain.chain]})
        else:
            st.info("Nossa cadeia é autoritativa (não houve conflitos para resolver).")

# --- Como Rodar ---
# Para rodar o aplicativo, salve os dois arquivos (blockchain_core.py e streamlit_app.py)
# e execute no terminal:
# streamlit run streamlit_app.py