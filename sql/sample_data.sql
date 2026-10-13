USE employee_management;
INSERT INTO employees (employee_code,name,email,department,joining_date) VALUES
('EMP001','Arun Kumar','arun@example.com','Engineering','2026-01-15'),
('EMP002','Meera S','meera@example.com','Analytics','2026-02-01');

INSERT INTO attendance (employee_id,attendance_date,status,check_in,check_out) VALUES
(1,'2026-10-12','PRESENT','09:10:00','18:05:00'),
(2,'2026-10-12','LEAVE',NULL,NULL);
