#blocco 1 preparazione ambiente e importazione delle librerie 
from pathlib import Path 
import time
import pygame
from reachy_mini import ReachyMini
from reachy_mini.motion.recorded_move import RecordedMoves


PROJECT_DIR = Path(__file__).resolve().parent 
MUSIC_FILE = str(PROJECT_DIR / "il-cielo-gino copy.mp3") 
FEEDBACK_FILE = str(PROJECT_DIR / "sample_audio.mp3")

# blocco 2 Pre-carica le librerie di movimenti
emotions = RecordedMoves("pollen-robotics/reachy-mini-emotions-library")
dances   = RecordedMoves("pollen-robotics/reachy-mini-dances-library")

# CON QUESTE DUE LINEE DI CODICE POTETE VISUALIZZARE TUTTE LE ANIMAZIONI DEL ROBOT
print(emotions.list_moves())
print(dances.list_moves())


print("Connessione a Reachy Mini in simulazione...")
pygame.mixer.init()

# blocco 3 DICHIARAZIONE DELLA FUNZIONE PER RIPRODURRE AUDIO
def play_sound(file_path: str, duration: float = 2.0):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        print("Riproduzione in corso...")
        time.sleep(duration)
        pygame.mixer.music.stop() #ferma la muisca dopo i secondi stabiliti 

    except Exception as errore : 
         print("errore durante la riproduzione dell'audio:")
         print(errore)
         
    
