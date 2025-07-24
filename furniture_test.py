from main import IKEAFurniture
from datetime import timedelta
import json
from typing import Dict, List, Tuple

def validate_and_print_furniture(json_file: str) -> Tuple[List[IKEAFurniture], List[Dict]]:
    """Validate each furniture item and print individual validation statements.
    Returns tuple of (valid_items, invalid_items)"""
    with open(json_file) as f:
        data = json.load(f)
    
    valid_items = []
    invalid_items = []
    
    print("="*50)
    print("IKEA FURNITURE VALIDATION REPORT".center(50))
    print("="*50)
    print()
    
    for idx, item in enumerate(data, 1):
        validation_errors = []
        is_valid = True
        
        # Convert and validate assembly time first
        try:
            if 'estimated_assembly_time' in item:
                item['estimated_assembly_time'] = timedelta(seconds=item['estimated_assembly_time'])
        except Exception as e:
            validation_errors.append(f"Invalid assembly time: {str(e)}")
            is_valid = False
        
        # Validate the entire item
        try:
            furniture = IKEAFurniture(**item)
            
            # Additional manual validations
            if not all(k in furniture.dimensions for k in ['height', 'width', 'depth']):
                validation_errors.append("Missing dimensions")
                is_valid = False
                
            if furniture.price <= 0:
                validation_errors.append("Price must be positive")
                is_valid = False
                
            if furniture.weight <= 0:
                validation_errors.append("Weight must be positive")
                is_valid = False
                
            if furniture.weight > 100:
                validation_errors.append("Weight must be less than or equal to 100kg")
                is_valid = False
        
            if furniture.estimated_assembly_time.total_seconds() <= 0:
                validation_errors.append("Assembly time must be positive")
                is_valid = False
                
        except Exception as e:
            validation_errors.append(str(e))
            is_valid = False
        
        # Print validation statement
        print(f"ITEM {idx}: {item.get('name', 'UNKNOWN').upper()}")
        print(f"  Product ID: {item.get('product_id', 'MISSING')}")
        
        if is_valid:
            valid_items.append(furniture)
            print("  Overall Status: ✅ VALID (All checks passed)")
            print(f"  Details: {furniture.category}, ${furniture.price:.2f}")
            print(f"  Dimensions: {furniture.dimensions['height']}×{furniture.dimensions['width']}×{furniture.dimensions['depth']}cm")
            print(f"  Weight: {furniture.weight}kg, Assembly: {furniture.estimated_assembly_time}")
            print(f"  Stock: {'✅ In Stock' if furniture.in_stock else '⚠️ Out of Stock'}")
        else:
            invalid_items.append({"item": item, "errors": validation_errors})
            print("  Overall Status: ❌ INVALID")
            print("  Validation Errors:")
            for error in validation_errors:
                print(f"    - {error}")
        
        print("-"*50)
    
    return valid_items, invalid_items

# Run the validation
if __name__ == "__main__":
    valid_items, invalid_items = validate_and_print_furniture("ikeaFurniture.json")
    
    # Print summary
    print("\nVALIDATION SUMMARY:")
    print(f"Total Items Processed: {len(valid_items) + len(invalid_items)}")
    print(f"✅ Valid Items: {len(valid_items)}")
    print(f"❌ Invalid Items: {len(invalid_items)}")
    
    if invalid_items:
        print("\nINVALID ITEMS DETAILS:")
        for idx, item in enumerate(invalid_items, 1):
            print(f"{idx}. {item['item'].get('name', 'UNKNOWN')} (ID: {item['item'].get('product_id', 'MISSING')})")
            for error in item['errors']:
                print(f"   - {error}")
