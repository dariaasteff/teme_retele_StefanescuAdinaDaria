import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999
BUFFER_SIZE = 1024
TIMEOUT     = 5

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

este_conectat = False

def trimite_comanda(mesaj: str) -> str:
    try:
        client_socket.sendto(mesaj.encode('utf-8'), (SERVER_HOST, SERVER_PORT))
        date_brute, _ = client_socket.recvfrom(BUFFER_SIZE)
        return date_brute.decode('utf-8')
    except socket.timeout:
        return "EROARE: Serverul nu raspunde (timeout)."
    except Exception as e:
        return f"EROARE: {e}"

print("=" * 55)
print("  CLIENT UDP - Seminar 9")
print("=" * 55)
print("  Comenzi disponibile:")
print("    CONNECT              - conectare la server")
print("    DISCONNECT           - deconectare de la server")
print("    PUBLISH <mesaj>      - publicare mesaj")
print("    DELETE <id>          - stergere mesaj dupa ID")
print("    LIST                 - afisare toate mesajele")
print("    EXIT                 - inchidere client")
print("=" * 55)
print()

while True:
    try:
        intrare = input(">> ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nInchidere client...")
        break

    if not intrare:
        continue

    parti = intrare.split(' ', 1)
    comanda = parti[0].upper()
    argument = parti[1] if len(parti) > 1 else ''

    if comanda == 'EXIT':
        print("Inchidere client...")
        break

    # --- VERIFICARE LOCALĂ A CONEXIUNII ---
    # Pentru orice comanda in afara de CONNECT si EXIT, trebuie sa fim conectati
    if comanda in ['PUBLISH', 'DELETE', 'LIST', 'DISCONNECT'] and not este_conectat:
        print("EROARE LOCALĂ: Trebuie să fii conectat pentru a folosi această comandă.")
        continue

    if comanda == 'CONNECT':
        raspuns = trimite_comanda(intrare)
        print(raspuns)
        if raspuns.startswith("OK"):
            este_conectat = True

    elif comanda == 'DISCONNECT':
        raspuns = trimite_comanda(intrare)
        print(raspuns)
        if raspuns.startswith("OK"):
            este_conectat = False

    elif comanda == 'PUBLISH':
        # --- VALIDARE LOCALĂ PUBLISH ---
        if not argument:
            print("EROARE LOCALĂ: Comanda PUBLISH necesită un mesaj (ex: PUBLISH Salut).")
            continue
        
        raspuns = trimite_comanda(intrare)
        print(raspuns)

    elif comanda == 'DELETE':
        # --- VALIDARE LOCALĂ DELETE ---
        if not argument or not argument.isdigit():
            print("EROARE LOCALĂ: Comanda DELETE necesită un ID numeric (ex: DELETE 1).")
            continue
            
        raspuns = trimite_comanda(intrare)
        print(raspuns)

    elif comanda == 'LIST':
        raspuns = trimite_comanda(intrare)
        print(raspuns)

    else:
        print(f"Comanda '{comanda}' nu este recunoscuta de client.")
        print("Comenzi valide: CONNECT, DISCONNECT, PUBLISH, DELETE, LIST, EXIT")

client_socket.close()
print("Socket inchis. La revedere!")