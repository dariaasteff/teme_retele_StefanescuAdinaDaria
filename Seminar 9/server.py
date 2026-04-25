import socket

HOST        = '127.0.0.1'
PORT        = 9999
BUFFER_SIZE = 1024

# --- STRUCTURI DE DATE NOI ---
clienti_conectati = {}
mesaje = []      # Lista de dictionare: {"id": int, "text": str, "autor": tuple}
next_id = 1      # Contor pentru ID-uri unice

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print("=" * 50)
print(f"  SERVER UDP pornit pe {HOST}:{PORT}")
print("  Asteptam mesaje de la clienti...")
print("=" * 50)

while True:
    try:
        date_brute, adresa_client = server_socket.recvfrom(BUFFER_SIZE)
        mesaj_primit = date_brute.decode('utf-8').strip()

        parti = mesaj_primit.split(' ', 1)
        comanda = parti[0].upper()
        argumente = parti[1] if len(parti) > 1 else ''

        print(f"\n[PRIMIT] De la {adresa_client}: '{mesaj_primit}'")

        # --- LOGICA DE CONECTARE ---
        if comanda == 'CONNECT':
            if adresa_client in clienti_conectati:
                raspuns = "EROARE: Esti deja conectat la server."
            else:
                clienti_conectati[adresa_client] = True
                nr_clienti = len(clienti_conectati)
                raspuns = f"OK: Conectat cu succes. Clienti activi: {nr_clienti}"
                print(f"[SERVER] Client nou conectat: {adresa_client}")

        elif comanda == 'DISCONNECT':
            if adresa_client in clienti_conectati:
                del clienti_conectati[adresa_client]
                raspuns = "OK: Deconectat cu succes. La revedere!"
                print(f"[SERVER] Client deconectat: {adresa_client}")
            else:
                raspuns = "EROARE: Nu esti conectat la server."

        # --- VERIFICARE OBLIGATORIE PENTRU RESTUL COMENZILOR ---
        elif adresa_client not in clienti_conectati:
            raspuns = "EROARE: Trebuie sa fii conectat (foloseste CONNECT)."

        # --- LOGICA PENTRU MESAJE ---
        elif comanda == 'PUBLISH':
            if not argumente:
                raspuns = "EROARE: Mesajul nu poate fi gol."
            else:
                nou_mesaj = {
                    "id": next_id,
                    "text": argumente,
                    "autor": adresa_client
                }
                mesaje.append(nou_mesaj)
                raspuns = f"OK: Mesaj publicat cu ID={next_id}"
                next_id += 1

        elif comanda == 'DELETE':
            try:
                id_de_sters = int(argumente)
                gasit = False
                
                for m in mesaje:
                    if m["id"] == id_de_sters:
                        gasit = True
                        # Verificam daca cel care sterge este autorul (IP si Port)
                        if m["autor"] == adresa_client:
                            mesaje.remove(m)
                            raspuns = f"OK: Mesajul {id_de_sters} a fost sters."
                        else:
                            raspuns = "EROARE: Nu poti sterge mesajul altui utilizator!"
                        break
                
                if not gasit:
                    raspuns = f"EROARE: ID-ul {id_de_sters} nu exista."
            except ValueError:
                raspuns = "EROARE: ID-ul trebuie sa fie un numar intreg."

        elif comanda == 'LIST':
            if not mesaje:
                raspuns = "INFO: Nu exista mesaje publicate."
            else:
                # Construim lista de mesaje sub forma de string
                linii = [f"ID {m['id']}: {m['text']}" for m in mesaje]
                raspuns = "\n" + "\n".join(linii)

        else:
            raspuns = f"EROARE: Comanda '{comanda}' este necunoscuta."

        server_socket.sendto(raspuns.encode('utf-8'), adresa_client)
        print(f"[TRIMIS]  Catre {adresa_client}: '{raspuns}'")

    except KeyboardInterrupt:
        print("\n[SERVER] Oprire server...")
        break
    except Exception as e:
        print(f"[EROARE] {e}")

server_socket.close()
print("[SERVER] Socket inchis.")