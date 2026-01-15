# 1. Variables & Input
name = input("Enter name: ")
print("Hello", name)

# 2. If-Else
age = int(input("Enter age: "))
if age >= 18:
    print("Adult")
else:
    print("Minor")

# 3. Loop
for i in range(1, 6):
    print(i)

# 4. List + Dictionary
skills = ["Python", "HTML", "CSS"]

user = {
    "name": "Rishav",
    "skills": skills
}

print(user["skills"])

# 5. Function
def greet(name):
    return f"Hello {name}"

print(greet("Rishav"))

# 6. File Write + Read
with open("test.txt", "w") as f:
    f.write("Hello GenAI")

with open("test.txt", "r") as f:
    print(f.read())
