from fastapi import APIRouter, Depends, Request, Form
from ..dependencies.database import get_db_connection
from ..models.common import ApiResponse
from ..models.user import UserRequest, UserListResponse, UserResponse
from fastapi.responses import HTMLResponse, RedirectResponse
from icecream import ic
from fastapi.templating import Jinja2Templates
from datetime import datetime
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from ..utility.functions import format_errors

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

templates = Jinja2Templates(directory="src/pages")
current_year = datetime.now().year

# @router.get("", response_model=ApiResponse[UserListResponse])
# async def list_users(db: tuple = Depends(get_db_connection)):
#     connection, cursor = db
#     cursor.execute("""
#         SELECT users.id, users.enrollment_number, users.firstname, users.lastname, 
#             users.email, users.password, users.contact, users.cuatri, 
#             roles.title AS role
#         FROM users
#         JOIN roles ON users.role_id = roles.id
#     """)
#     users = cursor.fetchall()
#     ic(users)
    
#     return {
#         "status": 200,
#         "message": "Users listed successfully",
#         "data": {
#             "users": users,
#             "items_count": len(users)
#         }
    
#     }
    
@router.get("", response_class=HTMLResponse)
async def list_users(request: Request, db: tuple = Depends(get_db_connection)):
    connection, cursor = db
    cursor.execute("""
        SELECT users.id, users.enrollment_number, users.firstname, users.lastname, 
            users.email, users.password, users.contact, users.cuatri, 
            roles.title AS role
        FROM users
        JOIN roles ON users.role_id = roles.id
    """)
    users = cursor.fetchall()
    
    return templates.TemplateResponse("users/index.html.jinja", {"request": request, "users": users})
    
# @router.post('', response_model=ApiResponse[UserResponse])
# async def create_user(user: UserRequest, db: tuple = Depends(get_db_connection)):
#     connection, cursor = db
#     cursor.execute(
#         "INSERT INTO users (firstname, lastname, enrollment_number, email, password, contact, cuatri, role_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
#         (user.firstname, user.lastname, user.enrollment_number, user.email, user.password, user.contact, user.cuatri, user.role_id)
#     )
#     cursor.execute("SELECT title FROM roles WHERE id = %s", (user.role_id,))
#     role = cursor.fetchone()
#     connection.commit()
    
#     response = {
#         "id": cursor.lastrowid,
#         "role": role["title"],
#         "firstname": user.firstname,
#         "lastname": user.lastname,
#         "enrollment_number": user.enrollment_number,
#         "email": user.email,
#         "contact": user.contact,
#         "cuatri": user.cuatri
#     }
#     ic(response)
    
#     return {
#         "status": 200,
#         "message": "User created successfully",
#         "data": response
#     }

@router.get("/create", response_class=HTMLResponse)
async def create_user(request: Request, db: tuple = Depends(get_db_connection)):
    connection, cursor = db
    cursor.execute("SELECT * FROM roles")
    roles = cursor.fetchall()
    return templates.TemplateResponse(request=request, name="users/create.html.jinja", context={"roles": roles, "current_year": current_year})


@router.post('', response_class=HTMLResponse)
async def save_user(
    request: Request,
    db: tuple = Depends(get_db_connection)):
    
    try:     
        form_data = await request.form()
        form_dict = {key: value for key, value in form_data.items()}
        connection, cursor = db
        
        form_data = UserRequest(**form_dict)
        
        cursor.execute(
            "INSERT INTO users (firstname, lastname, enrollment_number, email, password, contact, cuatri, role_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (form_data.firstname, form_data.lastname, form_data.enrollment_number, form_data.email, form_data.password, form_data.contact, form_data.cuatri, form_data.role_id)
        )
        connection.commit()
        return RedirectResponse(url="/users", status_code=303)
    
    except ValidationError as e:
        cursor.execute("SELECT * FROM roles")
        roles = cursor.fetchall()
                
        error_messages = format_errors(e.errors(), UserRequest)
            
        return templates.TemplateResponse(request=request, name="users/create.html.jinja", context={"errors": error_messages, "roles": roles, "current_year": current_year})
  
    
# @router.get("/{user_id}", response_model=ApiResponse[UserResponse])
# async def get_user(user_id: int, db: tuple = Depends(get_db_connection)):
#     connection, cursor = db
#     cursor.execute(
#         "SELECT users.id, users.enrollment_number, users.firstname, users.lastname, users.email, users.contact, users.cuatri, roles.title AS role FROM users JOIN roles ON users.role_id = roles.id WHERE users.id = %s",
#         (user_id,)
#     )
#     user = cursor.fetchone()
#     ic(user)
    
