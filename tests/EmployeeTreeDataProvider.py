class Employee:
    def __init__(self, name, designation, salary, age, years_of_service, location, email, gender):
        self.name = name
        self.designation = designation
        self.salary = salary
        self.age = age
        self.years_of_service = years_of_service
        self.location = location
        self.email = email
        self.gender = gender
        self.subordinates = []
    
    def add_subordinate(self, employee):
        self.subordinates.append(employee)
        return employee
    
    def remove_subordinate(self, employee):
        self.subordinates.remove(employee)
    
    def get_subordinates(self):
        return self.subordinates
    
    def display(self, level=0):
        indent = "  " * level
        print(f"{indent}{self.name} ({self.designation})")
        print(f"{indent}  Salary: ${self.salary:,}")
        print(f"{indent}  Age: {self.age}")
        print(f"{indent}  Gender: {self.gender}")
        print(f"{indent}  Years of Service: {self.years_of_service}")
        print(f"{indent}  Location: {self.location}")
        print(f"{indent}  Email: {self.email}")
        
        for subordinate in self.subordinates:
            subordinate.display(level + 1)
    
    def find_employee(self, name):
        if self.name == name:
            return self
        
        for subordinate in self.subordinates:
            found = subordinate.find_employee(name)
            if found:
                return found
        
        return None
    
    def get_total_employees(self):
        count = 1  # Count self
        for subordinate in self.subordinates:
            count += subordinate.get_total_employees()
        return count


