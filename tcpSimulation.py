import json
import re
import select
import socket

def iot_simulate():
    
    # the configuration data
    with open('./config.json', 'r') as file:
        config = json.load(file)

    # the command pairs
    with open(config["commandPairs"], 'r') as file:
        commandPairs = json.load(file)
    # normalize all of the command pair messages
    for commandPair in commandPairs:
        commandPair["message"] = commandPair["message"].encode('utf-8').decode('unicode_escape')
    server_socket = socket.socket() # get instance
    #bind to the socket
    server_socket.bind((config["host"], config["port"])) # bind the host and port
    # configure how many clients the server can listen to simultaneously
    server_socket.listen(5)
    inputs = [server_socket]
    buffers = {}
    # if each connection is authorized to connect
    authorizations = {}
    # Array of state variables
    stateVariables = ["0"]*10

    def parse_message(msg, conn):
        print(("Message Received: "+msg).encode())
        #if the correct password has been sent
        if msg == config["passwordString"]:
            authorizations[conn]=True
            conn.send(config["authSuccess"].encode())
        # if the connection is not authorized
        elif not authorizations[conn]:
            conn.send(config["unauthorizedResponse"].encode())
        # if there are command pairs
        elif commandPairs:
            matchFound = False
            # loop through the command pairs looking for a match
            for commandPair in commandPairs:
                savedMessage = commandPair["message"]
                # find a state variable in the message
                varIdx = savedMessage.find(config["stateVariable"])
                # index in the array of the variable
                arrIdx = -1
                # if there is a state variable in the message
                if varIdx != -1:
                    # get the number of characters
                    varChars = int(savedMessage[varIdx+2])
                    # Store in the index in the array where the variable is\
                    arrIdx = int(savedMessage[varIdx+1])
                    # Replace the variable with wildcard characters
                    savedMessage = savedMessage[:varIdx] + "[a-zA-Z0-9]"*varChars+ savedMessage[varIdx+3:]
                # look for question mark to be escaped
                qIdx = savedMessage.find('?')
                if qIdx != -1:
                    # insert the escape character
                    savedMessage = savedMessage[:qIdx]+"\\"+savedMessage[qIdx:]
                # look for a match with the message
                match = re.fullmatch(r""+savedMessage, msg)
                # if a match is found
                if match:
                    matchFound = True
                    # if there was a state variable in the message
                    if varIdx != -1:
                        # save the state variable
                        stateVariables[arrIdx] = msg[varIdx:varIdx+varChars]
                    # get the response
                    response = commandPair["response"]
                    # if there is a state variable in the response
                    varIdx = response.find(config["stateVariable"])
                    # if there is a state variable in the response
                    if varIdx != -1:
                        # replace the state variable with the value
                        response = response[:varIdx] + stateVariables[int(response[varIdx+1])] + response[varIdx+2:]
                    # if a match is found send the response
                    conn.send(response.encode())
                    print("Responding with: " + commandPair["response"])
                    break
            if not matchFound:
                conn.send(("No response found to message: "+msg).encode())
    while True:
        readable, _, _ = select.select(inputs, [], [], 10)
        for s in readable:
            if s is server_socket:
                client_socket, addr = server_socket.accept()
                inputs.append(client_socket)
                buffers[client_socket] = b''
                authorizations[client_socket]= not config["authRequired"]
                print("Connection from: " + str(addr))
            else:
                try:
                    byte = s.recv(1)
                    if not byte: # if no byte wait until the next loop
                        continue
                    # add the byte to the buffer
                    buffers[s] += byte
                    # if the byte is a carriage return
                    if byte == b'\r':
                        # parse the message
                        parse_message(buffers[s].decode('utf-8'), s)
                        # clear the buffer
                        buffers[s] = b''
                except (socket.error, ConnectionResetError):
                    print("Closing connection")
                    s.close()
                    inputs.remove(s)
                    del buffers[s]    
    
if __name__ == '__main__':
    iot_simulate()
