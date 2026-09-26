"""Country module managing state, resources, and annual dynamics."""

import random
from typing import Union


class Country:
    """Manages national state, resource depletion, and economic logic."""

    def __init__(self, name: str = "Aethelgard") -> None:
        self.name: str = name
        self.year: int = 2026

        # Core Parameters
        self.population: int = 1_000_000  # Total citizens
        self.water_resources: float = 80.0  # % capacity (0-100)
        self.food_supply: float = 75.0  # % capacity (0-100)
        self.treasury: float = 50_000_000.0  # Currency reserves in LC
        self.currency_exchange_rate: float = 1.0  # Relative to base standard
        self.inflation_rate: float = 2.0  # Annual percentage
        self.stability: float = 85.0  # Public stability percentage (0-100)
        self.tax_rate: float = 15.0  # Tax percentage (0-100)

    def print_status(self) -> None:
        """Display the current state of the nation in the console."""
        rate_str: str = f"1.00 USD = {1 / self.currency_exchange_rate:.2f} LC"
        print(f"\n{'=' * 50}")
        print(f"       STATE OF {self.name.upper()} - Year {self.year}")
        print(f"{'=' * 50}")
        print(f" Population       : {self.population:,} citizens")
        print(f" Water Resources  : {self.water_resources:.1f}% capacity")
        print(f" Food Supply      : {self.food_supply:.1f}% capacity")
        print(f" Treasury         : ${self.treasury:,.2f} LC")
        print(
            f" Currency Rate    : {rate_str} "
            f"(Valuation Index: {self.currency_exchange_rate:.2f})"
        )
        print(f" Inflation Rate   : {self.inflation_rate:.1f}%")
        print(f" Tax Rate         : {self.tax_rate:.1f}%")
        print(f" Public Stability : {self.stability:.1f}%")
        print(f"{'-' * 50}")

    def set_parameter(self, param: str, value: Union[int, float]) -> None:
        """Allow direct modification of country variables."""
        if hasattr(self, param):
            setattr(self, param, value)
            print(f" Successfully updated [{param}] to {value}.")
        else:
            print(f" Error: Parameter '{param}' does not exist.")

    def advance_year(self) -> None:
        """Simulate 1 year of events, dynamics, and resource interactions."""
        self.year += 1
        print(f"\n--- Simulating Year {self.year} ---")

        # 1. Economic Dynamics
        tax_revenue: float = (self.population * 150) * (self.tax_rate / 100.0)
        self.treasury += tax_revenue

        # Currency supply dynamics (Over-printing devalues currency)
        if self.treasury > 500_000_000:
            self.inflation_rate += 0.5
            self.currency_exchange_rate -= 0.05

        # High inflation devalues stability
        if self.inflation_rate > 8.0:
            self.stability -= 4.0

        # High tax rates reduce stability
        if self.tax_rate > 35.0:
            self.stability -= (self.tax_rate - 35.0) * 0.5

        # 2. Population & Resource Dynamics
        water_consumption: float = (self.population / 1_000_000) * 5.0
        self.water_resources = max(
            0.0, self.water_resources - water_consumption
        )

        food_consumption: float = (self.population / 1_000_000) * 4.0
        self.food_supply = max(0.0, self.food_supply - food_consumption)

        # Basic birth/death logic based on resources
        if self.water_resources > 30 and self.food_supply > 30:
            growth_rate: float = random.uniform(0.01, 0.03)
            self.population += int(self.population * growth_rate)
            self.stability = min(100.0, self.stability + 1.0)
        else:
            print(" WARNING: Critical resource shortages are occurring!")
            death_rate: float = random.uniform(0.03, 0.08)
            self.population -= int(self.population * death_rate)
            self.stability -= 10.0

        # Clamp stability bound
        self.stability = max(0.0, min(100.0, self.stability))

        # Check collapse state
        if self.stability <= 10.0:
            print("\n CRITICAL FAILURE: Civil unrest caused national collapse!")

    def invest_infrastructure(self, amount: float) -> None:
        """Spend treasury money to boost water and food infrastructure."""
        if amount > self.treasury:
            print(" Insufficient treasury funds!")
            return
        self.treasury -= amount
        boost: float = (amount / 1_000_000) * 2.5
        self.water_resources = min(100.0, self.water_resources + boost)
        self.food_supply = min(100.0, self.food_supply + boost)
        self.stability = min(100.0, self.stability + 1.5)
        print(
            f" Invested ${amount:,.2f}. "
            f"Water & food infrastructure improved by +{boost:.1f}%."
        )
