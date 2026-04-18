import socket

def server() -> None:
    HOST = '172.17.9.55'    
    PORT = 6666               
    balance = 100000         

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)
    print(f"Сервер запущен на {HOST}:{PORT}, начальный баланс: {balance}")

    conn, address = server_socket.accept()
    print(f"Подключение от {address}")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        try:
            parts = data.split(':')
            if parts[0] == 'TRANS' and len(parts) == 2:
                amount = int(parts[1])

                if amount > 25000:
                    response = "Сумма перевода превышает 25000"
                elif amount > balance:
                    response = f"Недостаточно средств"
                else:
                    balance -= amount
                    response = str(balance)   
                    print(f"Перевод на {amount} выполнен /n Остаток: {balance}")
        except ValueError:
            response = "Сумма должна быть > 0"
        except Exception as e:
            response = f"{e}"

        conn.send(response.encode())

    conn.close()

if __name__ == '__main__':
    server()