import os
import subprocess
import argparse
import time

# Definisci i filtri per tipo di file
TIPI_DI_FILE = {
    'immagine': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'video': ['.mp4', '.avi', '.mov', '.mkv', '.flv'],
    'documento': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx'],
    'audio': ['.mp3', '.wav', '.aac', '.flac'],
    'archivio': ['.zip', '.rar', '.tar', '.gz'],
    'server': ['.conf', '.log', '.sh', '.service', '.env']
}

# Associa i tipi di file a programmi specifici
PROGRAMMI_APERTURA = {
    'immagine': ['open -a Preview', 'open -a Photos', 'open -a Safari'],
    'video': ['open -a QuickTime Player', 'open -a VLC', 'open -a Safari'],
    'documento': ['open -a Preview', 'open -a Microsoft Word', 'open -a TextEdit'],
    'audio': ['open -a iTunes', 'open -a QuickTime Player', 'open -a Safari'],
    'archivio': ['open -a Archive Utility', 'open -a The Unarchiver', 'open -a Safari'],
    'server': ['open -a TextEdit', 'open -a Visual Studio Code', 'open -a Terminal']
}

# Elenco delle directory di sistema da escludere
SYSTEM_DIRS = ['/System', '/Library', '/bin', '/sbin', '/usr']

def is_system_path(path):
    """Controlla se il percorso fa parte delle directory di sistema."""
    return any(path.startswith(system_dir) for system_dir in SYSTEM_DIRS)

def apri_file(percorso_file, tipo_file):
    """Apre il file con uno dei programmi associati al tipo di file."""
    programmi = PROGRAMMI_APERTURA.get(tipo_file, [])
    for programma in programmi:
        try:
            subprocess.run(f"{programma} {percorso_file}", shell=True, check=True)
            break
        except subprocess.CalledProcessError:
            continue
    else:
        print(f"Non è stato possibile aprire il file {percorso_file} con i programmi disponibili.")

def filtra_per_data(percorso_file, filtro_data):
    """Filtra i file in base alla data di modifica."""
    ora_corrente = time.time()
    data_modifica = os.path.getmtime(percorso_file)

    if filtro_data == '24h':
        return ora_corrente - data_modifica <= 24 * 3600
    elif filtro_data == 'mese':
        return ora_corrente - data_modifica <= 30 * 24 * 3600
    elif filtro_data == 'anno':
        return ora_corrente - data_modifica <= 365 * 24 * 3600
    else:
        return True

def cerca_file(percorso, tipo_file=None, estensione=None, nome=None, ricorsivo=True, filtro_data=None):
    for radice, dir, file in os.walk(percorso):
        if not ricorsivo:
            del dir[:]
        
        # Escludi le directory di sistema
        dir[:] = [d for d in dir if not is_system_path(os.path.join(radice, d))]

        for file in file:
            percorso_file = os.path.join(radice, file)
            if is_system_path(percorso_file):
                continue

            if estensione and not file.endswith(estensione):
                continue
            
            if tipo_file and not any(file.endswith(ext) for ext in TIPI_DI_FILE.get(tipo_file, [])):
                continue
            
            if nome and nome not in file:
                continue
            
            if filtro_data and not filtra_per_data(percorso_file, filtro_data):
                continue
            
            print(percorso_file)
            apri_file(percorso_file, tipo_file)

def main():
    parser = argparse.ArgumentParser(description="Trova file nel sistema simile al comando find di Linux e aprili con programmi specifici.")
    parser.add_argument("percorso", help="Il percorso di directory dove iniziare la ricerca")
    parser.add_argument("-t", "--tipo-file", help="Filtra per tipo di file (es. immagine, video, documento, audio, archivio, server)")
    parser.add_argument("-e", "--estensione", help="Filtra i file per estensione")
    parser.add_argument("-n", "--nome", help="Filtra i file per nome")
    parser.add_argument("-r", "--no-ricorsivo", help="Cerca non ricorsivamente nelle directory", action="store_true", default=False)
    parser.add_argument("-f", "--filtro-data", help="Filtra i file per data di modifica (24h, mese, anno)")

    args = parser.parse_args()
    
    cerca_file(
        args.percorso, tipo_file=args.tipo_file, estensione=args.estensione, nome=args.nome, ricorsivo=not args.no_ricorsivo, filtro_data=args.filtro_data
    )

if __name__ == "__main__":
    main()
