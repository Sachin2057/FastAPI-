from fastapi import FastAPI, HTTPException, Depends
from .models import Employee, EmployeeData
from .database import SessionLocal, engine, Base
from sqlalchemy.orm import Session


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/employees/")
def get_employees(db: Session = Depends(get_db)):
    """
    Get all tehe employee

    Parameters
    ----------
    db : Session, optional
        databse session, by default Depends(get_db)

    Returns
    -------
        All the employee info in json
    """
    return db.query(Employee).all()


@app.get("/employee/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.post("/employees/")
def post_employeess(employee: EmployeeData, db: Session = Depends(get_db)):
    new_employee = Employee(
        name=f"{employee.first_name} {employee.middle_name} {employee.last_name}", department=employee.department)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted"}


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeData, db: Session = Depends(get_db)):
    existing_employee = db.query(Employee).filter(
        Employee.id == employee_id).first()
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing_employee.name = f"{employee.first_name} {employee.middle_name} {employee.last_name}"
    existing_employee.department = employee.department
    db.commit()
    db.refresh(existing_employee)
    return existing_employee