#     return {
#         "status": 200,
#         "message": "User retrieved successfully",
#         "data": user
#     }
    
    
@router.get("/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int, db: tuple = Depends(get_db_connection)):
    connection, cursor = db
    cursor.execute(
        "SELECT users.id, users.enrollment_number, users.firstname, users.lastname, users.email, users.contact, users.cuatri, roles.title AS role FROM users JOIN roles ON users.role_id = roles.id WHERE users.id = %s",
        (user_id,)
    )
    user = cursor.fetchone()
    
    return templates.TemplateResponse(request=request, name="users/details.html.jinja", context={"user": user, "current_year": current_year})

# @router.put("/{user_id}", response_model=ApiResponse[UserResponse])
# async def update_user(user_id: int, user: UserRequest, db: tuple = Depends(get_db_connection)):
#     connection, cursor = db
#     cursor.execute(
#         "UPDATE users SET firstname = %s, lastname = %s, enrollment_number = %s, email = %s, password = %s, contact = %s, cuatri = %s, role_id = %s WHERE id = %s",
#         (user.firstname, user.lastname, user.enrollment_number, user.email, user.password, user.contact, user.cuatri, user.role_id, user_id)
#     )
#     cursor.execute("SELECT title FROM roles WHERE id = %s", (user.role_id,))
#     role = cursor.fetchone()
#     connection.commit()
    
#     response = {
#         "id": user_id,
#         "role": role["title"],
#         "firstname": user.firstname,
#         "lastname": user.lastname,
#         "enrollment_number": user.enrollment_number,
#         "email": user.email,
#         "contact": user.contact,
#         "cuatri": user.cuatri
#     }
#     ic(response)
    
#     return {
#         "status": 200,
#         "message": "User updated successfully",
#         "data": response
#     }

@router.get("/{user_id}/edit", response_class=HTMLResponse)
async def edit_user(request: Request, user_id: int, db: tuple = Depends(get_db_connection)):
    connection, cursor = db
    
    cursor.execute(
        "SELECT users.id, users.enrollment_number, users.firstname, users.lastname, users.email, users.contact, users.cuatri, roles.title AS role FROM users JOIN roles ON users.role_id = roles.id WHERE users.id = %s",
        (user_id,)
    )
    user = cursor.fetchone()
        
    cursor.execute("SELECT * FROM roles")
    roles = cursor.fetchall()
    
    return templates.TemplateResponse(request=request, name="users/edit.html.jinja", context={"user": user, "roles": roles, "current_year": current_year})

@router.post("/{user_id}", response_class=HTMLResponse)
async def update_user(request: Request, user_id: int, db: tuple = Depends(get_db_connection)):
    try:
        connection, cursor = db
        
        form_data = await request.form()
        form_dict = {key: value for key, value in form_data.items()}
        connection, cursor = db
        
        form_data = UserRequest(**form_dict)
        
        cursor.execute(
            "UPDATE users SET firstname = %s, lastname = %s, enrollment_number = %s, email = %s, password = %s, contact = %s, cuatri = %s, role_id = %s WHERE id = %s",
            (form_data.firstname, form_data.lastname, form_data.enrollment_number, form_data.email, form_data.password, form_data.contact, form_data.cuatri, form_data.role_id, user_id)
        )
        connection.commit()
    
        return RedirectResponse(url="/users", status_code=303)
    except ValidationError as e:
        cursor.execute(
            "SELECT users.id, users.enrollment_number, users.firstname, users.lastname, users.email, users.contact, users.cuatri, roles.title AS role FROM users JOIN roles ON users.role_id = roles.id WHERE users.id = %s",
            (user_id,)
        )
        user = cursor.fetchone()
        cursor.execute("SELECT * FROM roles")
        roles = cursor.fetchall()
        error_messages = format_errors(e.errors(), UserRequest)
    
        return templates.TemplateResponse(request=request, name="users/edit.html.jinja", context={"errors": error_messages, "user": user, "roles": roles, "current_year": current_year})
    
# @router.delete("/{user_id}", response_model=ApiResponse[UserResponse])
# async def delete_user(user_id: int, db: tuple = Depends(get_db_connection)):
#     connection, cursor = db
#     cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
#     user = cursor.fetchone()
#     cursor.execute("SELECT title FROM roles WHERE id = %s", (user["role_id"],))
#     role = cursor.fetchone()["title"]
    
    
#     response = {
#         "id": user_id,
#         "role": role,
#         "firstname": user["firstname"],
#         "lastname": user["lastname"],
#         "enrollment_number": user["enrollment_number"],
#         "email": user["email"],
#         "contact": user["contact"],
#         "cuatri": user["cuatri"]
#     }
    
    
#     cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
#     connection.commit()
    
#     return {
#         "status": 200,
#         "message": "User deleted successfully",
#         "data": response
#     }


@router.post("/{user_id}/delete", response_class=HTMLResponse)
async def delete_user(user_id: int, method: str = Form(...), db: tuple = Depends(get_db_connection)):
    if method.lower() != "delete":
        return {"status": 400, "message": "Invalid request method"}

    connection, cursor = db
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        return {"status": 404, "message": "User not found"}

    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    connection.commit()

    return RedirectResponse(url="/users", status_code=303)



@router.post("/handle_validation_error", response_class=HTMLResponse, include_in_schema=False)
async def handle_validation_error(request: Request, exc):
    connection, cursor = await get_db_connection()
    cursor.execute("SELECT * FROM roles")
    roles = cursor.fetchall()
    
    return templates.TemplateResponse(
        "users/create.html.jinja",
        {
            "request": request,
            "errors": exc.errors(),
            "roles": roles,
            "current_year": current_year
        },
        status_code=400
    )