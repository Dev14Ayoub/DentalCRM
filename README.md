➡️ A dental clinic website built with `Django` and `Django REST` frameworks, using the TDD methodology with `Django` and `Selenium` tests, and the `PostgreSQL` database.

## ⚙️ Setup 
To run the project in a local environment, follow these steps:

```python -m venv venv; pip install -r requirements.txt; cp .env-example .env; python .\manage.py makemigrations; python .\manage.py migrate```

```python .\manage.py runserver```

Make sure to fill in the new `.env` file.

## 💻 Application Features

❕Home Page and Header
- The `OdontoDj` logo redirects the user to the home page. 
- While not logged in, the user can access the `Services`, `About`, `Login` and `Register` pages.
- When the user logs in, the pages `Schedule`, `Dashboard` and `Logout` are granted access. 

❕Services
- Displays all available treatments and procedures as well as their respective prices. 

❕Register
- The user must provide valid and unique information to register.
- The required fields are `Username`, `First Name`, `Last Name`, `Email`, `CPF` and `Password`.

❕Schedule
- When the user is logged in, displays a scheduler form with all available procedures, dates and times for an appointment.
- If the desired treatment is not found, the user has the option to schedule a custom appointment.
- When a valid appointment form is submitted, an email will be sent to the logged user with a confirmation link.

❕Dashboard
- Displays all the user's appointments and treatment history, with details for each appointment.
- Options to update the user's information and change the password can also be found in the dashboard.

## 🖱️ REST API
#### ➡️ The API was built using `Django REST Framework`, with `JWT` authentication
The `base_url` is `https://odontodj.onrender.com`, and all requests to the API can be called via `base_url` + `API endpoint URL` with the `JWT` authorization headers.

#### ➡️ Swagger documentation endpoints
- JSON view of the API specification at `/swagger.json`
- Swagger-ui view of the API specification at `/swagger/`
- ReDoc view of the API specification at `/redoc/`

❕JWT
- `POST` ➔ `/users/api/token/` ─ Generate `refresh` and `access` authorization tokens.
  - `request`: username, password
- `POST` ➔ `/users/api/token/refresh/` ─ Refresh the access token.
  - `request`: refresh
- `POST` ➔ `/users/api/token/verify/` ─ Verify the access token.
  - `request`: token

❕Users
- `GET` ➔ `/users/api/me/` ─ Retrieve the logged user's information.
- `GET` ➔ `/users/api/<pk>/` ─ [**Staff Only**] Retrieve information about user with id `pk`.
- `GET` ➔ `/users/api/` ─ [**Staff Only**] Retrieve a list of all registered users.
- `PATCH` ➔ `/users/api/<pk>/` ─ [**Staff Only**] Update information of user with id `pk`.
  - `request`: first_name, last_name, password, email, phone_number
- `POST` ➔ `/users/api/` ─ Create a new user.
  - `request`: username, password, first_name, last_name, email, phone_number, cpf
  
❕Schedule and Appointments
- `GET` ➔ `/schedule/api/` ─ Retrieve the logged user's appointments.
- `GET` ➔ `/schedule/api/` ─ [**Staff Only**] Retrieve a list of all upcoming appointments.
- `GET` ➔ `/schedule/api/<pk>/` ─ Retrieve information about the appointment with id `pk`, cannot access another user's appointment.
- `GET` ➔ `/schedule/api/<pk>/` ─ [**Staff Only**] Retrieve information about the appointment with id `pk`.
- `GET` ➔ `/schedule/api/users_appointments/<pk>/` ─ [**Staff Only**] Retrieve a list of all appointments of user with id `pk`.
- `GET` ➔ `/schedule/api/datetime/` ─ [**Staff Only**] Retrieve a list of all available dates and times.
- `GET` ➔ `/schedule/api/appointments/` ─ [**Staff Only**] Retrieve a list of all upcoming appointments dates and times.
- `POST` ➔ `/schedule/api/` ─ Schedule a new appointment for the logged user.
  - `request`: procedure, date, time
- `POST` ➔ `/schedule/api/` ─ [**Staff Only**] Schedule a new appointment for a specific user.
  - `request`: user, procedure, date, time
- `DELETE` ➔ `/schedule/api/<pk>/` ─ Cancel the scheduled appointment with id `pk` for the logged user.
- `DELETE` ➔ `/schedule/api/<pk>/` ─ [**Staff Only**] Cancel the scheduled appointment with id `pk`.


❕Procedures
- `GET` ➔ `/schedule/api/procedure/` ─ Retrieve a list of all available procedures.
- `POST` ➔ `/schedule/api/procedure/` ─ [**Staff Only**] Create a new procedure.
  - `request`: name, name_pt, description, description_pt, price
- `PATCH` ➔ `/schedule/api/procedure/<pk>` ─ [**Staff Only**] Update the information of the procedure with id `pk`.
  - `request`: name, name_pt, description, description_pt, price
- `DELETE` ➔ `/schedule/api/procedure/<pk>` ─ [**Staff Only**] Delete the procedure with id `pk`.


## ✔️ Tests
❕Functional tests using `Selenium` are located in the `/tests` directory, and `Django` unit and integration tests are stored within the `/tests` directory of each individual app folder.
