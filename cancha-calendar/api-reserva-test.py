import requests
from datetime import datetime, timedelta

def make_reservation(cancha_id, date, start_time, end_time, user_name):
    url = "http://localhost:5002/api/reservations"
    
    data = {
        "cancha_id": cancha_id,
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "user_name": user_name
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None

def main():
    # Obtener la fecha de hoy
    today = datetime.now().date().strftime("%Y-%m-%d")
    
    # Definir las horas de inicio y fin
    start_time = "22:00"
    end_time = "23:00"  # Asumimos que la reserva es por una hora
    
    print(f"Haciendo una reserva para hoy ({today}) de {start_time} a {end_time}")
    
    cancha_id = input("Ingrese el ID de la cancha: ")
    user_name = input("Ingrese su nombre: ")
    
    # Hacer la reserva
    result = make_reservation(cancha_id, today, start_time, end_time, user_name)
    
    if result:
        print("\nReserva realizada con éxito!")
        print(f"ID de la reserva: {result.get('reservation_id')}")
        print(f"Mensaje: {result.get('message')}")
    else:
        print("\nNo se pudo realizar la reserva.")

if __name__ == "__main__":
    main()