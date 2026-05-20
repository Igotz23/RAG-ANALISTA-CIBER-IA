import streamlit as st
import os
import shutil
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import PyPDFLoader
# --- AQUÍ ESTABA EL FALLO (Líneas 9 y 10) ---
from langchain_text_splitters import RecursiveCharacterTextSplitter
# --- REEMPLAZA TUS LÍNEAS 11, 12 y 13 POR ESTAS ---
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# -----------------------------------------------
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
# 1. Configuración inicial y carga de variables
load_dotenv()
folder_input = "documentos"
folder_procesados = "procesados"

for folder in [folder_input, folder_procesados]:
    if not os.path.exists(folder):
        os.makedirs(folder)

st.set_page_config(page_title="IA Analista - Pro", layout="wide")
st.title("🛡️ Sistema de Inteligencia para Analistas")

# 2. Inicialización de Modelos
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
index_name = "manuales-analistas" # Asegúrate de que coincida con tu panel de Pinecone

vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)

# 3. Lógica de Memoria Contextual (Historial)
# Esto permite que la IA entienda referencias como "¿Y el segundo punto?"
contextualize_q_system_prompt = (
    "Dada una conversación previa y la pregunta más reciente del usuario, "
    "formula una pregunta independiente que pueda ser entendida sin el historial."
)
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Creamos el recuperador con memoria
history_aware_retriever = create_history_aware_retriever(
    llm, vectorstore.as_retriever(search_kwargs={"k": 5}), contextualize_q_prompt
)

# Prompt de respuesta profesional
system_prompt = (
    "Eres un asistente analista de ciberseguridad experto. "
    "Usa los fragmentos de contexto recuperados para responder. "
    "Si no lo sabes, di que no lo sabes. "
    "Sé técnico, preciso y estructurado."
    "\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Combinamos todo en la cadena final
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# 4. Estado de la Sesión (Chat History)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. BARRA LATERAL (Gestión de Documentos)
with st.sidebar:
    st.header("📥 Ingesta de Documentos")
    uploaded_file = st.file_uploader("Sube un manual PDF", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Procesar e Integrar"):
            with st.spinner("Leyendo y vectorizando..."):
                try:
                    # Guardar temporalmente
                    path_temp = os.path.join(folder_input, uploaded_file.name)
                    with open(path_temp, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Cargar y trocear
                    loader = PyPDFLoader(path_temp)
                    docs = loader.load()
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
                    chunks = text_splitter.split_documents(docs)
                    
                    # Subir a Pinecone
                    vectorstore.add_documents(chunks)
                    
                    # Mover a procesados
                    shutil.move(path_temp, os.path.join(folder_procesados, uploaded_file.name))
                    
                    st.success(f"✅ {uploaded_file.name} integrado correctamente.")
                except Exception as e:
                    st.error(f"Error: {e}")

# 6. INTERFAZ DE CHAT
# Mostrar mensajes anteriores
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(message.content)

# Entrada de usuario
if prompt := st.chat_input("¿Qué quieres analizar hoy?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generar respuesta con la cadena RAG y memoria
    with st.chat_message("assistant"):
        with st.spinner("Analizando manuales..."):
            response = rag_chain.invoke({
                "input": prompt,
                "chat_history": st.session_state.chat_history
            })
            answer = response["answer"]
            st.markdown(answer)
    
    # Actualizar historial
    st.session_state.chat_history.append(HumanMessage(content=prompt))
    st.session_state.chat_history.append(AIMessage(content=answer))