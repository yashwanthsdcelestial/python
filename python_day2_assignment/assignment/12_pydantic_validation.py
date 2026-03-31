from pydantic import BaseModel, Field, field_validator, ValidationError, ConfigDict
from typing import Optional


class Address(BaseModel):
    """Address model with validation for zip code format."""
    
    street: str = Field(..., min_length=1, description="Street address")
    city: str = Field(..., min_length=1, description="City name")
    zip_code: str = Field(..., description="6-digit postal code")
    
    @field_validator("zip_code")
    @classmethod
    def validate_zip_code(cls, v):
        """
        Validate that zip code is exactly 6 digits.
        
        Args:
            v: The zip code value
            
        Returns:
            The validated zip code
            
        Raises:
            ValueError: If zip code is not exactly 6 digits
        """
        if not v.isdigit() or len(v) != 6:
            raise ValueError("zip_code must be exactly 6 digits")
        return v


class UserCreate(BaseModel):
    """User creation model with nested Address and comprehensive validation."""
    
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")
    age: int = Field(..., description="User age")
    address: Address = Field(..., description="User address (nested model)")
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        """
        Validate email format.
        
        Args:
            v: The email value
            
        Returns:
            The validated email
            
        Raises:
            ValueError: If email doesn't contain @ and .
        """
        if "@" not in v or "." not in v:
            raise ValueError("email must contain '@' and '.' characters")
        return v
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        """
        Validate password strength.
        
        Args:
            v: The password value
            
        Returns:
            The validated password
            
        Raises:
            ValueError: If password is too short
        """
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters long")
        return v
    
    @field_validator("age")
    @classmethod
    def validate_age(cls, v):
        """
        Validate age is within valid range.
        
        Args:
            v: The age value
            
        Returns:
            The validated age
            
        Raises:
            ValueError: If age is not between 18 and 120
        """
        if v < 18 or v > 120:
            raise ValueError("age must be between 18 and 120")
        return v


class UserResponse(BaseModel):
    """User response model (excludes password field)."""
    
    username: str
    email: str
    age: int
    address: Address
    
    model_config = ConfigDict(from_attributes=True)


# Test code demonstrating Pydantic validations
if __name__ == "__main__":
    print("=" * 70)
    print("PYDANTIC — USER SCHEMA WITH NESTED VALIDATION")
    print("=" * 70)
    print()
    
    # Test Case 1: Valid user creation
    print("--- Test Case 1: Valid User Creation ---\n")
    valid_data = {
        "username": "alice",
        "email": "alice@mail.com",
        "password": "securepass",
        "age": 25,
        "address": {
            "street": "MG Road",
            "city": "Bangalore",
            "zip_code": "560001"
        }
    }
    
    try:
        user = UserCreate(**valid_data)
        print("✓ UserCreate validation passed!")
        print(f"\nUserCreate object:\n{user}\n")
        
        # Create UserResponse (excludes password)
        user_response = UserResponse(**user.model_dump())
        print("✓ UserResponse created successfully (password excluded)!")
        print(f"\nUserResponse object:\n{user_response}\n")
        
        # Demonstrate model_dump() serialization
        print("UserResponse as dictionary (model_dump()):")
        print(user_response.model_dump())
        print()
    except ValidationError as e:
        print(f"✗ Validation Error:\n{e}\n")
    
    # Test Case 2: Invalid email (missing @)
    print("--- Test Case 2: Invalid Email Format ---\n")
    invalid_email_data = {
        "username": "bob",
        "email": "bobmail.com",  # Missing @
        "password": "securepass",
        "age": 30,
        "address": {
            "street": "Park Street",
            "city": "Mumbai",
            "zip_code": "400001"
        }
    }
    
    try:
        user = UserCreate(**invalid_email_data)
    except ValidationError as e:
        print(f"✗ Validation Error:")
        print(e)
    
    # Test Case 3: Invalid password (too short)
    print("\n--- Test Case 3: Invalid Password (Too Short) ---\n")
    invalid_password_data = {
        "username": "charlie",
        "email": "charlie@mail.com",
        "password": "short",  # Less than 8 characters
        "age": 35,
        "address": {
            "street": "Banjara Hills",
            "city": "Hyderabad",
            "zip_code": "500034"
        }
    }
    
    try:
        user = UserCreate(**invalid_password_data)
    except ValidationError as e:
        print(f"✗ Validation Error:")
        print(e)
    
    # Test Case 4: Invalid age (out of range)
    print("\n--- Test Case 4: Invalid Age (Out of Range) ---\n")
    invalid_age_data = {
        "username": "diana",
        "email": "diana@mail.com",
        "password": "securepass",
        "age": 150,  # Greater than 120
        "address": {
            "street": "Brigade Road",
            "city": "Bangalore",
            "zip_code": "560025"
        }
    }
    
    try:
        user = UserCreate(**invalid_age_data)
    except ValidationError as e:
        print(f"✗ Validation Error:")
        print(e)
    
    # Test Case 5: Invalid zip code (not 6 digits)
    print("\n--- Test Case 5: Invalid Zip Code (Not 6 Digits) ---\n")
    invalid_zip_data = {
        "username": "eve",
        "email": "eve@mail.com",
        "password": "securepass",
        "age": 28,
        "address": {
            "street": "The Forum",
            "city": "Bangalore",
            "zip_code": "56001"  # Only 5 digits
        }
    }
    
    try:
        user = UserCreate(**invalid_zip_data)
    except ValidationError as e:
        print(f"✗ Validation Error:")
        print(e)
    
    # Test Case 6: Multiple validation errors
    print("\n--- Test Case 6: Multiple Validation Errors ---\n")
    multiple_errors_data = {
        "username": "frank",
        "email": "frankmail",  # Missing @
        "password": "short",  # Too short
        "age": 200,  # Out of range
        "address": {
            "street": "Phoenix Market",
            "city": "Bangalore",
            "zip_code": "5600"  # Not 6 digits
        }
    }
    
    try:
        user = UserCreate(**multiple_errors_data)
    except ValidationError as e:
        print(f"✗ Validation Errors (Multiple):")
        print(e)
    
    # Summary
    print("\n" + "=" * 70)
    print("PYDANTIC FEATURES DEMONSTRATED")
    print("=" * 70)
    print("""
1. NESTED MODELS:
   • Address is a nested model within UserCreate
   • Validation cascades to nested models
   
2. FIELD VALIDATORS:
   • @field_validator decorator for custom validation logic
   • Separate validator for each field
   • Clear error messages

3. FIELD CONSTRAINTS:
   • Field(...) for required fields
   • min_length, max_length for string constraints
   • Description for field documentation

4. VALIDATION RULES:
   • Email: must contain '@' and '.'
   • Password: minimum 8 characters
   • Age: must be between 18 and 120
   • Zip Code: exactly 6 digits

5. MODEL EXCLUSION:
   • UserResponse excludes password field
   • Only includes username, email, age, address
   • Secure by design

6. SERIALIZATION:
   • model_dump() converts to dictionary
   • model_dump_json() converts to JSON
   • Maintains data integrity

7. VALIDATION ERROR:
   • Provides detailed error messages
   • Shows which field failed validation
   • Includes the validation failure reason

PYDANTIC BENEFITS:
   ✓ Type safety with Python type hints
   ✓ Automatic data validation
   ✓ Clear error messages for debugging
   ✓ JSON schema generation
   ✓ Supports nested models
   ✓ Easy serialization/deserialization
   ✓ Great for API request/response validation
    """)
