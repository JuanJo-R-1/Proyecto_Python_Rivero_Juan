import os
import json
import hashlib
import random

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
                return prize
        except ValueError:
            print("Error. The prize of the lottery must be a number, try again")

def Asign_ticket_price():#calcula el precio del boleto, teniendo en cuenta el premio y la cantidad de personas
    clean_term()
    global ticket_price
    while True:
        ticket_price = ((lottery_prize/lottery_size)*1.2)
        print(f"the price of the tickets wiil be: {ticket_price}")
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
                    print(f"Name: {participant['Name']}, Number: {participant['Number']}")#muestra los nombres y numeros, si no hay, pide ingresar
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
            for participant in participants:
                print(f"Name: {participant['Name']}, Number: {participant['Number']}")
            number = input("Enter the number by which the participant bet to edit: ").strip()#numero de la lotería
            found = False
            for participant in participants:
                if participant['Number'] == number:
                    new_name = ask_letters("Enter the new name for the participant: ")#nuevo nombre del usuario
                    used_numbers = set(int(p["Number"]) for p in participants if p["Number"] != number)
                    new_number = ask_lottery_number(used_numbers)
                    participant['Name'] = new_name
                    participant['Number'] = new_number
                    found = True
                    break
            if found:
                with open("suerte.json", "w") as file:
                    json.dump(participants, file, indent=4)
                    print("Participant updated successfully.")#guardado confirmado
            else:
                print("No participant found with that number.")
    except FileNotFoundError:
        print("No participants data found. Please add participants first.")

def delete_participants():#desicion del admin de borrar participantes(usuarios normales)
    clean_term()
    participants = []
    try:
        with open("suerte.json", "r") as file:
            participants = json.load(file)
            if not participants:
                print("No participants were found to delete.")
                return
            print("Current participants:")
            for participant in participants:
                print(f"Name: {participant['Name']}, Number: {participant['Number']}")
            number = input("Enter the number by which the participant bet to delete: ").strip()#los elige por el numero que eligieron
            new_participants = [p for p in participants if p['Number'] != number]
            if len(new_participants) < len(participants):
                with open("suerte.json", "w") as file:
                    json.dump(new_participants, file, indent=4)
                    print("Participant deleted successfully.")
            else:
                print("No participant found with that number.")
    except FileNotFoundError:
        print("No participants data found. Please add participants first.")

def play_lottery():#juega la lotería
    clean_term()
    try:
        with open("suerte.json", "r") as file:
            participants = json.load(file)
            if not participants:#ejecuta los participantes que hay, si no, no ejecuta y menciona que no hay
                print("No participants found. Please add participants first.")
                return
            assigned_numbers = [int(p["Number"]) for p in participants]#solo usa los numeros que ya fueron ocupados por los participantes
            num_winners = min(6, len(assigned_numbers))
            winners_numbers = [random.choice(assigned_numbers) for _ in range(num_winners)]
            winners = [next(p for p in participants if int(p["Number"]) == wn) for wn in winners_numbers]
            print("Winners of the lottery:")#menciona a los ganadores de la lotería que fueron elegidos de forma aleatoria
            for idx, winner in enumerate(winners, 1):
                print(f"{idx}. Name: {winner['Name']}, Number: {winner['Number']}")
            try:
                with open("w_history.json", "r") as hfile:
                    history = json.load(hfile)
            except (FileNotFoundError, json.JSONDecodeError):
                history = []
            history_entry = {
                "winners": winners,
                "numbers": winners_numbers#menciona a los ganadores con sus  numeros y los almacena en su archivo json
            }
            history.append(history_entry)
            with open("w_history.json", "w") as hfile:
                json.dump(history, hfile, indent=4)
            print("Winners saved to history.")
    except FileNotFoundError:
        print("No participants data found. Please add participants first.")
        return

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
                            print(f"Name: {participant['Name']}, Number: {participant['Number']}")
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
        clean_term()#Se crea un usuario de administrador, único
        password = input("Choose a password: ").strip()
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
    else:
        clean_term()
        code = generate_unique_code(users)#Se crea uno de multiples usuarios normales
        role = "user"
        users[username] = {
            "role": role,
            "code": code
        }
        print(f"User registered. Your access code is: {code}")
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
                break
            else:
                print("Invalid option.")
        else:
            print("No admin registered. Please register the admin user.")#el admin es el primer usuario en ser creado, ademas de ser unico, si no existe, se pide
            register_user()

def user_menu(current_user): #presenta el menu con las respectivas opciones que el usuario normal puede elegir
    while True:
        clean_term()
        print(f"Bienvenido, {current_user}.\n")
        print("1. Ver participantes")
        print("2. Comprar boletos de lotería")
        print("3. Salir")
        option = input("Selecciona una opción: ")
        if option == "1":
            show_participants()
            press_ent()
        elif option == "2":
            buy_tickets(current_user)
            press_ent()
        elif option == "3":
            break
        else:
            print("Opción inválida.")
            press_ent()

def buy_tickets(current_user): #si la loteria no ha sido configurada, no permite participar todavia, si está activa, continua el proceso con los datos almacenados
    global lottery_size, ticket_price
    if lottery_size == 0 or ticket_price == 0:
        print("La lotería aún no está configurada. Intenta más tarde.")
        return
    try:
        with open("suerte.json", "r") as file:
            existing = json.load(file)
            used_numbers = set(int(p["Number"]) for p in existing)
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []
        used_numbers = set()

    print(f"El precio de cada boleto es: {ticket_price}")#Pone el valor de el boleto segun la ecuacion que ya se realizo antes, pero aca a eleccion y capacidad del usuario de cuantos boletos va a querer
    while True:
        try:
            money = float(input("¿Cuánto dinero deseas ingresar para comprar boletos?: "))
            if money < ticket_price:
                print("No tienes suficiente para comprar un boleto.")
                return
            break
        except ValueError:
            print("Ingresa una cantidad válida.")

    max_tickets = int(money // ticket_price)# pone limites de cantidad de boletos y la eleccion de cuantos boletos va a querer el usuario normal
    print(f"Puedes comprar hasta {max_tickets} boletos.")
    while True:
        try:
            num_tickets = int(input(f"¿Cuántos boletos deseas comprar? (1-{max_tickets}): "))
            if 1 <= num_tickets <= max_tickets:
                break
            else:
                print("Cantidad fuera de rango.")
        except ValueError:
            print("Ingresa un número válido.")

    tickets = [] #Se realiza la eleccion del numero de la lotería por el que el usuario normal va a elegir
    for i in range(num_tickets):
        while True:
            ticket_num = input(f"Ingrese el número para el boleto #{i+1} (1-{lottery_size}, sin repetir): ").strip()
            if ticket_num.isdigit():
                ticket_num = int(ticket_num)
                if ticket_num in used_numbers:
                    print("Ese número ya está ocupado. Elige otro.")
                elif 1 <= ticket_num <= lottery_size:
                    used_numbers.add(ticket_num)
                    tickets.append({"Name": current_user, "Number": ticket_num})
                    break
                else:
                    print(f"El número debe estar entre 1 y {lottery_size}.")
            else:
                print("Debes ingresar un número válido.")

    all_participants = existing + tickets #se realiza la compra de boletos por parte de los usuarios normales
    with open("suerte.json", "w") as file:
        json.dump(all_participants, file, indent=4)
    print(f"¡Has comprado {num_tickets} boletos!")

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
    start()