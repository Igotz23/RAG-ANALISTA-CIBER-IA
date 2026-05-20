# 🛡️ Sistema de Inteligencia RAG para Analistas de Ciberseguridad

Este proyecto es un asistente de IA especializado en ciberseguridad que utiliza arquitectura **RAG (Retrieval-Augmented Generation)**. Permite a los analistas subir manuales técnicos en PDF, indexarlos en una base de datos vectorial y realizar consultas complejas manteniendo el hilo y contexto de la conversación.

## 🚀 Características principales

* **Ingesta de Documentos Dinámica:** Carga de PDFs, fragmentación con `RecursiveCharacterTextSplitter` y vectorización en tiempo real.
* **Memoria Contextual:** Implementación de `create_history_aware_retriever` de LangChain para que la IA entienda referencias continuas (ej. "¿Y el segundo punto de ese informe?").
* **Base de Datos Vectorial:** Integración con **Pinecone** para almacenamiento y búsqueda semántica eficiente.
* **Modelo de Lenguaje Avanzado:** Respuestas técnicas, precisas y estructuradas potenciadas por `Llama 3.3` a través de **Groq**.
* **Interfaz Intuitiva:** Desarrollado con **Streamlit** para una experiencia de usuario fluida y profesional.

## 🛠️ Tecnologías utilizadas

* **Framework LLM:** LangChain
* **Llamadas al Modelo:** ChatGroq (Llama 3.3 70B)
* **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
* **Vector Store:** Pinecone
* **Frontend:** Streamlit
* **Contenerización:** Docker

## 📦 Instalación y Despliegue con Docker

Para ejecutar este proyecto de forma local utilizando Docker, sigue estos pasos:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
cd TU_REPOSITORIO



2. Configurar las Variables de Entorno
Antes de levantar el contenedor, necesitas configurar las credenciales para que LangChain pueda comunicarse con los servicios de LLM y la base de datos vectorial.

Crea un archivo llamado .env en la raíz del proyecto (puedes guiarte con el archivo .env.example) y añade tus API Keys:

Plaintext
GROQ_API_KEY=tu_api_key_de_groq
PINECONE_API_KEY=tu_api_key_de_pinecone
3. Construcción y Despliegue con Docker
El proyecto está completamente contenerizado para asegurar que se ejecute en cualquier entorno sin conflictos de dependencias ni configuraciones locales.

Paso A: Construir la imagen de Docker
Este comando compilará el entorno aislado e instalará las librerías necesarias de Python (Streamlit, LangChain, etc.):

Bash
docker build -t ia-analista .
Paso B: Levantar el contenedor en producción
Ejecuta el siguiente comando en tu terminal para arrancar la aplicación.

💡 Nota sobre el comando: El parámetro -v (volúmenes) mapea de forma persistente las carpetas de tu máquina real con el contenedor. Esto garantiza que todos los PDFs que subas se guarden de forma segura en tu disco duro y no se pierdan al reiniciar el contenedor.

Elige el comando según el sistema operativo o terminal que estés utilizando:

En Linux / macOS:

Bash
docker run -d -p 8501:8501 --env-file .env -v "$(pwd)/documentos:/app/documentos" -v "$(pwd)/procesados:/app/procesados" --name app-analista ia-analista
En Windows (PowerShell):

PowerShell
docker run -d -p 8501:8501 --env-file .env -v "${PWD}/documentos:/app/documentos" -v "${PWD}/procesados:/app/procesados" --name app-analista ia-analista
En Windows (CMD / Símbolo del Sistema):

DOS
docker run -d -p 8501:8501 --env-file .env -v "%cd%/documentos:/app/documentos" -v "%cd%/procesados:/app/procesados" --name app-analista ia-analista
4. Acceso al Sistema
Una vez levantado el contenedor, el servidor local de Streamlit estará escuchando. Abre tu navegador web favorito y accede a la interfaz de usuario a través de la siguiente dirección:

👉 http://localhost:8501

Ahí podrás cargar tus documentos PDF en la barra lateral, esperar a que el pipeline los vectorice en Pinecone y comenzar tu sesión de análisis en el chat con memoria contextual integrada.