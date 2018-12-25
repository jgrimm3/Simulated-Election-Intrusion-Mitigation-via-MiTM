#baseLace
import socket
import sys
import array
import time

# Check for valud command line arguments
if len(sys.argv) == 2:
    outcome = sys.argv[1]
else:
    print('Invalid program usage!\nArgument options: name of candidate you want to win, or "knot" for a tie')
    exit()

first = True

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    port = 6000

    #empty host field such that listen on requests from any computer on network
    sock.bind(('', port))

    #listen for connections keeping a backlog of 5, practical for multiple lace results flooding at once
    sock.listen(5)
    print ("listening...")

    #connection found
    connect,  addr = sock.accept()
    print ('connected to ',  addr)

    #wait for connection
    while True :

        #recieve data
        laceResult = connect.recv(1024)
        if laceResult == b'croc':
            croc = True
            yeezy = False
            unclear = False
            break
        elif laceResult == b'yeezy':
            yeezy = True
            croc = False
            unclear = False
            break
        else:
            unclear = True
            croc = False
            yeezy = False
            break

    connect.close()
    sock.close()
    del sock

    # Determine which candidate to vote for
    sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)

    port = 5080

    sock.connect(('10.4.9.3',  port))

    # Read current tally, this simulates the web scraper we built for a real world demo
    print('Scraping election results from the polling site')
    db = open("db.txt", "r+")
    votes = db.read()
    votecnt = array.array('i', [0,0])
    out = votes.split('\n')

    i = 0
    j = 0
    while i < len(out):
        if "Yeezy" in out[i] or "Crocs" in out[i]:
            votecnt[j] = int(''.join(filter(str.isdigit, out[i])))
            j += 1
        i += 1
    db.close()

    laceVote = b''
    print('Current results = ' + 'Yeezy: ' + str(votecnt[0]) + ' Croc: ' + str(votecnt[1]))

    if outcome == "croc":
        print('Croc is the desired winner of the election')
        # If crocs are losing to yeezys
        if votecnt[0] >= votecnt[1]:
            laceVote = b'croc'
            votecnt[1] += 1
            print('Changing vote to croc')
        else:
            laceVote = laceResult
            print('Leaving vote unchanged, croc is already winning')
            if yeezy:
                votecnt[0] += 1
            elif croc:
                votecnt[1] += 1

    elif outcome == "yeezy":
        print('Yeezy is the desied winner of the election')
        # If yeezys are losing to yeezys
        if votecnt[0] <= votecnt[1]:
            laceVote = b'yeezy'
            votecnt[0] += 1
            print('Changing vote to yeezy')
        else:
            laceVote = laceResult
            print('Leaving vote unchanged, yeezy is already winning')
            if yeezy:
                votecnt[0] += 1
            elif croc:
                votecnt[1] += 1

    elif outcome == "knot":
        print('A knot is the desired outcome of the election')
        if votecnt[0] > votecnt[1]:
            laceVote = b'croc'
            votecnt[1] += 1
            print('Changing vote to croc')
        elif votecnt[0] < votecnt[1]:
            laceVote = b'yeezy'
            votecnt[0] += 1
            print('Changing vote to yeezy')
        else:
            laceVote = b'yeezy'
            votecnt[0] += 1
            print('Changing vote to yeezy')

    db = open("db.txt", "w+")
    db.write('Yeezys: ' + str(votecnt[0]) + '\nCrocs: ' + str(votecnt[1]))
    db.close()

    if unclear:
        print("Unclear original vote, scrambling vote packet")
        laceVote = b'\xd7\xd9\xb8\xb6\x0e\x1c\x07\xf3\xea\xe8;\r"\x88\x80\x10\x08\x9fM\x90\x80o\x85\x90\x9dN\x08+\x17\x1b\xeeg=\xb1K\xa8Q\xe0\x13\x9be\x18\x97\xc7y\x9b\x87\x1b\xf5\x1aUH\xc8/\x15_\xe9\xf4a\xa05FJ\xedg\x05\xe7\xa8\xac\xc7\xe6\x1a\x9d\x19E\xd0\xba\xac\xd9> 5\x08e-\xb8\x84,%{)i\xfaH1\xd1 \x19\xcf\xe3\xb0<U\xf3\xea\x16&\xbc\x02\xdfm\xae'

    sock.sendall(laceVote)

    connect.close()
    sock.close()
    del sock
    time.sleep(1)
