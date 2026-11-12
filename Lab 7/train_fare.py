
BERTHS = ["SU", "LB", "MB", "UB", "LB", "MB", "UB", "SL"]


def parse_pnr(pnr):
    # Check whether PNR is a valid 10-digit string
    if not isinstance(pnr, str):
        return None

    if len(pnr) != 10 or not pnr.isascii() or not pnr.isdigit():
        return None

    return int(pnr[0]), int(pnr[1:])


def journey_distance(distances_csv):
    # Check whether input is a string
    if not isinstance(distances_csv, str):
        return None

    try:
        distances = [int(d.strip()) for d in distances_csv.split(',')]

        # At least one distance must be provided
        if not distances:
            return None

        return distances[-1] - distances[0]

    except ValueError:
        return None


def berth_type(seat):
    # Check whether input is a string
    if not isinstance(seat, str):
        return None

    try:
        parts = seat.split('-')

        # Exactly two parts are required
        if len(parts) != 2:
            return None

        coach, number = parts
        coach = coach.strip()
        number = number.strip()

        if not coach or not number:
            return None

        if not number.isascii() or not number.isdigit():
            return None

        number = int(number)

        if number <= 0:
            return None

        return coach.upper(), BERTHS[number % 8]

    except (ValueError, IndexError):
        return None


def main():
    print("==== Running parse_pnr ====")
    user_input = input("Enter a 10 digit PNR (e.g. 4521367890): ")
    result = parse_pnr(user_input)
    print("Zone and Number:", result if result is not None else "Invalid PNR")

    print("\n==== Running journey_distance ====")
    user_input = input("Enter station distances as CSV (e.g. 0,120,340): ")
    result = journey_distance(user_input)
    print("Total Distance:", result if result is not None else "Invalid distances")

    print("\n==== Running berth_type ====")
    user_input = input("Enter coach and seat (e.g. S3-45): ")
    result = berth_type(user_input)
    print("Coach and Berth:", result if result is not None else "Invalid seat")


if __name__ == "__main__":
    main()
