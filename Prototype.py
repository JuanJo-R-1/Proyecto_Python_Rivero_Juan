import os
import json
import hashlib
import random
from datetime import datetime

lottery_size = 0
ticket_price = 0
lottery_prize = 0

def clean_term():#limpia la terminal para mayor orden
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def ask_letters(message, only_letters=True):
    while True:
        text = input(message).strip()
        if only_letters:
            if text.replace(" ", "").isalpha():
                if text > " " and len(text) > 20:
                    print("Error. The text must not exceed 20 characters. Try again.")
                    continue
                elif text > " " and len(text) <= 20:
                    print("Text accepted.")
                    return text
            else:
                print("Error. Only letters are allowed. Try again.")
        else:
            if text:
                return text
            else:
                print("Error, This space can't be clear.")

def ask_lottery_number(used_numbers):
    while True:
        bet = input(f"Enter the number that the participant wants to bet (only numbers and {lottery_size}, is the limit): ").strip()
        if bet.isdigit():
            num = int(bet)
            if num in used_numbers:
                print("Error. That number has already been chosen by another participant. Try another one.")
            elif 1 <= num <= lottery_size:
                print("Number accepted.")
                return bet
            else:
                print(f"Error. The bet number must be between 1 and {lottery_size}, try again.")
        else:
            print("Error. The bet number must be written with numbers, try again.")

def save_config():
    config = {
        "lottery_size": lottery_size,
        "lottery_prize": lottery_prize,
        "ticket_price": ticket_price
    }
    with open("config.json", "w") as f:
        json.dump(config, f)

