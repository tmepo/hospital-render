
create table if not EXISTS doctors(
doctor_id serial primary key,
first_name varchar(200),
last_name varchar(200),
specialization varchar(200),
phone varchar(10),
email varchar(100),
address varchar(100)
);

create table if not EXISTS patients(
patient_id serial primary key,
first_name varchar(100),
last_name varchar(100),
age int,
gender varchar(10),
phone varchar(10),
email varchar(50),
address varchar(100)
);


create table if not EXISTS services(
service_id serial primary key,
patient_id int,
service_name varchar(100),
service_description text,
service_total numeric(10,3),
foreign key(patient_id) references patients(patient_id) on delete cascade

);


CREATE TABLE IF NOT EXISTS appoinments (
    id SERIAL PRIMARY KEY,
    appointment_date DATE,
    appointment_time TIME CHECK (appointment_time BETWEEN '09:00:00' AND '17:00:00'),
    service_id INT,
    doctor_id INT,
    patient_id INT,
    FOREIGN KEY (service_id) REFERENCES services (service_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id) ON DELETE CASCADE
);

-- Create the trigger function to check appointment date
CREATE OR REPLACE FUNCTION check_appointment_date()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.appointment_date < CURRENT_DATE THEN
        RAISE EXCEPTION 'Appointment date must be today or in the future.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER trg_check_appointment_date
BEFORE INSERT OR UPDATE ON appoinments
FOR EACH ROW
EXECUTE FUNCTION check_appointment_date();



create table if not EXISTS billing(
billing_id serial primary key,
total_amount numeric(10,3),
payment_status varchar(100),
payment_date date,
patient_id int,
appointment_id int,
foreign key(patient_id) references patients(patient_id) on delete cascade,
foreign key(appointment_id) references appoinments(id) on delete cascade
);