# Create the organizational structure
def create_org_structure():
    # Level 1: President
    president = Employee(
        name="Jennifer Hughes",
        designation="President",
        salary=375000,
        age=58,
        years_of_service=15,
        location="New York, NY",
        email="j.hughes@company.com",
        gender="Female"
    )
    
    # Level 2: Directors
    director_sales = president.add_subordinate(Employee(
        name="Michael Chen",
        designation="Sales Director",
        salary=210000,
        age=45,
        years_of_service=10,
        location="Chicago, IL",
        email="m.chen@company.com",
        gender="Male"
    ))
    
    director_tech = president.add_subordinate(Employee(
        name="Sandra Powell",
        designation="Technology Director",
        salary=230000,
        age=42,
        years_of_service=8,
        location="San Francisco, CA",
        email="s.powell@company.com",
        gender="Female"
    ))
    
    director_hr = president.add_subordinate(Employee(
        name="Robert Martinez",
        designation="HR Director",
        salary=190000,
        age=49,
        years_of_service=12,
        location="New York, NY",
        email="r.martinez@company.com",
        gender="Male"
    ))
    
    # Level 3: Managers
    manager_sales_east = director_sales.add_subordinate(Employee(
        name="Patricia Williams",
        designation="East Region Sales Manager",
        salary=120000,
        age=38,
        years_of_service=7,
        location="Boston, MA",
        email="p.williams@company.com",
        gender="Female"
    ))
    
    manager_sales_west = director_sales.add_subordinate(Employee(
        name="David Kim",
        designation="West Region Sales Manager",
        salary=125000,
        age=36,
        years_of_service=5,
        location="Seattle, WA",
        email="d.kim@company.com",
        gender="Male"
    ))
    
    manager_frontend = director_tech.add_subordinate(Employee(
        name="Alicia Rodriguez",
        designation="Frontend Manager",
        salary=140000,
        age=34,
        years_of_service=6,
        location="San Francisco, CA",
        email="a.rodriguez@company.com",
        gender="Female"
    ))
    
    manager_backend = director_tech.add_subordinate(Employee(
        name="Thomas Johnson",
        designation="Backend Manager",
        salary=145000,
        age=39,
        years_of_service=9,
        location="Austin, TX",
        email="t.johnson@company.com",
        gender="Male"
    ))
    
    manager_recruitment = director_hr.add_subordinate(Employee(
        name="Lisa Thompson",
        designation="Recruitment Manager",
        salary=110000,
        age=41,
        years_of_service=8,
        location="New York, NY",
        email="l.thompson@company.com",
        gender="Female"
    ))
    
    # Level 4: Employees
    # Sales team employees
    manager_sales_east.add_subordinate(Employee(
        name="Kevin Patel",
        designation="Senior Sales Executive",
        salary=85000,
        age=32,
        years_of_service=4,
        location="Boston, MA",
        email="k.patel@company.com",
        gender="Male"
    ))
    
    manager_sales_east.add_subordinate(Employee(
        name="Sophia Garcia",
        designation="Sales Executive",
        salary=65000,
        age=27,
        years_of_service=2,
        location="Philadelphia, PA",
        email="s.garcia@company.com",
        gender="Female"
    ))
    
    manager_sales_west.add_subordinate(Employee(
        name="James Wilson",
        designation="Senior Sales Executive",
        salary=87000,
        age=34,
        years_of_service=5,
        location="Los Angeles, CA",
        email="j.wilson@company.com",
        gender="Male"
    ))
    
    manager_sales_west.add_subordinate(Employee(
        name="Emily Taylor",
        designation="Sales Executive",
        salary=67000,
        age=26,
        years_of_service=1,
        location="Portland, OR",
        email="e.taylor@company.com",
        gender="Female"
    ))
    
    # Tech team employees
    manager_frontend.add_subordinate(Employee(
        name="Daniel Lee",
        designation="Senior Frontend Developer",
        salary=110000,
        age=31,
        years_of_service=4,
        location="San Francisco, CA",
        email="d.lee@company.com",
        gender="Male"
    ))
    
    manager_frontend.add_subordinate(Employee(
        name="Olivia Brown",
        designation="Frontend Developer",
        salary=90000,
        age=28,
        years_of_service=3,
        location="San Francisco, CA",
        email="o.brown@company.com",
        gender="Female"
    ))
    
    manager_backend.add_subordinate(Employee(
        name="Nathan Campbell",
        designation="Senior Backend Developer",
        salary=115000,
        age=33,
        years_of_service=6,
        location="Austin, TX",
        email="n.campbell@company.com",
        gender="Male"
    ))
    
    manager_backend.add_subordinate(Employee(
        name="Zoe Phillips",
        designation="Backend Developer",
        salary=95000,
        age=27,
        years_of_service=2,
        location="Austin, TX",
        email="z.phillips@company.com",
        gender="Female"
    ))
    
    # HR team employees
    manager_recruitment.add_subordinate(Employee(
        name="Marcus Johnson",
        designation="Senior Recruiter",
        salary=78000,
        age=35,
        years_of_service=5,
        location="New York, NY",
        email="m.johnson@company.com",
        gender="Male"
    ))
    
    manager_recruitment.add_subordinate(Employee(
        name="Hannah Wright",
        designation="Recruiter",
        salary=60000,
        age=25,
        years_of_service=1,
        location="New York, NY",
        email="h.wright@company.com",
        gender="Female"
    ))
    
    return president

# Example usage
if __name__ == "__main__":
    organization = create_org_structure()
    
    print("Complete Organization Structure:")
    organization.display()
    
    print("\nTotal number of employees:", organization.get_total_employees())
    
    # Find and display information about a specific employee
    emp = organization.find_employee("Alicia Rodriguez")
    if emp:
        print("\nFound employee:")
        emp.display()
    
    # Find and display all employees at a specific location
    print("\nEmployees in San Francisco:")
    def find_by_location(employee, location):
        found = []
        if employee.location == location:
            found.append(employee)
        
        for subordinate in employee.subordinates:
            found.extend(find_by_location(subordinate, location))
        
        return found
    
    sf_employees = find_by_location(organization, "San Francisco, CA")
    for emp in sf_employees:
        print(f"- {emp.name}, {emp.designation}, {emp.gender}")
    
    # Find and display employees by gender
    print("\nFemale employees in the organization:")
    def find_by_gender(employee, gender):
        found = []
        if employee.gender == gender:
            found.append(employee)
        
        for subordinate in employee.subordinates:
            found.extend(find_by_gender(subordinate, gender))
        
        return found
    
    female_employees = find_by_gender(organization, "Female")
    for emp in female_employees:
        print(f"- {emp.name}, {emp.designation}, {emp.location}")