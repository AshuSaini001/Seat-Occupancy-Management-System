# main.py

def load_seats(filename="seats.txt"):
    with open("F:/LPU/Python/Project/seat.txt", "r") as f:
        return [list(map(int, line.strip().split())) for line in f]

def save_seats(seats, filename="seats.txt"):
    with open("F:/LPU/Python/Project/seat.txt", "w") as f:
        for row in seats:
            f.write(" ".join(map(str, row)) + "\n")

def display_seats(seats):
    print("\nSeat Map:")
    for row in seats:
        print(" ".join(["🟩" if s == 0 else "🟥" for s in row]))
    print()

def update_seat(seats, row, col, status):
    if 0 <= row < len(seats) and 0 <= col < len(seats[0]):
        seats[row][col] = status
    else:
        print("Invalid seat position!")

def count_seats(seats):
    total = sum(row.count(1) for row in seats)
    vacant = sum(row.count(0) for row in seats)
    return total, vacant

def main():
    seats = load_seats()

    while True:
        display_seats(seats)
        print("Options:")
        print("1. Mark seat")
        print("2. Count seats")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            r = int(input("Row: "))
            c = int(input("Column: "))
            s = int(input("Status (1=Occupied, 0=Vacant): "))
            update_seat(seats, r, c, s)
            save_seats(seats)

        elif choice == "2":
            occ, vac = count_seats(seats)
            print(f"Occupied: {occ}, Vacant: {vac}")

        elif choice == "3":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()