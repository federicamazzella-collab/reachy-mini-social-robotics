from reachy_mini import ReachyMini
from reachy_mini.motion.recorded_move import RecordedMoves
import time
import pygame

# Pre-carica le librerie di movimenti
emotions = RecordedMoves("pollen-robotics/reachy-mini-emotions-library")
dances   = RecordedMoves("pollen-robotics/reachy-mini-dances-library")

# CON QUESTE DUE LINEE DI CODICE POTETE VISUALIZZARE TUTTE LE ANIMAZIONI DEL ROBOT
print(emotions.list_moves())
print(dances.list_moves())

print("Connessione a Reachy Mini in simulazione...")
pygame.mixer.init()

# DICHIARAZIONE DELLA FUNZIONE PER RIPRODURRE AUDIO
def play_sound(file_path: str):
    # Carica il file audio (inserisci il percorso corretto del tuo file)
    pygame.mixer.music.load(file_path)
    
    # Avvia la riproduzione
    pygame.mixer.music.play()

    print("Riproduzione in corso...")

    # Mantieni il programma in esecuzione finché l'audio non finisce
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    print("Riproduzione terminata.")

# QUI, SOTTO QUESTO COMMENTO, INSERITE LE VOSTRE FUNZIONI


with ReachyMini() as mini:
    # DA QUI IN POI SCRIVETE IL CODICE DEL PROGETTO

    # IL CODICE SOTTO QUESTO COMMENTO DEVE ESSERE SOSTITUITO CON IL CODICE DEL PROGETTO
    print("Connesso! Inizio la sequenza di test...")

    input("Premi INVIO per muovere le antenne")
    
    # Muove le antenne
    mini.goto_target(antennas=[0.5, -0.5], duration=0.5)
    time.sleep(0.5)
    mini.goto_target(antennas=[-0.5, 0.5], duration=0.5)
    time.sleep(0.5)
    
    # Riporta le antenne in posizione neutra
    mini.goto_target(antennas=[0.0, 0.0], duration=0.5)

    input("Premi INVIO per riprodurre un audio")
    
    # ESEMPIO DI COME RIPRODURRE UN AUDIO
    play_sound("sample_audio.mp3")

    input("Premi INVIO per riprodurre un'animazione")
    
    # ESEMPIO DI COME RIPRODURRE UN'ANIMAZIONE
    move = emotions.get("dance3")   # <-- sostituisci con il nome che vuoi tu
    mini.play_move(move)

    
    print("Test completato con successo!")


    # QUI TERMINA IL CODICE DEL PROGETTO
