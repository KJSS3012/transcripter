# 🎤 Transcriptor Simples

Um transcriptor de áudio para texto simples e eficiente usando a API Groq Whisper.

## 📋 Funcionalidades

- 📂 **Lista arquivos de áudio** da pasta `app/assets/audio`
- 🎵 **Transcreve arquivos** usando Groq Whisper (modelo `whisper-large-v3-turbo`)
- 💾 **Salva transcrições** em formato JSON
- 📋 **Visualiza histórico** de transcrições com interface bonita
- 🎨 **Interface rica** usando Rich e Questionary

## 🚀 Como usar

### 1. Configuração

1. Clone o repositório:
```bash
git clone https://github.com/KJSS3012/transcripter.git
cd transcripter
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure sua chave da API Groq:
    - Renomeie o arquivo `.env.example` para `.env` na raiz do projeto
    - Adicione sua chave da API: `GROQ_API_KEY=sua_chave_aqui`
    - **Obtenha sua chave gratuita em:** [console.groq.com](https://console.groq.com/keys)

> ⚠️ **Importante:** Mantenha sua chave da API segura e nunca a compartilhe publicamente.

### 2. Preparação dos arquivos

Coloque seus arquivos de áudio na pasta `app/assets/audio/`

**Formatos suportados:** `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`

### 3. Execução

```bash
cd app
python main.py
```

## 🎯 Interface

O programa oferece um menu interativo com as seguintes opções:

- **📂 Listar arquivos de áudio** - Mostra todos os arquivos disponíveis
- **🎵 Transcrever arquivo** - Seleciona e transcreve um arquivo
- **📋 Ver transcrições salvas** - Visualiza o histórico de transcrições
- **🚪 Sair** - Encerra o programa

## 📁 Estrutura do Projeto

```
transcripter/
├── app/
│   ├── main.py                 # Programa principal
│   └── assets/
│       ├── audio/              # Pasta para arquivos de áudio
│       └── transcriptions.json # Transcrições salvas
├── .env                        # Chave da API (não versionado)
├── README.md
└── exemplo.py                  # Código original complexo
```

## 📄 Formato das Transcrições

As transcrições são salvas em `app/assets/transcriptions.json`:

```json
[
  {
    "archive": "meu_audio.wav",
    "text": "Texto transcrito aqui...",
    "data": "2025-09-30 14:30:45"
  }
]
```

## 🔧 Dependências

- **groq** - Cliente da API Groq para transcrição
- **python-dotenv** - Carregamento de variáveis de ambiente
- **questionary** - Interface interativa de linha de comando
- **rich** - Interface rica com cores e formatação