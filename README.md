# Hospital Management System

This is a Hospital Management System built with Django for the backend and PostgreSQL as the database. The frontend is developed using HTML, CSS, and JavaScript.

[![Website Demo](https://img.shields.io/badge/Website-Demo-brightgreen)](https://www.loom.com/share/4008a338fe3a4aefac4e8c6584af64da?sid=67cfc3f4-631c-4395-a766-e49300e13ba1)
[![Website](https://img.shields.io/badge/Website-Live-blue)](https://hospital-render.onrender.com/)

## Features

- **Patient Management:** Add, update, view, and delete patient records.
- **Appointment Scheduling:** Manage appointments with doctors.
- **Doctor Management:**  Add, update, view, and delete doctor records.
- **Billing System:** Generate and manage billing for patients.
- **Service Management:** Track and manage different services offered by the hospital.
- **Authentication:** Admin authentication and authorization.

## Technologies Used

### Backend:
- **Django:** A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
- **PostgreSQL:** A powerful, open-source object-relational database system.

### Frontend:
- **HTML:** For structuring the web pages.
- **CSS:** For styling the web pages.
- **JavaScript:** For interactivity and dynamic content on the client-side.

### Deployment
- **Render:** Cloud platform used for deploying the application.

## Setup Instructions

### Prerequisites:
- Python 3.x
- PostgreSQL
- Django

### Installation:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/tmepo/hospital-management.git
    cd hospital-management
    ```

2. **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up PostgreSQL Database:**
    - Create a PostgreSQL database for the project.
    - Update the `DATABASES` setting in `settings.py` with your PostgreSQL credentials.

5. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

8. **Access the application:**
    Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage

- **Admin Panel:** Accessible at `/admin`, where you can manage all the data in the system.
- **User Interface:** Simple and user-friendly design for managing hospital operations.

## Contributing

If you'd like to contribute to this project, feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License.

## Contact

If you have any questions or feedback, feel free to reach out to one of the below email:
-> prasishabde@gmail.com
-> shreeroshan60@gmail.com
-> panthisandesh754@gmail.com
