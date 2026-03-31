# Q10: Environment Variables Loader
# Read a .env file and load key=value pairs into a dictionary

# Step 1: Create a sample .env file
with open(".env", "w") as f:
    f.write("DB_HOST=localhost\nDB_PORT=5432")

# Step 2: Read and parse the .env file
def load_env(filepath):
    env_vars = {}   # Dictionary to store variables
    
    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()   # Remove spaces and newlines
            
            if line and "=" in line:               # Skip empty lines
                key, value = line.split("=", 1)    # Split on first '=' only
                env_vars[key] = value
    
    return env_vars

result = load_env(".env")
print("Output:", result)
# Output: {'DB_HOST': 'localhost', 'DB_PORT': '5432'}
