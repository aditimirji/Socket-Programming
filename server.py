import socket
import threading
import ssl

def handle_client(client_socket, items):
    try:
        print(f"Connection established with {client_socket.getpeername()}")
        for item_name, _ in items:
            client_socket.send(item_name.encode())  # Send item name to client
            while True:
                bid = client_socket.recv(1024).decode()  # Receive bid from client
                if bid.lower() == 'end':
                    break
                bidder_name = client_socket.recv(1024).decode()  # Receive bidder's name from client
                bid = float(bid)
                # Store bid along with bidder's name
                for i, (name, bids) in enumerate(items):
                    if name == item_name:
                        bids.append((bid, bidder_name))
                        items[i] = (name, bids)
                        break
                client_socket.send("Bid received".encode())  # Send acknowledgment for bid
            
            # Send acknowledgment for ending bidding for current item
            client_socket.send("Bidding ended".encode())
        
        print("Bidding ended. Results:")
        # Display highest bid for each item
        for item_name, bids in items:
            if not bids:
                print(f"No bids for {item_name}")
            else:
                highest_bid, highest_bidder = max(bids, key=lambda x: x[0])
                print(f"Highest bid for {item_name}: {highest_bid} by {highest_bidder}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('10.1.20.168', 8080))
    server_socket.listen(5)
    print("Server is listening...")
    
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    
    items_count = int(input("Enter the number of items to bid for: "))
    items = []
    for i in range(items_count):
        item_name = input(f"Enter the name for item {i + 1}: ")
        items.append((item_name, []))  # Store item names and bids as a tuple
    
    while True:
        client_socket, _ = server_socket.accept()
        ssl_socket = context.wrap_socket(client_socket, server_side=True)
        
        client_thread = threading.Thread(target=handle_client, args=(ssl_socket, items))
        client_thread.start()

if __name__ == "__main__":
    main()