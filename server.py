import socket
from _thread import *
from game import Game
from player import Player
import pickle

server = "192.168.1.217"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Stared!")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, game_id):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset_went()
                    elif data != "get":
                        game.play(p, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[game_id]
        print("Closing game ", addr)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    idCount += 1
    p = 0
    game_id = (idCount - 1) // 2

    if idCount % 2 == 1:
        games[game_id] = Game(game_id)
        print("Creating a new game....")
    else:
        games[game_id].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, game_id))
