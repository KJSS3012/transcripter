import os
import json
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
import questionary
import pyperclip
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

load_dotenv()
client = Groq()
console = Console()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(SCRIPT_DIR, "assets", "audio")
TRANSCRIPTIONS_FILE = os.path.join(SCRIPT_DIR, "assets", "transcriptions.json")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(os.path.dirname(TRANSCRIPTIONS_FILE), exist_ok=True)

def get_audio_files():
    """Lista todos os arquivos de áudio na pasta assets/audio"""
    audio_extensions = ['.wav', '.mp3', '.m4a', '.flac', '.ogg']
    files = []
    
    for file in os.listdir(AUDIO_DIR):
        if any(file.lower().endswith(ext) for ext in audio_extensions):
            files.append(file)
    
    return files

def transcribe_audio(audio_file):
    """Transcreve um arquivo de áudio usando Groq"""
    audio_path = os.path.join(AUDIO_DIR, audio_file)
    
    with console.status(f"[bold green]Transcrevendo: {audio_file}..."):
        try:
            with open(audio_path, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=(audio_file, file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="text"
                )
            
            return transcription
        
        except Exception as e:
            console.print(f"[bold red]Erro na transcrição: {e}[/bold red]")
            return None

def save_transcription(audio_file, text):
    """Salva a transcrição em arquivo JSON"""
    transcription_data = {
        "archive": audio_file,
        "text": text,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if os.path.exists(TRANSCRIPTIONS_FILE):
        with open(TRANSCRIPTIONS_FILE, 'r', encoding='utf-8') as f:
            transcriptions = json.load(f)
    else:
        transcriptions = []
    
    transcriptions.append(transcription_data)
    
    with open(TRANSCRIPTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(transcriptions, f, indent=2, ensure_ascii=False)
    
    console.print(f"[bold green]✅ Transcrição salva em {TRANSCRIPTIONS_FILE}[/bold green]")

def show_transcriptions():
    """Exibe todas as transcrições salvas"""
    console.clear()
    
    if not os.path.exists(TRANSCRIPTIONS_FILE):
        console.print("[yellow]📝 Nenhuma transcrição encontrada.[/yellow]")
        return
    
    with open(TRANSCRIPTIONS_FILE, 'r', encoding='utf-8') as f:
        transcriptions = json.load(f)
    
    if not transcriptions:
        console.print("[yellow]📝 Nenhuma transcrição encontrada.[/yellow]")
        return
    
    table = Table(title="📋 Transcrições Salvas")
    table.add_column("Nº", style="bold yellow", width=4)
    table.add_column("Arquivo", style="cyan", width=20)
    table.add_column("Data", style="magenta", width=20)
    table.add_column("Prévia do Texto", style="green")
    
    for i, trans in enumerate(transcriptions, 1):
        preview = trans['text'][:80] + "..." if len(trans['text']) > 80 else trans['text']
        table.add_row(
            str(i),
            trans['archive'],
            trans['data'],
            preview
        )
    
    console.print(table)
    
    if transcriptions:
        choice = questionary.text("Digite o número para ver a transcrição completa (ou ENTER para voltar):").ask()
        if choice and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(transcriptions):
                trans = transcriptions[idx]
                console.clear()
                panel = Panel(
                    trans['texto'],
                    title=f"📄 {trans['arquivo']} - {trans['data']}",
                    border_style="blue"
                )
                console.print(panel)
                questionary.press_any_key_to_continue("Pressione qualquer tecla para continuar...").ask()

def main():
    console.clear()
    console.print(Panel.fit("🎤 TRANSCRIPTOR SIMPLES", style="bold blue"))
    
    while True:
        console.print()
        choice = questionary.select(
            "O que deseja fazer?",
            choices=[
                "📂 Listar arquivos de áudio",
                "🎵 Transcrever arquivo", 
                "📋 Ver transcrições salvas",
                "🚪 Sair"
            ]
        ).ask()
        
        if choice.startswith("📂"):
            console.clear()
            files = get_audio_files()
            if files:
                table = Table(title=f"🎵 Arquivos encontrados em {AUDIO_DIR}")
                table.add_column("Nº", style="bold yellow", width=4)
                table.add_column("Arquivo", style="cyan")
                
                for i, file in enumerate(files, 1):
                    table.add_row(str(i), file)
                
                console.print(table)
            else:
                console.print(f"[yellow]📂 Nenhum arquivo encontrado em {AUDIO_DIR}[/yellow]")
                console.print("[dim]Coloque seus arquivos de áudio (.wav, .mp3, .m4a, .flac, .ogg) nesta pasta.[/dim]")
            
            questionary.press_any_key_to_continue("Pressione qualquer tecla para continuar...").ask()
        
        elif choice.startswith("🎵"):
            console.clear()
            files = get_audio_files()
            if not files:
                console.print(f"[yellow]📂 Nenhum arquivo encontrado em {AUDIO_DIR}[/yellow]")
                questionary.press_any_key_to_continue("Pressione qualquer tecla para continuar...").ask()
                continue
            
            file_choices = [f"🎵 {file}" for file in files]
            file_choices.append("⬅️ Voltar")
            
            selected = questionary.select(
                "Escolha o arquivo para transcrever:",
                choices=file_choices
            ).ask()
            
            if selected and not selected.startswith("⬅️"):
                selected_file = selected.replace("🎵 ", "")
                
                text = transcribe_audio(selected_file)
                
                if text:
                    console.clear()
                    panel = Panel(
                        text,
                        title=f"📄 Transcrição de {selected_file}",
                        border_style="green"
                    )
                    console.print(panel)
                    
                    # Copia para o clipboard
                    try:
                        pyperclip.copy(text)
                        console.print("[dim green]📋 Texto copiado para o clipboard![/dim green]")
                    except Exception as clipboard_error:
                        console.print(f"[dim yellow]⚠️ Não foi possível copiar para o clipboard: {clipboard_error}[/dim yellow]")
                    
                    save_transcription(selected_file, text)
                    questionary.press_any_key_to_continue("Pressione qualquer tecla para continuar...").ask()
                else:
                    console.print("[bold red]❌ Falha na transcrição.[/bold red]")
                    questionary.press_any_key_to_continue("Pressione qualquer tecla para continuar...").ask()
        
        elif choice.startswith("📋"):
            show_transcriptions()
        
        elif choice.startswith("🚪"):
            console.print("[bold blue]👋 Até logo![/bold blue]")
            break

if __name__ == "__main__":
    main()