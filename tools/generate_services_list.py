USERNAME = "student_admin"
PASSWORD = "password1!"
COMMAND = "id"


def main():
    with open("hosts.txt") as f:
        lines = f.readlines()
    
    services = []
    for host in lines:
        target = {
            "server": host.strip(),
            "username": USERNAME,
            "password": PASSWORD,
            "command": COMMAND
        }
        services.append(target)
    
    print(services)


if __name__ == "__main__":
    main()