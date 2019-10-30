import socket
import datetime

with open("jpg_header.bin", "rb") as f:
    jpg_header = f.read()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('',1883))
pkgCntr = 0;





current_image_id = -1
def reset_image():
    global image_unstructured
    global received_images
    image_unstructured = []
    received_images = []


while True:
    print("Receiving a packet ...")
    message, address = server_socket.recvfrom(1024)
    pkgCntr += 1;
    print(datetime.datetime.now(), end=' ')
    print("Packet received:")
    print("From", address)
    print("Package count:", pkgCntr)
    
    # For each message, we have:
    # message[0] = image id
    # message[1] = chunk index
    # message[2] = number of chunks
    if message[0] != current_image_id:
        print("Image ID does not match. Resetting image ...")
        reset_image()
        current_image_id = message[0]
        print("Receiving image", current_image_id)
    # store message with header in a list
    image_unstructured.append(message)
    # save received index
    received_images.append(message[1])
    print("Stored image {}/{}".format(message[1], message[2]))
    print("Available image parts:", list(sorted(received_images)))
    # all parts received? 
    if list(sorted(received_images)) == list(range(message[2])):
        print()
        print()
        print("All image parts have been received. Storing image ...")
        # assemble image 
        # write to file in binary
        with open("img/" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".jpg", "wb") as f: 
            # Write jpg header first
            f.write(jpg_header)
            # iterate over all possible indices
            for i in range(message[2]):
                # find corresponding buffer 
                for buf in image_unstructured: 
                    if buf[1] == i:
                        # write in binary the image data (no header)
                        f.write(bytearray(buf[3:]))

        # Send 'ACK' response to camera module: the image index
        server_socket.sendto(message[0:1], address)

        # start a new image
        reset_image()
    
    #print(type(message))
    #print(message)
    #print("Answering the same packet back ... ", end='')
    #server_socket.sendto(message, address)
    #print("packet sent back.")
    print() # single newline for separating packets

