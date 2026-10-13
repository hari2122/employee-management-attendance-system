from flask import Flask, jsonify, request
from .db import get_connection


def create_app():
    app = Flask(__name__)

    @app.get('/health')
    def health():
        return jsonify({'status': 'ok'})

    @app.get('/api/employees')
    def list_employees():
        conn = get_connection(); cur = conn.cursor(dictionary=True)
        cur.execute('SELECT id, employee_code, name, email, department, joining_date FROM employees ORDER BY id')
        rows = cur.fetchall(); cur.close(); conn.close()
        return jsonify(rows)

    @app.post('/api/employees')
    def create_employee():
        data = request.get_json(silent=True) or {}
        required = ['employee_code', 'name', 'email', 'department']
        if any(not data.get(k) for k in required):
            return jsonify({'error': 'employee_code, name, email and department are required'}), 400
        conn = get_connection(); cur = conn.cursor()
        cur.execute('INSERT INTO employees (employee_code,name,email,department,joining_date) VALUES (%s,%s,%s,%s,%s)',
                    (data['employee_code'], data['name'], data['email'], data['department'], data.get('joining_date')))
        conn.commit(); employee_id = cur.lastrowid; cur.close(); conn.close()
        return jsonify({'id': employee_id, 'message': 'Employee created'}), 201

    @app.put('/api/employees/<int:employee_id>')
    def update_employee(employee_id):
        data = request.get_json(silent=True) or {}
        fields = [k for k in ['name','email','department','joining_date'] if k in data]
        if not fields:
            return jsonify({'error':'No supported fields supplied'}), 400
        sql = 'UPDATE employees SET ' + ', '.join(f'{k}=%s' for k in fields) + ' WHERE id=%s'
        values = [data[k] for k in fields] + [employee_id]
        conn = get_connection(); cur = conn.cursor(); cur.execute(sql, values); conn.commit(); changed = cur.rowcount; cur.close(); conn.close()
        return (jsonify({'message':'Employee updated'}), 200) if changed else (jsonify({'error':'Employee not found'}), 404)

    @app.delete('/api/employees/<int:employee_id>')
    def delete_employee(employee_id):
        conn = get_connection(); cur = conn.cursor(); cur.execute('DELETE FROM employees WHERE id=%s', (employee_id,)); conn.commit(); changed=cur.rowcount; cur.close(); conn.close()
        return (jsonify({'message':'Employee deleted'}),200) if changed else (jsonify({'error':'Employee not found'}),404)

    @app.post('/api/attendance')
    def mark_attendance():
        data = request.get_json(silent=True) or {}
        if not data.get('employee_id') or not data.get('attendance_date') or data.get('status') not in ['PRESENT','ABSENT','LEAVE']:
            return jsonify({'error':'employee_id, attendance_date and status (PRESENT/ABSENT/LEAVE) are required'}),400
        conn=get_connection(); cur=conn.cursor()
        cur.execute('INSERT INTO attendance (employee_id,attendance_date,status,check_in,check_out) VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE status=VALUES(status),check_in=VALUES(check_in),check_out=VALUES(check_out)',
                    (data['employee_id'],data['attendance_date'],data['status'],data.get('check_in'),data.get('check_out')))
        conn.commit(); cur.close(); conn.close(); return jsonify({'message':'Attendance saved'}),201

    @app.get('/api/attendance/<int:employee_id>')
    def attendance_history(employee_id):
        conn=get_connection(); cur=conn.cursor(dictionary=True)
        cur.execute('SELECT attendance_date,status,check_in,check_out FROM attendance WHERE employee_id=%s ORDER BY attendance_date DESC',(employee_id,))
        rows=cur.fetchall(); cur.close(); conn.close(); return jsonify(rows)

    @app.post('/api/leaves')
    def create_leave():
        data=request.get_json(silent=True) or {}
        required=['employee_id','start_date','end_date','reason']
        if any(not data.get(k) for k in required):
            return jsonify({'error':'employee_id, start_date, end_date and reason are required'}),400
        conn=get_connection(); cur=conn.cursor()
        cur.execute('INSERT INTO leave_requests (employee_id,start_date,end_date,reason,status) VALUES (%s,%s,%s,%s,%s)',
                    (data['employee_id'],data['start_date'],data['end_date'],data['reason'],'PENDING'))
        conn.commit(); leave_id=cur.lastrowid; cur.close(); conn.close(); return jsonify({'id':leave_id,'status':'PENDING'}),201

    @app.get('/api/reports/attendance-summary')
    def attendance_summary():
        conn=get_connection(); cur=conn.cursor(dictionary=True)
        cur.execute('''SELECT e.employee_code,e.name,
                      SUM(a.status='PRESENT') AS present_days,
                      SUM(a.status='ABSENT') AS absent_days,
                      SUM(a.status='LEAVE') AS leave_days
                      FROM employees e LEFT JOIN attendance a ON a.employee_id=e.id
                      GROUP BY e.id,e.employee_code,e.name ORDER BY e.name''')
        rows=cur.fetchall(); cur.close(); conn.close(); return jsonify(rows)

    return app