# blocco 4 apriamo contesto robot
with ReachyMini() as mini:
     # DA QUI IN POI SCRIVETE IL CODICE DEL PROGETTO
    
    print("Connesso! Inizio l'interazione della storia")

    #blocco 5 funzioni di benvenuto e consenso 

    def saluto():
        print("Reachy: Buongiorno! Sono Reachy!")
        # Muove le antenne e saluta 
        mini.goto_target(antennas=[0.5, -0.5], duration=0.5)
        time.sleep(0.5)
        mini.goto_target(antennas=[-0.5, 0.5], duration=0.5)
        time.sleep(0.5)
   
         # Riporta le antenne in posizione neutra
        mini.goto_target(antennas=[0.0, 0.0], duration=0.5)

        print ("Reachy: Oggi ti racconto una breve storia e poi ti farò tre domande semplici per testare il tuo livello di attenzione.")
        print ("Reachy: E se vorrai potrai anche ascoltare una canzone e indovinare il titolo e/o l'autore")
        print ("Reachy: Ti va di iniziare con me ?")

    def conferma():
        risposta = input("Utente (si/no)").lower()

        if risposta == "si": 
            print("Reachy: Perfetto! Cominciamo insieme")
            #se l'utente dice di si allora facciamo un balletto (dance3)
            move = emotions.get("dance3")
            if move: mini.play_move(move)
            return True 
            
        elif risposta == "no": 
            print("Reachy: Va bene, nessun problema.")
            print("Reachy: Sarò qui ad aspettarti quando vorrai.")
            #AGGIUNTA EMOZIONE SAD
            move_sad = emotions.get("sad1")
            if move_sad: mini.play_move(move_sad)

            mini.goto_target(antennas=[-0.5, -0.5], duration=1.0)
            time.sleep(1.0)
            return False 
        
        else:
            print("Reachy: Non ho capito, ma va bene lo stesso.")
            return False 
        
        #blocco 6 storia + le 3 domande 
        
    def storia():
            print("\nReachy: Leggi con attenzione la storia che ti sto per raccontare.")
            print("\n--- LE NOSTRE ANIME DI NOTTE ---")
            print("Immagina una cittadina tranquilla dove vivono due anziani vicini, Louis e Addie.")
            print("Una sera, mentre il vento fischia forte contro i vetri, Addie bussa da Louis.")
            print("Porta con sé un semplice sacchetto di carta marrone con le sue cose per la notte.")
            print("Addie gli fa una proposta: 'La notte è difficile. Ti andrebbe di dormire da me per farci compagnia?'")
            print("Louis accetta sorridendo. Da quella sera, chiacchierano sotto una grande coperta di lana gialla,")
            print("tenendosi per mano e trovando finalmente una voce amica.")
            print("--- FINE STORIA ---\n")
            
            #la storia finisce qui e aspetta che l'utente abbia finito di leggere 
            input("Premi INVIO quando hai finito di leggere")
            print("Reachy: Bravo! Ora iniziamo con le domande.")

    # domanda 1 

    def domanda_uno(): 
        print("\nReachy: Prima domanda.")
        print("Reachy: Ti ricordi che rumore si sentiva fuori dalla finestra quando Addie ha bussato?")
        risposta = input("Utente: ").lower()

            #Il programma cerca la parola chiave nella risposta dell'utente
        if "vento" in risposta or "fischia" in risposta: 
            print("Reachy: Ottimo! Hai risposto benissimo!")

            # emozione di gioia/affetto dalla libreria
            move_correct = emotions.get("cheerful1") or emotions.get("loving1")
            if move_correct: mini.play_move(move_correct)
            mini.goto_target(antennas=[0.5, 0.5], duration=0.5) #le antenne su (felice) 
            play_sound(FEEDBACK_FILE, duration=2.0)   
            mini.goto_target(antennas=[0.0, 0.0], duration=0.5) #le antenne si fermano
            return True #risposta corretta
    

        else:
            print("Reachy: Non proprio, ma va bene!")
            print("Reachy: C'era il vento che fischiava contro i vetri.")

            # emozione di comprensione empatica per la RSA
            move_wrong = emotions.get("understanding1")
            if move_wrong: mini.play_move(move_wrong)

            mini.goto_target(antennas=[-0.5, -0.5], duration=1.0) #le antenne si abbassano
            time.sleep(1.5)
            mini.goto_target(antennas=[0.0, 0.0], duration=2.0) 
            return False #risposta sbagliata
    
    # domanda 2

    def domanda_due():
            print("\nReachy: Seconda domanda.")
            print("Reachy: In cosa aveva messo Addie le sue cose per la notte?")
            risposta = input("Utente: ").lower()

            #Il programma cerca la parola chiave nella risposta dell'utente
            if "sacchetto" in risposta or "carta" in risposta or "marrone" in risposta:
                print("Reachy: Ottimo! Hai risposta benissimo!")
                move_correct = emotions.get("proud1")
                if move_correct: mini.play_move(move_correct)

                mini.goto_target(antennas=[0.5, 0.5], duration=0.5)
                play_sound(FEEDBACK_FILE, duration=2.0)
                mini.goto_target(antennas=[0.0, 0.0], duration=0.5)

                return True 
            else:
                print("Reachy: Non proprio, ma va bene!")
                print("Reachy: Le aveva messe in un sacchetto di carta marrone.")

                move_wrong = emotions.get("calming1")
                if move_wrong: mini.play_move(move_wrong)
                mini.goto_target(antennas=[-0.5, -0.5], duration=0.5) #le antenne si abbassano
                time.sleep(1.5)
                mini.goto_target(antennas=[0.0, 0.0], duration=0.5) 
                return False

    # domanda 3

    def domanda_tre():
            print("\nReachy: Terza ed ultima domanda.")
            print("Reachy: Sotto che tipo di coperta stavano per non prendere freddo?")
            risposta = input("Utente: ").lower()

            #Il programma cerca la parola chiave nella risposta dell'utente
            if "lana" in risposta or "gialla" in risposta: 
                print("Reachy: Ottimo! Hai indovinato anche l'ultima domanda!")
                move_correct = emotions.get("grateful1")
                if move_correct: mini.play_move(move_correct)

                mini.goto_target(antennas=[0.5, 0.5], duration=0.5)
                play_sound(FEEDBACK_FILE, duration=2.0)
                mini.goto_target(antennas=[0.0, 0.0], duration=0.5)
                return True 
            else:
                print("Reachy: Non proprio, non preoccuparti!")
                print("Reachy: Era una grande coperta di lana gialla.")

                move_wrong = emotions.get("sad2")
                if move_wrong: mini.play_move(move_wrong)

                mini.goto_target(antennas=[-0.5, -0.5], duration=0.5) #le antenne si abbassano
                time.sleep(1.5)
                mini.goto_target(antennas=[0.0, 0.0], duration=0.5) 
                return False

    #blocco 7 chiusura valutazione finale 
    def chiusura(punteggio):
        if punteggio == 0:
            #se ha sbagliato tutte le domende, cambia il finale
            print("\nReachy: Oh, vedo che oggi le domande erano un po' difficili!")
            print("Reachy: Non ti preoccupare, l'importante è tenere la mente allenata e passare il tempo insieme")

            move_resigned = emotions.get("resigned1")
            if move_resigned: mini.play_move(move_resigned)

            mini.goto_target(antennas=[-0.5, -0.5], duration=0.5) # Movimento di empatia/dispiacere
            time.sleep(1.5)
            mini.goto_target(antennas=[0.0, 0.0], duration=0.5)
        else: 
             #se ne hai indovinate almeno una
            print(f"\nReachy: Bravissimo! Hai indovinato {punteggio} risposte su 3!")
            print("Reachy: Hai fatto un ottimo lavoro oggi, hai una bellissima memoria!")
            print("Reachy: È stato davvero splendido passare questo tempo con te.")
            mini.goto_target(antennas=[0.5, 0.5], duration=0.5)
            move = emotions.get("dance3")   
            if move: mini.play_move(move)
            mini.goto_target(antennas=[0.0, 0.0], duration=0.5)     


    #blocco 8 gioco 2: Indovina la canzone anni '60 per RSA   
    def indovinello_musicale():
         print("\nReachy: Adesso facciamo un gioco con la musica dei nostri tempi...")
         print("Reachy: Ti farò ascoltare una melodia speciale per 25 secondi. Vediamo se ti ricorda qualcosa!")

         move_think = emotions.get("thoughtful1")
         if move_think: mini.play_move(move_think)
         #Sostituite qui il percorso del vostro file audio anni '60 (il-cielo-gino copy)
         
         play_sound(MUSIC_FILE, duration=25.0)

         print("\nReachy: Che bella melodia... Ti ricordi il titolo della canzone o chi la cantava?")
         risposta = input("Utente: ").lower()

         # Parole chiave flessibili per agevolare il successo del gioco per gli ospiti in RSA
         if "paoli" in risposta or "gino" in risposta or "cielo" in risposta or "stanza" in risposta:
              print("\nReachy: Proprio così! Che meraviglia! E' il cielo in una stanza di Gino Paoli")
              print("Reachy: Hai una memoria musicale splendida, mi hai fatto emozionare!")
              move_happy = emotions.get("loving1")
              if move_happy: mini.play_move(move_happy)
              
              
         else:
              print("\nReachy: E' una canzone meravigliosa, vero? Era il cielo in una stanza del grande Gino Paoli")
              print("Reachy: l'importante è averla ascoltata insieme per ricordare le sue bellissime note")
              move_emp = emotions.get("understanding1")
              if move_emp: mini.play_move(move_emp)

    #blocco 9 motore  DFEL PROGRAMMA 
    saluto()
    if conferma():
        gioca_ancora = True
        
        while gioca_ancora:
        # Menu di scelta dell'attività 
            print("\n--- COSA FACCIAMO INSIEME? ---")
            print("1. Gioca con la Storia")
            print("2. Gioca con l'Indovinello Musicale")
            scelta_gioco = input("Scegli un'attività (1 o 2): ")
            
            if scelta_gioco == "1":
                storia()
                # Calcoliamo il punteggio finale in base alle risposte alle domande 
                punti = 0
                if domanda_uno(): punti += 1
                if domanda_due(): punti += 1
                if_risposta_tre = domanda_tre()
                if if_risposta_tre: punti += 1
                
                # Chiamiamo la chiusura personalizzata basata sui punti
                chiusura(punti)
                
            elif scelta_gioco == "2":
                indovinello_musicale()
            
            # Proposta di ritentare o cambiare attività
            scelta = input("\nReachy: Ti va di fare un altro gioco o allenarci ancora insieme? (si/no):") .lower()
            if scelta != "si":
                gioca_ancora = False 
                print("\nReachy: Grazie mille per aver passato questo tempo prezioso con me. A presto e buona giornata!")

    print("\nGruppo T, Michele Lombardi, Federica Mazzella e Sofia Torchio!")
           
    
    # QUI TERMINA IL CODICE DEL PROGETTO
