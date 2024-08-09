from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime, time
from django.contrib import messages



def fetch_all_as_dict(cursor):
    "Return all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
def error_404(request,exception):
    return render(request,'hospital/404_error.html')

def execute_sql(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        connection.commit()
def index(request):
    query = """
    SELECT id as patient_id, first_name, last_name, age, email, phone_number, address, gender
    FROM patient
    ORDER BY id ASC
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        patients = fetch_all_as_dict(cursor)  # Assuming fetch_all_as_dict is implemented correctly
    
    # For debugging or validation, print each patient
    for patient in patients:
        print(patient)
    
    return render(request, 'hospital/show_patients.html', {'patients': patients})
@login_required
def add_patient(request):
    if request.method == 'POST':
        patient_id=request.POST.get('patient_id')
        first_name = request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        address=request.POST.get('address')


        
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO patients (patient_id,first_name, last_name, age, gender,phone,email,address) VALUES (%s,%s,%s,%s,%s, %s,%s, %s)",
                [patient_id,first_name, last_name, age, gender,phone,email,address]
            )
        
        return redirect('index')
    
    return render(request, 'hospital/add_patients.html')


@login_required
def update_patient(request, patient_id):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        
        query = '''
        UPDATE patients SET first_name=%s, last_name=%s, age=%s, phone=%s, address=%s, email=%s, gender=%s
        WHERE patient_id=%s
        '''
        params = [first_name, last_name, age, phone, address, email, gender, patient_id]
        execute_sql(query, params)
        
        return redirect('index')
    
    else:
        query = 'SELECT patient_id, first_name, last_name, age, gender, address, phone, email FROM patients WHERE patient_id=%s'
        with connection.cursor() as cursor:
            cursor.execute(query, [patient_id])
            patient = cursor.fetchone()
        
        if patient is None:
            return redirect('index')  # Or raise Http404("Patient not found")
        
        context = {
            'patient_id': patient[0],
            'first_name': patient[1],
            'last_name': patient[2],
            'age': patient[3],
            'gender': patient[4],
            'address': patient[5],
            'phone': patient[6],
            'email': patient[7],
        }
        
        return render(request, 'hospital/edit_patients.html', {'patient': context})
    
@login_required
def delete_patient(request, patient_id):
    query = 'DELETE FROM patients WHERE patient_id=%s'
    execute_sql(query, [patient_id])
    return redirect('index')
# --------------------------------------------------------------------------------------------------------------
@login_required
def add_doctor(request):
    if request.method == 'POST':
        doctor_id=request.POST.get('doctor_id')
        first_name = request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        specialization=request.POST.get('specialization')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        address=request.POST.get('address')


        
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO doctors (doctor_id,first_name, last_name, specialization,phone,email,address) VALUES (%s,%s,%s,%s,%s, %s,%s)",
                [doctor_id,first_name, last_name, specialization,phone,email,address]
            )
        
        return redirect('show_doctors')
    
    return render(request, 'hospital/add_doctors.html')

@login_required
def update_doctor(request, doctor_id):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        specialization = request.POST.get('specialization')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        
        query = '''
        UPDATE doctors SET first_name=%s, last_name=%s, specialization=%s, phone=%s, address=%s, email=%s
        WHERE doctor_id=%s
        '''
        params = [first_name, last_name, specialization, phone, address, email,doctor_id]
        execute_sql(query, params)
        
        return redirect('show_doctors')
    
    else:
        query = 'SELECT doctor_id, first_name, last_name, specialization, address, phone, email FROM doctors WHERE doctor_id=%s'
        with connection.cursor() as cursor:
            cursor.execute(query, [doctor_id])
            doctor = cursor.fetchone()
        
        if doctor is None:
            return redirect('show_doctors')  # Or raise Http404("doctor not found")
        
        context = {
            'doctor_id': doctor[0],
            'first_name': doctor[1],
            'last_name': doctor[2],
            'specialization': doctor[3],
            'address': doctor[4],
            'phone': doctor[5],
            'email': doctor[6],
        }
        
        return render(request, 'hospital/edit_doctors.html', {'doctor': context})

@login_required        
def delete_doctor(request, doctor_id):
    query = 'DELETE FROM doctors WHERE doctor_id=%s'
    execute_sql(query, [doctor_id])
    return redirect('show_doctors')
# --------------------------------------------------------------------------------------------------------------




@login_required
def add_appointment(request):
    if request.method == "POST":
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        service_id = request.POST.get('service_id')
        doctor_id = request.POST.get('doctor_id')
        patient_id = request.POST.get('patient_id')

        query = '''
        INSERT INTO appoinments (appointment_date, appointment_time, service_id, doctor_id, patient_id)
        VALUES (%s, %s, %s, %s, %s)
        '''
        params = [appointment_date, appointment_time, service_id, doctor_id, patient_id]
        execute_sql(query, params)
        
        return redirect('index')  # Redirect to an appropriate page or a list of appointments
    
    return render(request, 'hospital/add_appointment.html')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connection

@login_required
def add_service(request):
    if request.method == "POST":
        patient_id = request.POST.get('patient_id')  # Get selected patient ID
        service_name = request.POST.get('service_name')
        service_description = request.POST.get('service_description')
        service_total = request.POST.get('service_total')

        query = '''
        INSERT INTO services (patient_id, service_name, service_description, service_total)
        VALUES (%s, %s, %s, %s)
        '''
        params = [patient_id, service_name, service_description, service_total]
        
        with connection.cursor() as cursor:
            cursor.execute(query, params)
        
        return redirect('index')  # Redirect to an appropriate page or a list of services
    
    else:
        # Fetch patients for the form
        patient_query = 'SELECT patient_id, first_name, last_name FROM patients'
        
        with connection.cursor() as cursor:
            cursor.execute(patient_query)
            patients = cursor.fetchall()
        
        context = {
            'patients': [{'patient_id': p[0], 'first_name': p[1], 'last_name': p[2]} for p in patients],
        }
        
        return render(request, 'hospital/add_service.html', context)



@login_required
def update_service(request, service_id):
    if request.method == "POST":
        patient_id = request.POST.get('patient_id')
        service_name = request.POST.get('service_name')
        service_description = request.POST.get('service_description')
        service_total = request.POST.get('service_total')

        query = '''
        UPDATE services
        SET patient_id=%s, service_name=%s, service_description=%s, service_total=%s
        WHERE service_id=%s
        '''
        params = [patient_id, service_name, service_description, service_total, service_id]
        execute_sql(query, params)
        
        return redirect('index')  # Redirect to an appropriate page or a list of services

    else:
        query = 'SELECT service_id, patient_id, service_name, service_description, service_total FROM services WHERE service_id=%s'
        with connection.cursor() as cursor:
            cursor.execute(query, [service_id])
            service = cursor.fetchone()
        
        if service is None:
            return redirect('index')  # Or raise Http404("Service not found")

        context = {
            'service_id': service[0],
            'patient_id': service[1],
            'service_name': service[2],
            'service_description': service[3],
            'service_total': service[4],
        }
        
        return render(request, 'hospital/edit_service.html', {'service': context})
    
@login_required
def delete_service(request, service_id):
    query = 'DELETE FROM services WHERE service_id=%s'
    with connection.cursor() as cursor:
        cursor.execute(query, [service_id])
    
    return redirect('index')  # Redirect to an appropriate page or a list of services

# ----------------------------------------------------------------------------------------------------------------------------


@login_required
def add_billing(request):
    if request.method == "POST":
        total_amount = request.POST.get('total_amount')
        payment_status = request.POST.get('payment_status')
        payment_date = request.POST.get('payment_date')
        patient_id = request.POST.get('patient_id')
        appointment_id = request.POST.get('appointment_id')

        query = '''
        INSERT INTO billing (total_amount, payment_status, payment_date, patient_id, appointment_id)
        VALUES (%s, %s, %s, %s, %s)
        '''
        params = [total_amount, payment_status, payment_date, patient_id, appointment_id]
        execute_sql(query, params)
        
        return redirect('index')  # Redirect to an appropriate page or a list of billing records
    
    else:
        patient_query = '''
        SELECT p.patient_id, p.first_name, p.last_name, s.service_total
        FROM patients p
        JOIN services s ON p.patient_id = s.patient_id
    '''
    
    with connection.cursor() as cursor:
        cursor.execute(patient_query)
        patients = cursor.fetchall()
    
    context = {
        'patients': [{'patient_id': p[0], 'first_name': p[1], 'last_name': p[2], 'service_total': p[3]} for p in patients],
    }

    return render(request, 'hospital/add_billing.html', context)




@login_required
def update_billing(request, billing_id):
    if request.method == "POST":
        total_amount = request.POST.get('total_amount')
        payment_status = request.POST.get('payment_status')
        payment_date = request.POST.get('payment_date')
        patient_id = request.POST.get('patient_id')
        appointment_id = request.POST.get('appointment_id')

        query = '''
        UPDATE billing
        SET total_amount=%s, payment_status=%s, payment_date=%s, patient_id=%s, appointment_id=%s
        WHERE billing_id=%s
        '''
        params = [total_amount, payment_status, payment_date, patient_id, appointment_id, billing_id]
        execute_sql(query, params)
        
        return redirect('index')  # Redirect to an appropriate page or a list of billing records

    else:
        query = 'SELECT billing_id, total_amount, payment_status, payment_date, patient_id, appointment_id FROM billing WHERE billing_id=%s'
        with connection.cursor() as cursor:
            cursor.execute(query, [billing_id])
            billing = cursor.fetchone()
        
        if billing is None:
            return redirect('index')  # Or raise Http404("Billing record not found")

        context = {
            'billing_id': billing[0],
            'total_amount': billing[1],
            'payment_status': billing[2],
            'payment_date': billing[3],
            'patient_id': billing[4],
            'appointment_id': billing[5],
        }
        
        return render(request, 'hospital/edit_billing.html', {'billing': context})
    
@login_required
def delete_billing(request, billing_id):
    query = 'DELETE FROM billing WHERE billing_id=%s'
    with connection.cursor() as cursor:
        cursor.execute(query, [billing_id])
    
    return redirect('view_billing')  # Redirect to an appropriate page or a list of billing records

# ----------------------------------------------------------------------------------------------------------


def make_appointment(request):
    if request.method == "POST":
        doctor_id = request.POST.get('doctor_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        
        # Insert new patient
        patient_query = '''
        INSERT INTO patients (first_name, last_name, age, gender, phone, email, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING patient_id
        '''
        patient_params = [first_name, last_name, age, gender, phone, email, address]
        with connection.cursor() as cursor:
            cursor.execute(patient_query, patient_params)
            patient_id = cursor.fetchone()[0]
        
        # Create a new appointment
        appointment_query = '''
        INSERT INTO appoinments (appointment_date, appointment_time, doctor_id, patient_id)
        VALUES (%s, %s, %s, %s) RETURNING id
        '''
        appointment_params = [appointment_date, appointment_time, doctor_id, patient_id]
        with connection.cursor() as cursor:
            cursor.execute(appointment_query, appointment_params)
            appointment_id = cursor.fetchone()[0]
            
            messages.success(request, "Appointment successfully booked!")
        
        return redirect('make_appointment')  # Redirect to an appropriate page or appointment confirmation page

    else:
        # Fetch departments and doctors for the form
        # departments_query = 'SELECT id, name FROM departments'
        doctors_query = 'SELECT doctor_id, first_name, last_name , specialization FROM doctors'
        
        with connection.cursor() as cursor:
            # cursor.execute(departments_query)
            # departments = cursor.fetchall()
            
            cursor.execute(doctors_query)
            doctors = cursor.fetchall()
        
        context = {
            # 'departments': [{'id': d[0], 'name': d[1]} for d in departments],
            'doctors': [{'doctor_id': d[0], 'first_name': d[1], 'last_name': d[2] , 'specialization': d[3]} for d in doctors],
        }
        
        return render(request, 'hospital/make_appointment.html', context)




@login_required
def update_appointment(request, appointment_id):
    # Fetch the existing appointment details
    appointment_query = '''
    SELECT a.id, a.appointment_date, a.appointment_time, a.service_id, a.doctor_id, a.patient_id,
           p.first_name as patient_first_name, p.last_name as patient_last_name, p.age as patient_age,
           p.gender as patient_gender, p.phone as patient_phone, p.email as patient_email, p.address as patient_address
    FROM appoinments a
    JOIN patients p ON a.patient_id = p.patient_id
    WHERE a.id = %s
    '''
    
    with connection.cursor() as cursor:
        cursor.execute(appointment_query, [appointment_id])
        appointment = cursor.fetchone()
    
    if not appointment:
        return redirect('viewappointment')  # Redirect if the appointment does not exist

    # Fetch doctors for the form
    doctors_query = 'SELECT doctor_id, first_name, last_name FROM doctors'
    
    with connection.cursor() as cursor:
        cursor.execute(doctors_query)
        doctors = cursor.fetchall()
    
    if request.method == "POST":
        doctor_id = request.POST.get('doctor_id')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        service_id = request.POST.get('service_id')
        patient_first_name = request.POST.get('patient_first_name')
        patient_last_name = request.POST.get('patient_last_name')
        patient_age = request.POST.get('patient_age')
        patient_gender = request.POST.get('patient_gender')
        patient_phone = request.POST.get('patient_phone')
        patient_email = request.POST.get('patient_email')
        patient_address = request.POST.get('patient_address')
        
        # Update the appointment
        update_appointment_query = '''
        UPDATE appoinments
        SET appointment_date = %s, appointment_time = %s, doctor_id = %s, service_id = %s
        WHERE id = %s
        '''
        update_params = [appointment_date, appointment_time, doctor_id, service_id, appointment_id]
        
        with connection.cursor() as cursor:
            cursor.execute(update_appointment_query, update_params)
        
        # Update the patient details
        update_patient_query = '''
        UPDATE patients
        SET first_name = %s, last_name = %s, age = %s, gender = %s, phone = %s, email = %s, address = %s
        WHERE patient_id = (
            SELECT patient_id FROM appoinments WHERE id = %s
        )
        '''
        update_patient_params = [patient_first_name, patient_last_name, patient_age, patient_gender, patient_phone, patient_email, patient_address, appointment_id]
        
        with connection.cursor() as cursor:
            cursor.execute(update_patient_query, update_patient_params)
        
        return redirect('viewappointment')  # Redirect to the appointments list after update

    context = {
        'appointment': {
            'appointment_id': appointment[0],
            'appointment_date': appointment[1],
            'appointment_time': appointment[2],
            'service_id': appointment[3],
            'doctor_id': appointment[4],
            'patient_id': appointment[5],
            'patient_first_name': appointment[6],
            'patient_last_name': appointment[7],
            'patient_age': appointment[8],
            'patient_gender': appointment[9],
            'patient_phone': appointment[10],
            'patient_email': appointment[11],
            'patient_address': appointment[12],
        },
        'doctors': [{'doctor_id': d[0], 'first_name': d[1], 'last_name': d[2]} for d in doctors],
    }
    
    return render(request, 'hospital/edit_appointment.html', context)






@login_required
def view_appointments(request):
    # Fetch all appointments along with their related doctor and patient information
    appointments_query = '''
    SELECT a.id, a.appointment_date, a.appointment_time,  a.patient_id,  concat(p.first_name,' ',p.last_name) as "patient name", a.service_id, a.doctor_id,
    concat(d.first_name,' ',d.last_name) "doctor name"

     FROM appoinments a
    JOIN doctors d ON a.doctor_id = d.doctor_id
    JOIN patients p ON a.patient_id = p.patient_id
    '''
    
    with connection.cursor() as cursor:
        cursor.execute(appointments_query)
        appointments = cursor.fetchall()
    
    context = {
        'appointments': appointments
    }
    
    return render(request, 'hospital/view_appointments.html', context)

@login_required
def delete_appointment(request, appointment_id):
    query = 'DELETE FROM appoinments WHERE id=%s'
    with connection.cursor() as cursor:
        cursor.execute(query, [appointment_id])
    
    return redirect('viewappointment')  # Redirect to an appropriate page or a list of appointments


@login_required
def index(request):
    query = 'SELECT * FROM patients'
    with connection.cursor() as cursor:
        cursor.execute(query)
        patients = cursor.fetchall()
    return render(request, 'hospital/show_patients.html', {'patients': patients})

@login_required
def view_billing(request):
    query = '''select b.billing_id,  p.first_name , p.last_name , s.service_name , s.service_description,  b.total_amount , b.payment_status
    from patients p
    inner join services s on s.patient_id = p.patient_id 
    inner join billing b on b.patient_id = p.patient_id 
    
    '''
    with connection.cursor() as cursor:
        cursor.execute(query)
        combined_list = cursor.fetchall()
    
    context = {
        'combined_list': [
            {   'billing_id': c[0],
                'patient_name': f"{c[1]} {c[2]}",
                'service_name': f"{c[3]}",
                'service_description' : f"{c[4]}",
                'total_amount': f"{c[5]}",
                'payment_status': f"{c[6]}",
            } for c in combined_list
        ],
    }
    
    return render(request, 'hospital/view_billing.html', context)

@login_required
def show_doctors(request):
    query='Select * from doctors'
    with connection.cursor() as cursor:
        cursor.execute(query)
        doctors=cursor.fetchall()
    return render(request, 'hospital/show_doctors.html',{'doctors':doctors})



def home(request):

    return render(request,"hospital/home.html")

def login_user(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.success(request,('Hey There is a problem with logging in. Try again..'))
            return redirect('login')
    else:
        return render(request,'registration/login.html')
    

def logout_user(request):
    logout(request)
    messages.success(request,('You are logged out!! Please log in.'))
    return redirect('login')

def contact(request):
    return render(request,'hospital/contact.html')

def about(request):
    return render(request,'hospital/aboutus.html')