import socket
import ssl

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.load_verify_locations("server.crt")  # Load server SSL certificate for verification
    
    try:
        client_socket_ssl = context.wrap_socket(client_socket, server_hostname="10.1.20.168")
        client_socket_ssl.connect(('10.1.20.168', 8080))
        
        while True:
            item_name = client_socket_ssl.recv(1024).decode()
            if not item_name:
                break
            
            print(f"Bidding for {item_name}")
            while True:
                bid = input(f"Enter your bid for {item_name} (or 'end' to stop bidding for this item): ")
                client_socket_ssl.send(bid.encode())
                
                if bid.lower() == 'end':
                    break
                
                bidder_name = input("Enter your name: ")
                client_socket_ssl.send(bidder_name.encode())  # Send bidder's name along with each bid
                
                acknowledgment = client_socket_ssl.recv(1024).decode()
                if acknowledgment != "Bid received":
                    print("Error: Bid not received by server")
                    break
            
            acknowledgment_end = client_socket_ssl.recv(1024).decode()  # Receive acknowledgment for ending bidding for current item
            if acknowledgment_end != "Bidding ended":
                print("Error: Bidding not ended by server")
                break
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        client_socket_ssl.close()

if __name__ == "__main__":
    main()