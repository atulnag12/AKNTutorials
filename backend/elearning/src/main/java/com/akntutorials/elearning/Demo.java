package com.akntutorials.elearning;
import java.time.LocalDate;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Objects;

class Employee {
    private String name;
    private String department;
    private double salary;
    private LocalDate joiningDate;

    // Constructor
    public Employee(String name, String department, double salary, LocalDate joiningDate) {
        this.name = name;
        this.department = department;
        this.salary = salary;
        this.joiningDate = joiningDate;
    }

    // Getters
    public String getName() {
        return name;
    }

    public String getDepartment() {
        return department;
    }

    public double getSalary() {
        return salary;
    }

    public LocalDate getJoiningDate() {
        return joiningDate;
    }

    // Setters
    public void setName(String name) {
        this.name = name;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public void setSalary(double salary) {
        this.salary = salary;
    }

    public void setJoiningDate(LocalDate joiningDate) {
        this.joiningDate = joiningDate;
    }

    // toString for easy display
    @Override
    public String toString() {
        return "Employee{" +
                "name='" + name + '\'' +
                ", department='" + department + '\'' +
                ", salary=" + salary +
                ", joiningDate=" + joiningDate +
                '}';
    }

    // equals and hashCode for proper object comparison
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Employee employee = (Employee) o;
        return Double.compare(employee.salary, salary) == 0 &&
                Objects.equals(name, employee.name) &&
                Objects.equals(department, employee.department) &&
                Objects.equals(joiningDate, employee.joiningDate);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, department, salary, joiningDate);
    }
}
public class Demo {
    public static void main(String[] args) {
        List<Employee> employees = Arrays.asList(
                new Employee("John Doe", "IT", 85000, LocalDate.of(2020, 1, 15)),
                new Employee("Jane Smith", "IT", 92000, LocalDate.of(2019, 3, 10)),
                new Employee("Bob Johnson", "HR", 65000, LocalDate.of(2021, 5, 20)),
                new Employee("Alice Brown", "HR", 78000, LocalDate.of(2018, 7, 8)),
                new Employee("Charlie Davis", "Finance", 95000, LocalDate.of(2017, 11, 12)),
                new Employee("Diana Wilson", "Finance", 95000, LocalDate.of(2016, 9, 5)),  // Same salary, earlier date
                new Employee("Eve Miller", "Marketing", 55000, LocalDate.of(2022, 2, 1)),   // Below 75k threshold
                new Employee("Frank Garcia", "Marketing", 80000, LocalDate.of(2019, 6, 15))
        );
        HashMap<String,Employee> answer=new HashMap<>();
        for(Employee e:employees){
            if(answer.containsKey(e.getDepartment())){
                double salary=answer.get(e.getDepartment()).getSalary();
                if(e.getSalary()>salary){
                    answer.put(e.getDepartment(),e);
                }
            }
            else {
                answer.put(e.getDepartment(),e);
            }
        }
        System.out.println(answer);
    }
}
