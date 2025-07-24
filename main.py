from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal, Dict
from decimal import Decimal
from sqlmodel import SQLModel, Field
from datetime import timedelta

class IKEAFurniture(SQLModel, table=True):
    """A SQLModel representing IKEA furniture items that can be stored in a database.

    Attributes:
        id: Optional primary key for database.
        name: The name of the furniture product.
        product_id: The unique IKEA product ID.
        price: The price of the furniture in local currency.
        dimensions: Dictionary of furniture dimensions (height, width, depth) in centimeters.
        in_stock: Availability status of the product.
        category: The category of furniture (e.g., 'Bookcase', 'Chair', 'Table').
        weight: The weight of the item in kilograms.
        color: The primary color of the furniture.
        material: The primary material used in construction.
        estimated_assembly_time: Estimated time required for assembly.
    """
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., min_length=1, max_length=50, description="Name of the furniture product")
    product_id: str = Field(..., description="IKEA product ID", regex=r'^\d{3}\.\d{3}\.\d{2}$')
    price: float = Field(...,  description="Product price in local currency", gt=Decimal("0"), decimal_places=2)
    dimensions: Dict[str, float] = Field(..., description="Dictionary containing 'height', 'width', and 'depth' in centimeters", sa_type="JSON")
    in_stock: bool = Field(False, description="Whether the product is currently in stock")
    category: str = Field( ..., description="Category of furniture")
    weight: float = Field( ...,  description="Weight in kilograms", gt=0, le=100.00, decimal_places=2)
    color: str = Field( ...,   description="Primary color of the furniture" )
    material: str = Field( ..., description="Primary material used in construction")
    estimated_assembly_time: timedelta = Field( ..., description="Estimated time required for assembly")

    def get_volume(self) -> float:
        """Calculate the volume of the furniture item in cubic centimeters.

        Returns:
            float: The product of height × width × depth.
        
        Raises:
            ValueError: If any dimension is missing in the dimensions dictionary.
        """
        required_dims = {"height", "width", "depth"}
        if not required_dims.issubset(self.dimensions.keys()):
            missing = required_dims - set(self.dimensions.keys())
            raise ValueError(f"Missing dimension(s): {missing}")
            
        return self.dimensions["height"] * self.dimensions["width"] * self.dimensions["depth"]

    def __str__(self) -> str:
        """Return a user-friendly string representation of the furniture item.
        
        Returns:
            str: Formatted string containing product name, ID and price.
        """
        return f"IKEA {self.name} (ID: {self.product_id}), Price: {self.price}, Category: {self.category}"

def main():
    """Example usage of the IkeaFurniture class."""

    # Valid furniture item
    try:
        billy_bookcase = IKEAFurniture(
            name="BILLY Bookcase",
            product_id="002.638.50",
            price=79.99,
            dimensions={"height": 202.0, "width": 80.0, "depth": 28.0},
            in_stock=True,
            category="Bookcase",
            weight=25.3,
            color="White",
            material="Particleboard/ABS plastic",
            estimated_assembly_time=timedelta(minutes=45)
        )
        print("✅ Valid furniture created successfully!")
        print(f"Name: {billy_bookcase.name}")
        print(f"Price: ${billy_bookcase.price}")
        print(f"Dimensions: {billy_bookcase.dimensions}")
    except Exception as e:
        print(f"❌ Validation error: {e}")

if __name__ == "__main__":
    main()