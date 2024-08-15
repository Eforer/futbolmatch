import requests
from datetime import datetime, timedelta

def get_availability(cancha_id, start_date, end_date):
    url = "http://localhost:5002/api/availability"
    
    params = {
        "cancha_id": cancha_id,
        "start_date": start_date,
        "end_date": end_date
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None

def print_availability(availability):
    if not availability:
        print("No hay reservas en el período especificado.")
        return
    
    for slot in availability:
        print(f"Fecha: {slot['date']}")
        print(f"Hora de inicio: {slot['start_time']}")
        print(f"Hora de fin: {slot['end_time']}")
        print(f"Reservado por: {slot['user_name']}")
        print("-" * 30)

def get_current_week_dates():
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week.strftime("%Y-%m-%d"), end_of_week.strftime("%Y-%m-%d")

def main():
    cancha_id = input("Ingrese el ID de la cancha: ")
    
    default_start, default_end = get_current_week_dates()
    print(f"\nFechas por defecto para esta semana:")
    print(f"Fecha de inicio: {default_start}")
    print(f"Fecha de fin: {default_end}")
    
    use_default = input("\n¿Usar fechas por defecto? (s/n): ").lower() == 's'
    
    if use_default:
        start_date = default_start
        end_date = default_end
    else:
        start_date = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
        end_date = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
    
    availability = get_availability(cancha_id, start_date, end_date)
    
    if availability is not None:
        print(f"\nDisponibilidad para la cancha {cancha_id} del {start_date} al {end_date}:")
        print_availability(availability)

if __name__ == "__main__":
    main()