from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from decimal import Decimal

class IKEAFurniture:
    """A class representing IKEA furniture items.

    Attributes:
        name (str): The name of the furniture product.
        product_id (str): The unique IKEA product ID.
        price (float): The price of the furniture in local currency.
        dimensions (dict[str, float]): Dictionary of furniture dimensions (height, width, depth).
        in_stock (bool): Availability status of the product.
    """

    def __init__(
        self,
        name: str,
        product_id: str,
        price: float,
        dimensions: dict[str, float],
        in_stock: bool = False
    ) -> None:
        """Initialize an IKEA furniture item.

        Args:
            name: Name of the furniture product (e.g., 'BILLY Bookcase').
            product_id: IKEA product ID (e.g., '002.638.50').
            price: Product price in local currency.
            dimensions: Dictionary containing 'height', 'width', and 'depth' in centimeters.
            in_stock: Whether the product is currently in stock. Defaults to False.
        """
        self.name = name
        self.product_id = product_id
        self.price = price
        self.dimensions = dimensions
        self.in_stock = in_stock

    def get_volume(self) -> float:
        """Calculate the volume of the furniture item in cubic centimeters.

        Returns:
            The product of height × width × depth.
        """
        return (
            self.dimensions["height"] * self.dimensions["width"] * self.dimensions["depth"]
        )

    def __str__(self) -> str:
        """Return a string representation of the furniture item."""
        return f"IKEA {self.name} (ID: {self.product_id}), Price: {self.price}"

# Example usage
sample = IKEAFurniture(
    name="BILLY Bookcase",
    product_id="002.638.50",
    price=59.99,
    dimensions={"height": 202, "width": 80, "depth": 28},
    in_stock=True
)
print(sample)
#print(sample.get_volume())