def load_config():
    global lottery_size, lottery_prize, ticket_price
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            lottery_size = config.get("lottery_size", 0)
            lottery_prize = config.get("lottery_prize", 0)
            ticket_price = config.get("ticket_price", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        lottery_size = 0
        lottery_prize = 0
        ticket_price = 0
if __name__ == "__main__":
    try:
        with open("suerte.json", "r") as file:
            content = file.read().strip()
            if not content:
                with open("suerte.json", "w") as file:
                    json.dump([], file)
    except FileNotFoundError:
        with open("suerte.json", "w") as file:
            json.dump([], file)

def bet_size():
    global lottery_size
    clean_term()
    while True:
        try:
            size = int(input("Enter the size of the lottery : "))
            if size > 1000000:
                print("Error. The size of the lottery must be less than 1000000, try again.")
            elif size <= 1:
                print("Error. The size of the lottery must be more than 1, try again.")
            else:
                print(f"The size of the lottery is {size}, acceptable.")
                lottery_size = size
                save_config()  # <--- Guarda la configuración
                return size
        except ValueError:
            print("Error. The size of the lottery must be a number, try again.")

def Asign_lottery_prize():
    clean_term()
    global lottery_prize
    while True:
        try:
            prize = int(input("Enter the prize of the lottery (money): "))
            if prize > 1000000000:
                print("Error. The lottery prize must be less than 1000000000, try a lower prize")
            elif prize <= 100000:
                print("Error. The lottery prize must be more than 100000, try a higher prize")
            else:
                print(f"the size of the lottery is {prize}, acceptable")
                lottery_prize = prize
                save_config()  # <--- Guarda la configuración
                return prize
        except ValueError:
            print("Error. The prize of the lottery must be a number, try again")

def Asign_ticket_price():
    clean_term()
    global ticket_price
    while True:
        ticket_price = ((lottery_prize/lottery_size)*1.2)
        print(f"the price of the tickets wiil be: {ticket_price}")
        save_config()  # <--- Guarda la configuración
        return ticket_price

def user_data(current_user=None):
    global lottery_size
    if lottery_size == 0:
        print("You must set the size of the lottery before adding participants.")
        return
    clean_term()
    participants = []
    used_numbers = set()
    try:
        with open("suerte.json", "r") as file:
            existing = json.load(file)
            for p in existing:
                used_numbers.add(int(p["Number"]))
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []
    if current_user:  # Usuario normal, solo puede agregarse a sí mismo
        Name = current_user
        ticket = ask_lottery_number(used_numbers)
        used_numbers.add(int(ticket))
        participants.append({"Name": Name, "Number": ticket})
        all_participants = existing + participants
        with open("suerte.json", "w") as file:
            json.dump(all_participants, file, indent=4)
            print("Data saved.")
    else:  # Admin, puede agregar cualquier nombre
        Name = ask_letters("Enter the participant Name (Only letters, max 20 chars): ").strip()
        ticket = ask_lottery_number(used_numbers)
        used_numbers.add(int(ticket))
        participants.append({"Name": Name, "Number": ticket})
        all_participants = existing + participants
        with open("suerte.json", "w") as file:
            json.dump(all_participants, file, indent=4)
            print("Data saved.")

def show_participants():#muestra a los participantes que hay en el momento
    clean_term()
    try:
        with open("suerte.json", "r") as file:
            participants = json.load(file)
            if participants:
                print("Current participants:")
                for participant in participants:
                    print(f"Name: {participant['Name']}, Numbers: {', '.join(participant['Numbers'])}")#muestra los nombres y numeros, si no hay, pide ingresar
            else:
                print("No participants found.")
    except FileNotFoundError:
        print("No participants data found. Please add participants first.")

def edit_participants():#edita la informacion de los participantes, nombre(sin repetir) y el numero de apuesta
    clean_term()
    try:
        with open("suerte.json", "r") as file:
            participants = json.load(file)
            if not participants:
                print("No participants were found to edit.")
                return
            print("Current participants:")
            for idx, participant in enumerate(participants, 1):
                print(f"{idx}. Name: {participant['Name']}, Numbers: {', '.join(participant['Numbers'])}")
            idx_to_edit = int(input("Enter the number of the user you want to edit: ")) - 1
            if 0 <= idx_to_edit < len(participants):
                new_name = ask_letters("Enter the new name for the participant: ")
                new_numbers = ask_six_numbers()
                participants[idx_to_edit]['Name'] = new_name
                participants[idx_to_edit]['Numbers'] = new_numbers
                with open("suerte.json", "w") as file:
                    json.dump(participants, file, indent=4)
                print("Participant updated successfully.")
            else:
                print("out of range.")
    except FileNotFoundError:
        print("No participants data found. Please add participants first.")
    except ValueError:
        print("Invalid character.")

def delete_participants():
    clean_term()
    try:
        with open("suerte.json", "r") as file:
            participants = json.load(file)
            if not participants:
                print("No participants were found to delete.")
                return
            print("Current participants:")
            for idx, participant in enumerate(participants, 1):
                print(f"{idx}. Name: {participant['Name']}, Numbers: {', '.join(participant['Numbers'])}")
            idx_to_delete = int(input("Enter the number of the ticket you want to delete: ")) - 1
            if 0 <= idx_to_delete < len(participants):
                del participants[idx_to_delete]
                with open("suerte.json", "w") as file:
                    json.dump(participants, file, indent=4)
                print("Participant deleted successfully.")
            else:
                print("Índice fuera de rango.")
    except FileNotFoundError:
        print("No participants data found. Please add participants first.")
    except ValueError:
        print("Entrada inválida.")

def play_lottery():#juega la lotería
    clean_term()
    try:
        with open("suerte.json", "r") as file:
            participants = json.load(file)
            if not participants:
                print("No participants found. Please add participants first.")
                return
    except FileNotFoundError:
        print("No participants data found. Please add participants first.")
        return
    winner_ticket = Make_winner_ticket()
    print(f"\nWinner ticket: {' '.join(winner_ticket)}\n")
    results = []
    prizes = {6: "Biggest prize", 5: "Medium prize", 4: "Small prize", 3: "No prize", 2: "No prize", 1: "No prize", 0: "No prize"}
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_tickets = len(participants)
    total_money = ticket_price * total_tickets
    investment = total_money - lottery_prize
    for ticket in participants:
        successes = len(set(ticket["Numbers"]) & set(winner_ticket))
        if successes == 6:
            Revenue = lottery_prize/2
        elif successes == 5:
            Revenue = lottery_prize/3
        elif successes == 4:
            Revenue = lottery_prize/6
        else:
            Revenue = 0
        Revenue -= ticket_price
        results.append({
            "Date": date,
            "Name": ticket["Name"],
            "Ticket": ticket["Numbers"],
            "successes": successes,
            "Prize": prizes.get(successes, "No prize"),
            "Revenue": Revenue
        })
    for r in results:    # Mostrar resultados
        print(f"{r['Date']} | {r['Name']} | Ticket: {' '.join(r['Ticket'])} | successes: {r['successes']} | {r['Prize']} | Revenue: {r['Revenue']}")
    print(f"\nTotal money got: {total_money}")
    print(f"total prize: {lottery_prize}")
    print(f"Extra Revenue for the admin: {investment}")
    # Guardar historial
    try:
        with open("w_history.json", "r") as hfile:
            history = json.load(hfile)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    history.append({
        "Date": date,
        "Winner_ticket": winner_ticket,
        "results": results,
        "total_money": total_money,
        "investment": investment
    })
    with open("w_history.json", "w") as hfile:
        json.dump(history, hfile, indent=4)
    print("\nResults saved in the record.")

def press_ent():#presionar Enter para continuar
    input('Press Enter to continue')

def menu():
    while True:
        clean_term() # Muestra los participantes antes del menu del admin
        print("=== Current participants ===")
        try:
            with open("suerte.json", "r") as file:
                content = file.read().strip()
                if not content:  # Verifica si el archivo está vacío(sin participantes)
                    print("No participants data found.")
                    participants = []
                else:
                    participants = json.loads(content)
                    if participants:
                        for participant in participants:
                            print(f"Name: {participant['Name']}, Numbers: {participant['Numbers']}")
                    else:
                        print("No participants found.")
        except FileNotFoundError:
            print("No participants data found.")
        except json.JSONDecodeError:
            print("Error reading participants data. The file may be corrupted.")
        print("\n")
        print("""
1.  Enter the size of the lottery              
2.  Enter the lottery prize
3.  Enter the ticket price
4.  Show current participants
5.  Edit participants
6.  Delete participants
7.  Play the lottery
8.  Show the list of winners
9.  Exit
""")
        try:
            option = int(input("select one of the options: \n"))
        except ValueError:
            print("Enter a valid option (only numbers).")
            press_ent()
            continue
        if option == 1:
            bet_size()
            press_ent()
        elif option == 2:
            Asign_lottery_prize()
            press_ent()
        elif option == 3:
            Asign_ticket_price()
            press_ent()
        elif option == 4:
            show_participants()
            press_ent()
        elif option == 5:
            edit_participants()
            press_ent()
        elif option == 6:
            delete_participants()
            press_ent()
        elif option == 7:
            play_lottery()
            press_ent()
        elif option == 8:
            press_ent()
        elif option == 9:
            return start()
        else:
            print('Enter a valid option')
            press_ent()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()#codifica la contraseña del admin para mayor seguridad

def generate_unique_code(users):#Se encarga de generar el codigo de 4 digitos para los usuarios, el admin elige su propio codigo
    while True:
        code = "{:04d}".format(random.randint(0, 9999))
        if not any(u.get("code") == code for u in users.values()):
            return code

def register_user():
    clean_term()
    username = input("Choose a username: ").strip()#opcion del usuario a ingresar el nombre de su cuenta
    try:
        with open("Users.json", "r") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}
    if username in users:
        print("That username is already taken.")#Evita que los usuarios tenga un nombre identico, ejemplo David y David, pero se permite David y David S, etc.desde que no sea identico.
        return False
    if users and any(u["role"] == "admin" and username == admin for admin, u in users.items()):#Evita que un usuario normal use el nombre del admin
        print("You cannot use the admin's username.")
        return False
    if not users:
        clean_term()
        password = input("Choose a password: ").strip()#Se crea un usuario de administrador, único
        while True:
            code = input("Enter a 4-digit admin code (e.g. 1234): ").strip()#el admin elige su propio codigo de 4 digitos
            if code.isdigit() and len(code) == 4:
                break
            print("Code must be exactly 4 digits.")
        role = "admin"#Se crea el usuario de administrador
        users[username] = {
            "password": hash_password(password),
            "role": role,
            "code": code
        }
        print(f"Admin registered with code: {code}")
        press_ent()
    else:
        clean_term()
        code = generate_unique_code(users)#Se crea uno de multiples usuarios normales
        role = "user"
        users[username] = {
            "role": role,
            "code": code
        }
        print(f"User registered. Your access code is: {code}")
        press_ent()
    with open("users.json", "w") as f:
        json.dump(users, f)
    print(f"User registered successfully as {role}.")
    return start()

