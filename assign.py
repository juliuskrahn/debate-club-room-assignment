import csv
import random


class Participant:
    def __init__(self, name, language, is_speaker, could_not_speak_last_time, group_name, level):
        self.name = name
        self.language = language or "EN"
        self.is_speaker = is_speaker == "YES"
        self.could_not_speak_last_time = could_not_speak_last_time == "YES"
        self.group_name = group_name or ""
        self.level = level or "BEGINNER"


def load_participants(filename):
    participants = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Überspringe die Kopfzeile
        for row in reader:
            if len(row) == 6:
                participant = Participant(*row)
                participants.append(participant)
    return participants


class Room:
    def __init__(self, name, language, level):
        self.name = name
        self.language = language
        self.judge = None
        self.positions = []
        self.level = level


def get_rooms():
    rooms = []
    while True:
        room_name = input("Geben Sie den Raumnamen ein (leer lassen zum Beenden): ")
        if not room_name:
            break
        language = input("Ist der Raum für Language EN oder GE? (EN/GE): ")
        level = input("Ist der Raum für Level ADVANCED, BEGINNER oder BOTH?: ")
        room = Room(room_name, language, level)
        rooms.append(room)
    return rooms


def assign_participants_to_rooms(participants, rooms):
    random.shuffle(participants)

    groups = {}
    for participant in participants:
        if participant.group_name:
            if participant.group_name not in groups:
                groups[participant.group_name] = []
            groups[participant.group_name].append(participant)

    judges_by_language = {}
    for participant in participants:
        if not participant.is_speaker:
            if participant.language not in judges_by_language:
                judges_by_language[participant.language] = []
            judges_by_language[participant.language].append(participant)
    for room in rooms:
        eligible_judges = judges_by_language.get(room.language, [])
        if eligible_judges:
            judge = eligible_judges.pop(0)
            room.judge = judge.name

    prioritized_speaker_participants = [p for p in participants if p.could_not_speak_last_time and p.is_speaker]\
                                       + [p for p in participants if not p.could_not_speak_last_time and p.is_speaker]

    for room in rooms:
        for position in ["Opening Government", "Closing Government", "Opening Opposition", "Closing Opposition"]:

            for number in range(1, 3):  # 1 & 2
                if not prioritized_speaker_participants:
                    break

                participant = prioritized_speaker_participants.pop([i for i, p in enumerate(prioritized_speaker_participants)
                    if p.language == room.language
                    and (p.level == room.level or room.level == "BOTH")
                    and (number == 1 or not p.group_name)][0])  # selecting random fitting participant
                room.positions.append((position, participant.name))

                if participant.group_name:
                    # attach partner, only happens if this participant was the first one on this position
                    groups[participant.group_name].remove(participant)
                    if groups[participant.group_name]:
                        group_partner = groups[participant.group_name].pop()
                        prioritized_speaker_participants.remove(group_partner)
                        room.positions.append((position, group_partner.name))
                        break


def save_room_assignments(filename, rooms):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        for room in rooms:
            writer.writerow([room.name, room.language, "Judge", room.judge or "-"])
            for position in room.positions:
                writer.writerow([room.name, room.language, *position])


def generate_random_participants(filename):
    names = [
        "Alice", "Bob", "Carol", "Dave", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack",
        "Kathy", "Liam", "Mia", "Noah", "Olivia", "Pete", "Quinn", "Rachel", "Sam", "Tina",
        "Uma", "Vince", "Wendy", "Xander", "Yasmin", "Zack", "Abby", "Brian", "Cindy", "Derek",
        "Elena", "Fred", "Gina", "Howard", "Ingrid", "Joel", "Karen", "Leo", "Mona", "Nate",
        "Opal", "Pablo", "Queen", "Randy", "Sylvia", "Tom", "Ursula", "Victor", "Willa", "Xavier",
        "Yolanda", "Zeke", "Amber", "Bruce", "Clara", "Dexter", "Elise", "Felix", "Gloria", "Harold",
        "Ida", "Julian", "Krista", "Lorenzo", "Mabel", "Nolan", "Olive", "Paul", "Queenie", "Roger",
        "Sienna", "Travis", "Ulysses", "Valerie", "Wilbur", "Xenia", "Yvette", "Zion", "April", "Blaine",
        "Cora", "Drake", "Estelle", "Floyd", "Gemma", "Heath", "Isla", "Jared", "Keira", "Lance",
        "Maya", "Neil", "Octavia", "Phil", "Rhea", "Sterling", "Thalia", "Uriah", "Vera", "Wayne",
        "Xander", "Yara", "Zander", "Annie", "Barrett", "Celia", "Dominic", "Elsa", "Flynn", "Gretchen"
    ]

    languages = ["EN", "GE"]
    speaker_status = ["YES", "NO"]
    could_not_speak_last_time = ["YES", "NO"]
    group_names = ["groupA", "", "", "groupD", "", "", "", "", "", ""]
    levels = ["ADVANCED", "BEGINNER"]

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Name", "Language EN/GE", "Speaker (YES/ NO means Judge)", "Could not speak last time (YES)", "Group Name (leave blank)", "Level (ADVANCED/ BEGINNER)"])

        for name in names:
            data = [
                name,
                random.choice(languages),
                random.choice(speaker_status),
                random.choice(could_not_speak_last_time),
                random.choice(group_names),
                random.choice(levels)
            ]
            writer.writerow(data)


def main():
    participants_file = input("Bitte geben Sie den Pfad der Participants CSV-Datei ein: ")
    rooms_file = input("Bitte geben Sie den Pfad der Rooms CSV-Datei ein: ")
    participants = load_participants(participants_file)
    rooms = get_rooms()
    assign_participants_to_rooms(participants, rooms)
    save_room_assignments(rooms_file, rooms)
    print(f"Die Zuordnung wurde erfolgreich in {rooms_file} gespeichert.")


if __name__ == "__main__":
    # generate_random_participants("Participants.csv")
    main()
