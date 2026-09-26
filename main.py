"""Main entry point for running the World Simulator interactive CLI."""

from typing import Union
from src.country import Country


def main() -> None:
    """Main terminal loop for the simulator."""
    print("Welcome to the World Simulator Terminal")
    default_name: str = "Aethelgard"
    user_input: str = input(f"Enter country name [Default: {default_name}]: ")
    country_name: str = user_input.strip() or default_name

    world: Country = Country(name=country_name)

    while True:
        world.print_status()
        print("\nActions:")
        print(" [1] Advance 1 Year")
        print(" [2] Modify Country Parameters (Set values directly)")
        print(" [3] Invest Treasury into Infrastructure")
        print(" [4] Adjust Tax Rate")
        print(" [5] Exit")

        choice: str = input("\nSelect an action (1-5): ").strip()

        if choice == "1":
            world.advance_year()
        elif choice == "2":
            print(
                "\nAvailable parameters: population, water_resources, "
                "food_supply, treasury, currency_exchange_rate, "
                "inflation_rate, tax_rate, stability"
            )
            param: str = input("Enter parameter name to change: ").strip()
            val: str = input("Enter new value: ").strip()
            try:
                new_val: Union[int, float] = (
                    float(val) if "." in val else int(val)
                )
                world.set_parameter(param, new_val)
            except ValueError:
                print(" Invalid numeric value.")
        elif choice == "3":
            try:
                amt: float = float(input("Enter amount to invest from treasury: "))
                world.invest_infrastructure(amt)
            except ValueError:
                print(" Invalid amount.")
        elif choice == "4":
            try:
                rate_in: float = float(input("Enter tax rate % (0-100): "))
                world.tax_rate = max(0.0, min(100.0, rate_in))
                print(f" Tax rate set to {world.tax_rate}%")
            except ValueError:
                print(" Invalid percentage.")
        elif choice == "5":
            print("Exiting simulator. Goodbye!")
            break
        else:
            print(" Invalid selection, please try again.")


if __name__ == "__main__":
    main()