def login_user(): #Se usa ingresar el nombre del usuario en la pagina a menos que no se encuentre el usuario, lo regresa al menu principal
    clean_term()
    username = input("Username: ").strip()
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No users registered.")
        return start()
    if username in users:#si el usuario existe, le ejecuta lo siguiente
        user = users[username]
        if user["role"] == "admin":#si elige admin, le pide el usuario, la contraseña y el codigo
            password = input("Password: ").strip()
            code = input("Admin code (4 digits): ").strip()
            if user.get("password") == hash_password(password) and user.get("code") == code:
                print("Login successful as admin.")#si es correcto ingresa como admin
                return username, "admin"
            else:
                print("Invalid password or code.")
                return start()
        else:
            code = input("Enter your 4-digit code: ").strip()#ejecuta la entrada de un usuario normal con su codigo y nombre
            if user.get("code") == code:
                print("Login successful as user.")
                return username, "user"
            else:
                print("Invalid code.")
                return start()
    else:
        clean_term()
        print("User not found. If you are new, please register first.") #si el usuario no existe lo regresa a la pagina principal para que se registre o ingrese de forma correcta el nombre, quien sabe
        return start()

def start():#Genera la pagina principal, el menu,
    clean_term()
    while True:
        try:
            with open("Users.json", "r") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = {}
        if users:
            print("""
                
[̲̅$̲̅( ͡• ‿ ͡•)̲̅$̲̅]  [̲̅$̲̅( ͡• ‿ ͡•)̲̅$̲̅]  [̲̅$̲̅( ͡• ‿ ͡•)̲̅$̲̅]

████████████████████████████████████████████
██▄ ▄███ ▄▄ █ ▄ ▄ █ ▄ ▄ █▄ ▄▄ █▄ ▄▄▀█▄ █ ▄██
███ ██▀█ ██ ███ █████ ████ ▄█▀██ ▄ ▄██▄ ▄███
█▀▄▄▄▄▄▀▄▄▄▄▀▀▄▄▄▀▀▀▄▄▄▀▀▄▄▄▄▄▀▄▄▀▄▄▀▀▄▄▄▀▀█

███████████████████████████████████
████▄ ▀█▀ ▄█▄ ▄▄ █▄ ▀█▄ ▄█▄ ██ ▄███
█████ █▄█ ███ ▄█▀██ █▄▀ ███ ██ ████
██▀▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▀▄▄▄▄▀▀██

[̲̅$̲̅( ͡• ‿ ͡•)̲̅$̲̅]  [̲̅$̲̅( ͡• ‿ ͡•)̲̅$̲̅]  [̲̅$̲̅( ͡• ‿ ͡•)̲̅$̲̅]
                
                1. Login
                2. Register
                3. Exit
                
                """)#Da las opciones para que el usuario realize
            choice = input("Choose an option: ")
            if choice == "1":
                clean_term()
                username, role = login_user()
                if username:
                    if role == "admin":#muestra el menu editable para el administrador
                        menu()
                    else:
                        user_menu(username)#Muestra el menu para usuario normales sin posibilidad de editar aspectos, solo su desicion de participar o no
                    break
            elif choice == "2":#Creacion de usuarios
                clean_term()
                register_user()
            elif choice == "3":
                print("Goodbye!")
                break #vuelve a la pagina principal
            else:
                print("Invalid option.")
        else:
            print("No admin registered. Please register the admin user.")#el admin es el primer usuario en ser creado, ademas de ser unico, si no existe, se pide
            register_user()

