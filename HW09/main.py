def error_handler(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Give me name"
        except KeyError:
            return "Contact not found"
    return inner

dic_clients = {}

def hello(*args):
    return "How can I help you?"


def good_bye(*args):
    return None


def show_all(*args):
    if not dic_clients:
        return "No clients"
    string_clients = "Contacts:\n"
    for name, number in dic_clients.items():
        string_clients += f"{name} : {number}\n"
    return string_clients

@error_handler
def add(args):
    name, phone = args
    dic_clients[name] = phone
    return f"contact {name} with number {phone} added"

@error_handler
def change(args):
    name, phone = args
    dic_clients[name] = phone
    return f"contact {name} changed number {phone}"
    


@error_handler
def phone(args):
    name = args[0]
    return f"contact {name} has number {dic_clients[name]}"
   
    
def input_parser(client_text):
    if client_text.lower().startswith("show all"):
        args = ""
        command = "show all"
    else:
        command, *args = client_text.split()
    handler = dic_func.get(command.strip().lower())
    return handler, args


dic_func = {"hello": hello,
            "good bye": good_bye,
            "close": good_bye,
            "exit": good_bye,
            "show all": show_all,
            "add": add,
            "change": change,
            "phone": phone}


def main():
    while True:
        client_word = input("enter comand: ")
        cw_0, cw_1 = input_parser(client_word)
        result = cw_0(cw_1)


        if not result:
            print("Good Bye")
            break
        print(result)



if __name__ == "__main__":
    main()