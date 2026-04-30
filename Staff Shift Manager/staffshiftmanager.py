import datetime
import os
import time
import json


class Roleplayer:
    def __init__(self):
        self.options = {
            1: {"name": "Users Banned", "points": 0, "logs": []},
            2: {"name": "Unbanned", "points": 0, "logs": []},
            3: {"name": "Kicked", "points": 0, "logs": []},
            4: {"name": "Warned", "points": 0, "logs": []},
            5: {"name": "Muted", "points": 0, "logs": []},
            6: {"name": "Support Given", "points": 0, "logs": []},
            7: {"name": "Tickets Done", "points": 0, "logs": []}
        }

        self.error_message = ""
        self.temp_file = "temp_stafflog.txt"
        self.version = "1.7"
        self.load_temp_file()

    def load_temp_file(self):
        if os.path.exists(self.temp_file):
            try:
                with open(self.temp_file, "r") as file:
                    data = json.load(file)

                for k, v in data.items():
                    k = int(k)
                    if "logs" not in v:
                        v["logs"] = []
                    self.options[k] = v
            except:
                print("Temp file corrupted. Resetting...")
                self.save_temp_file()

    def save_temp_file(self):
        with open(self.temp_file, "w") as file:
            json.dump(self.options, file, indent=4)

    def select_option(self, option):
        if option in self.options:
            entry = {
                "user": "",
                "reason": "",
                "time": "",
                "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            print("\n--- Enter Details ---")

            entry["user"] = input("Username: ")
            entry["reason"] = input("Reason: ")

            if option in [1, 5]:
                entry["time"] = input("Duration (e.g. 10m, 1h, perm): ")
            else:
                entry["time"] = "N/A"

            self.options[option]["points"] += 1
            self.options[option]["logs"].append(entry)

            self.error_message = ""
            self.save_temp_file()
        else:
            self.error_message = "Invalid option."

    def remove_points(self, option, points):
        if option in self.options:
            if self.options[option]["points"] >= points > 0:
                self.options[option]["points"] -= points

                for _ in range(points):
                    if self.options[option]["logs"]:
                        self.options[option]["logs"].pop()

                self.error_message = ""
                self.save_temp_file()
            else:
                self.error_message = "Invalid number of points."
        else:
            self.error_message = "Invalid option."

    def show_info(self):
        info_file = "info.txt"
        print("\n--- Information ---\n")
        if os.path.exists(info_file):
            with open(info_file, "r") as file:
                print(file.read())
        else:
            print("Create 'info.txt' in the folder.")

    # ✅ NEW FEATURE
    def view_logs(self):
        print("\n--- Current Logs ---\n")

        found = False

        for option in self.options:
            data = self.options[option]

            if data["logs"]:
                found = True
                print(f"{data['name']} ({data['points']} points):\n")

                for i, log in enumerate(data["logs"], 1):
                    print(
                        f"  [{i}] User: {log['user']} | Reason: {log['reason']} | Duration: {log['time']} | Time: {log['timestamp']}"
                    )

                print()

        if not found:
            print("No logs found yet.")

        input("\nPress Enter to return...")

    def finish_deployment(self, start_time):
        print("\nFinish shift? (Y/N)")
        confirm = input().lower()

        if confirm == 'y':
            total_points = sum([self.options[o]["points"] for o in self.options])
            elapsed_time = time.time() - start_time

            if not os.path.exists("logs"):
                os.makedirs("logs")

            filename = f"logs/stafflog_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

            with open(filename, "w") as file:
                file.write(f"Total points: {total_points}\n\n")

                for option in self.options:
                    data = self.options[option]
                    file.write(f"{data['name']}: {data['points']} points\n")

                    for log in data["logs"]:
                        file.write(
                            f"  - User: {log['user']} | Reason: {log['reason']} | Duration: {log['time']} | Time: {log['timestamp']}\n"
                        )

                    file.write("\n")

                file.write(
                    f"Time elapsed: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}\n"
                )

            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)

            print(f"\nSaved to {filename}")
            return True

        elif confirm == 'n':
            return False
        else:
            self.error_message = "Invalid input."
            return False


def main():
    start_time = time.time()
    roleplayer = Roleplayer()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print(f"Cactos Tool v{roleplayer.version}")
        print("Remember To Always Check Punishment Info\n")

        print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        print("Options:")
        for option in roleplayer.options:
            data = roleplayer.options[option]
            print(f"{option}: {data['name']} [x{data['points']}]")

        if roleplayer.error_message:
            print(f"\nError: {roleplayer.error_message}")

        user_input = input(
            "\nSelect option | V=Logs | I=Info | R=Remove | F=Finish | K=Exit\n> ")

        if user_input.lower() == 'f':
            if roleplayer.finish_deployment(start_time):
                break

        elif user_input.lower() == 'r':
            try:
                option = int(input("Option #: "))
                points = int(input("Points to remove: "))
                roleplayer.remove_points(option, points)
            except:
                roleplayer.error_message = "Invalid input."

        elif user_input.lower() == 'k':
            print("Exiting...")
            break

        elif user_input.lower() == 'i':
            roleplayer.show_info()
            input("\nPress Enter...")

        elif user_input.lower() == 'v':
            roleplayer.view_logs()

        else:
            try:
                roleplayer.select_option(int(user_input))
            except:
                roleplayer.error_message = "Invalid input."


if __name__ == "__main__":
    main()