def user_menu(current_user): #presenta el menu con las respectivas opciones que el usuario normal puede elegir
    while True:
        clean_term()
        print(f"Welcome, {current_user}.\n")
        print("1. See current participants")
        print("2. buy tickets")
        print("3. Exit to main menu")
        option = input("Select one option: ")
        if option == "1":
            show_participants()
            press_ent()
        elif option == "2":
            buy_tickets(current_user)
            press_ent()
        elif option == "3":
            return start() #vuelve a la pagina principal
        else:
            print("Invalid option. Please try again.")
            press_ent()

def build_used_by_position(participants):
    used_by_position = [set() for _ in range(6)]
    for boleto in participants:
        for idx, num in enumerate(boleto["Numbers"]):
            used_by_position[idx].add(num)
    return used_by_position

def buy_tickets(current_user):
    global lottery_size, ticket_price
    if lottery_size == 0 or ticket_price == 0:
        print("The lottery isn't available for now. Please wait.")
        return
    try:
        with open("suerte.json", "r") as file:
            existing = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []
    used_by_position = build_used_by_position(existing)
    print(f"The price for the ticket: {ticket_price}")
    while True:
        try:
            money = float(input("¿How much money do you want to spend?: "))
            if money < ticket_price:
                print("You don't have enough money to buy a ticket.")
                return
            break
        except ValueError:
            print("Enter a valid quantity of money.")
    # El máximo de boletos posibles es el mínimo de números disponibles en cualquier posición
    max_possible_tickets = min(99 - len(pos) for pos in used_by_position)
    max_tickets = min(int(money // ticket_price), max_possible_tickets)
    if max_tickets == 0:
        print("There aren't enough available numbers to buy a ticket.")
        return
    print(f"You can buy up to {max_tickets} tickets.")
    while True:
        try:
            num_tickets = int(input(f"¿How many tickets do you want to buy? (1-{max_tickets}): "))
            if 1 <= num_tickets <= max_tickets:
                break
            else:
                print("Quantity out of range")
        except ValueError:
            print("Enter a valid number.")
    tickets = []
    for i in range(num_tickets):
        print(f"\nEnter the 6 numbers for the ticket #{i+1} (between 01 and 99, no repeat in this ticket or in other tickets):")
        ticket = ask_six_numbers_by_position(used_by_position)
        if not ticket:
            print("No se pudo generar el boleto. Ya no hay suficientes números disponibles para más boletos.")
            break  # <-- Rompe el ciclo si ya no se pueden generar más boletos
        tickets.append({"Name": current_user, "Numbers": ticket})
        for idx, num in enumerate(ticket):
            used_by_position[idx].add(num)
    all_participants = existing + tickets
    with open("suerte.json", "w") as file:
        json.dump(all_participants, file, indent=4)
    order_suerte_json()
    print(f"¡You have bought {len(tickets)} tickets!")

def Make_winner_ticket(): #Genera un boleto ganador aleatorio con 6 numeros del 01 al 99, para que los usuarios que mas se parezcan ganen premios
    return sorted([str(random.randint(1, 99)).zfill(2) for _ in range(6)])

def order_suerte_json():
    try:
        with open("suerte.json", "r") as file:
            data = json.load(file)
        data.sort(key=lambda x: x["Name"])# Ordena a los usuarios y sus numeros en el archivo suerte.json
        with open("suerte.json", "w") as file:
            json.dump(data, file, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def ask_six_numbers(used_numbers_global):
    while True:
        choice = input("¿Do you wanna enter the numbers yourself(M) or randomly(A)? [M/A]: ").strip().upper()
        if choice in ("M", "A"):
            break
        print("Invalid choice. Please enter 'M' for manual or 'A' for automatic.")
    numbers = []
    if choice == "M":
        while len(numbers) < 6:
            num = input(f"number {len(numbers)+1}: ").zfill(2)
            if num.isdigit() and 1 <= int(num) <= 99 and num not in numbers and num not in used_numbers_global:
                numbers.append(num)
            else:
                print("Invalid number. It must be between 01 and 99, not repeated in this ticket or in other tickets.")
    else:  # Aleatorio
        posibility = [str(i).zfill(2) for i in range(1, 100) if str(i).zfill(2) not in used_numbers_global]
        if len(posibility) < 6:
            print("There isn't enough numbers available to generate a ticket. Cancelling this ticket.")
            return []
        numbers = random.sample(posibility, 6)
    return numbers

def ask_six_numbers_by_position(used_by_position):
    while True:
        choice = input("¿Quieres ingresar los números manualmente (M) o aleatoriamente (A)? [M/A]: ").strip().upper()
        if choice in ("M", "A"):
            break
        print("Opción inválida. Escribe 'M' o 'A'.")
    numbers = []
    for pos in range(6):
        disponibles = [str(i).zfill(2) for i in range(1, 100) if str(i).zfill(2) not in used_by_position[pos]]
        if not disponibles:
            print(f"No hay números disponibles para la posición {pos+1}. No se puede generar más boletos.")
            return []
        if choice == "M":
            while True:
                num = input(f"Número para la posición {pos+1} (entre 01 y 99, no repetido en esta posición): ").zfill(2)
                if num in disponibles:
                    numbers.append(num)
                    break
                else:
                    print("Número inválido o ya usado en esta posición. Elige otro.")
        else:  # Aleatorio
            num = random.choice(disponibles)
            print(f"Número aleatorio para la posición {pos+1}: {num}")
            numbers.append(num)
    return numbers

load_config()  # <--- Carga la configuración guardada
start()