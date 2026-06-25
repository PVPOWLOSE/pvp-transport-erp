from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import pandas as pd

app = Flask(__name__)
app.secret_key = "pvp123"

# -----------------------------
# DATABASE
# -----------------------------
conn = sqlite3.connect("pvp_erp.db", check_same_thread=False)
cursor = conn.cursor()

# -----------------------------
# CREATE TABLES
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vehicles(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_no TEXT,
    capacity TEXT,
    rc_expiry TEXT,
    insurance_expiry TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS drivers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_name TEXT,
    mobile TEXT,
    license_no TEXT
)
""")

conn.commit()

# -----------------------------
# DEFAULT LOGIN
# -----------------------------
user = cursor.execute(
    "SELECT * FROM users WHERE username='admin'"
).fetchone()

if user is None:
    cursor.execute(
        "INSERT INTO users(username,password) VALUES(?,?)",
        ("admin", "admin123")
    )
    conn.commit()
    # -----------------------------
# LOGIN
# -----------------------------

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Invalid Username or Password"

    return render_template("login.html")


# -----------------------------
# DASHBOARD
# -----------------------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    total_vehicles = cursor.execute(
        "SELECT COUNT(*) FROM vehicles"
    ).fetchone()[0]

    total_drivers = cursor.execute(
        "SELECT COUNT(*) FROM drivers"
    ).fetchone()[0]

    return render_template(
        "dashboard.html",
        total_vehicles=total_vehicles,
        total_drivers=total_drivers
    )


# -----------------------------
# LOGOUT
# -----------------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# -----------------------------
# RUN
# -----------------------------

@app.route("/vehicles", methods=["GET", "POST"])
def vehicles():

    if request.method == "POST":

        vehicle_no = request.form["vehicle_no"]
        capacity = request.form["capacity"]
        rc_expiry = request.form["rc_expiry"]
        insurance_expiry = request.form["insurance_expiry"]

        cursor.execute("""
        INSERT INTO vehicles
        (vehicle_no, capacity, rc_expiry, insurance_expiry)
        VALUES (?, ?, ?, ?)
        """,
        (
            vehicle_no,
            capacity,
            rc_expiry,
            insurance_expiry
        ))

        conn.commit()

        return redirect("/dashboard")

    return render_template("vehicle.html")

@app.route("/drivers", methods=["GET", "POST"])
def drivers():

    if request.method == "POST":

        driver_name = request.form["driver_name"]
        mobile = request.form["mobile"]
        license_no = request.form["license_no"]

        cursor.execute("""
        INSERT INTO drivers
        (driver_name, mobile, license_no)
        VALUES (?, ?, ?)
        """,
        (
            driver_name,
            mobile,
            license_no
        ))

        conn.commit()

        return redirect("/dashboard")

    return render_template("driver.html")

@app.route("/trips", methods=["GET", "POST"])
def trips():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_no TEXT,
        driver_name TEXT,
        loading_point TEXT,
        unloading_point TEXT
    )
    """)
    conn.commit()

    if request.method == "POST":

        vehicle_no = request.form["vehicle_no"]
        driver_name = request.form["driver_name"]
        loading_point = request.form["loading_point"]
        unloading_point = request.form["unloading_point"]

        cursor.execute("""
        INSERT INTO trips
        (vehicle_no, driver_name, loading_point, unloading_point)
        VALUES (?, ?, ?, ?)
        """, (
            vehicle_no,
            driver_name,
            loading_point,
            unloading_point
        ))

        conn.commit()

        return redirect("/dashboard")

    return render_template("trip.html")

@app.route("/allocation", methods=["GET","POST"])
def allocation():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS allocation(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_no TEXT,
        driver_name TEXT,
        customer TEXT,
        destination TEXT
    )
    """)
    conn.commit()

    if request.method == "POST":

        vehicle_no = request.form["vehicle_no"]
        driver_name = request.form["driver_name"]
        customer = request.form["customer"]
        destination = request.form["destination"]

        cursor.execute("""
        INSERT INTO allocation
        (vehicle_no,driver_name,customer,destination)
        VALUES(?,?,?,?)
        """,
        (
            vehicle_no,
            driver_name,
            customer,
            destination
        ))

        conn.commit()

        return redirect("/dashboard")

    return render_template("allocation.html")

@app.route("/attendance", methods=["GET","POST"])
def attendance():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        driver_name TEXT,
        attendance_date TEXT,
        status TEXT
    )
    """)
    conn.commit()

    if request.method == "POST":

        driver_name = request.form["driver_name"]
        attendance_date = request.form["attendance_date"]
        status = request.form["status"]

        cursor.execute("""
        INSERT INTO attendance
        (driver_name,attendance_date,status)
        VALUES(?,?,?)
        """,
        (
            driver_name,
            attendance_date,
            status
        ))

        conn.commit()

        return redirect("/dashboard")

    return render_template("attendance.html")

@app.route("/diesel", methods=["GET","POST"])
def diesel():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diesel(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_no TEXT,
        diesel_date TEXT,
        litres REAL,
        amount REAL,
        km INTEGER
    )
    """)
    conn.commit()

    if request.method == "POST":

        vehicle_no = request.form["vehicle_no"]
        diesel_date = request.form["diesel_date"]
        litres = request.form["litres"]
        amount = request.form["amount"]
        km = request.form["km"]

        cursor.execute("""
        INSERT INTO diesel
        (vehicle_no,diesel_date,litres,amount,km)
        VALUES(?,?,?,?,?)
        """,
        (
            vehicle_no,
            diesel_date,
            litres,
            amount,
            km
        ))

        conn.commit()

        return redirect("/dashboard")

    return render_template("diesel.html")

@app.route("/maintenance", methods=["GET","POST"])
def maintenance():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS maintenance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_no TEXT,
        service_date TEXT,
        maintenance_type TEXT,
        amount REAL,
        remarks TEXT
    )
    """)
    conn.commit()

    if request.method == "POST":

        vehicle_no = request.form["vehicle_no"]
        service_date = request.form["service_date"]
        maintenance_type = request.form["maintenance_type"]
        amount = request.form["amount"]
        remarks = request.form["remarks"]

        cursor.execute("""
        INSERT INTO maintenance
        (vehicle_no,service_date,maintenance_type,amount,remarks)
        VALUES(?,?,?,?,?)
        """,
        (
            vehicle_no,
            service_date,
            maintenance_type,
            amount,
            remarks
        ))

        conn.commit()

        return redirect("/dashboard")

    return render_template("maintenance.html")

@app.route("/salary", methods=["GET", "POST"])
def salary():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS salary(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        driver_name TEXT,
        month TEXT,
        basic REAL,
        incentive REAL,
        advance REAL,
        net_salary REAL
    )
    """)
    conn.commit()

    if request.method == "POST":

        driver_name = request.form["driver_name"]
        month = request.form["month"]
        basic = float(request.form["basic"])
        incentive = float(request.form["incentive"])
        advance = float(request.form["advance"])

        net_salary = basic + incentive - advance

        cursor.execute("""
        INSERT INTO salary
        (driver_name, month, basic, incentive, advance, net_salary)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (driver_name, month, basic, incentive, advance, net_salary))

        conn.commit()

        return redirect("/salary")

    data = cursor.execute("SELECT * FROM salary").fetchall()

    return render_template("salary.html", data=data)

@app.route("/payment", methods=["GET", "POST"])
def payment():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer TEXT,
        invoice_no TEXT,
        invoice_date TEXT,
        amount REAL,
        status TEXT,
        received_date TEXT
    )
    """)
    conn.commit()

    if request.method == "POST":

        customer = request.form["customer"]
        invoice_no = request.form["invoice_no"]
        invoice_date = request.form["invoice_date"]
        amount = request.form["amount"]
        status = request.form["status"]
        received_date = request.form["received_date"]

        cursor.execute("""
        INSERT INTO payments
        (customer, invoice_no, invoice_date, amount, status, received_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (customer, invoice_no, invoice_date, amount, status, received_date))

        conn.commit()

        return redirect("/payment")

    data = cursor.execute("SELECT * FROM payments").fetchall()

    return render_template("payment.html", data=data)

@app.route("/reports")
def reports():

    vehicle_count = cursor.execute(
        "SELECT COUNT(*) FROM vehicles"
    ).fetchone()[0]

    driver_count = cursor.execute(
        "SELECT COUNT(*) FROM drivers"
    ).fetchone()[0]

    trip_count = cursor.execute(
        "SELECT COUNT(*) FROM trips"
    ).fetchone()[0]

    allocation_count = cursor.execute(
        "SELECT COUNT(*) FROM allocation"
    ).fetchone()[0]

    attendance_count = cursor.execute(
        "SELECT COUNT(*) FROM attendance"
    ).fetchone()[0]

    diesel_total = cursor.execute(
        "SELECT IFNULL(SUM(amount),0) FROM diesel"
    ).fetchone()[0]

    maintenance_total = cursor.execute(
        "SELECT IFNULL(SUM(amount),0) FROM maintenance"
    ).fetchone()[0]

    salary_total = cursor.execute(
        "SELECT IFNULL(SUM(net_salary),0) FROM salary"
    ).fetchone()[0]

    payment_total = cursor.execute(
        "SELECT IFNULL(SUM(amount),0) FROM payments"
    ).fetchone()[0]

    return render_template(
        "reports.html",
        vehicle_count=vehicle_count,
        driver_count=driver_count,
        trip_count=trip_count,
        allocation_count=allocation_count,
        attendance_count=attendance_count,
        diesel_total=diesel_total,
        maintenance_total=maintenance_total,
        salary_total=salary_total,
        payment_total=payment_total
    )

@app.route("/vehicle_search", methods=["GET", "POST"])
def vehicle_search():

    data = []

    if request.method == "POST":

        vehicle_no = request.form["vehicle_no"]

        data = cursor.execute(
            "SELECT * FROM vehicles WHERE vehicle_no LIKE ?",
            ('%' + vehicle_no + '%',)
        ).fetchall()

    return render_template("vehicle_search.html", data=data)

@app.route("/vehicle_edit/<int:id>", methods=["GET","POST"])
def vehicle_edit(id):

    if request.method == "POST":

        vehicle_no = request.form["vehicle_no"]
        capacity = request.form["capacity"]
        rc_expiry = request.form["rc_expiry"]
        insurance_expiry = request.form["insurance_expiry"]

        cursor.execute("""
        UPDATE vehicles
        SET vehicle_no=?,
            capacity=?,
            rc_expiry=?,
            insurance_expiry=?
        WHERE id=?
        """,
        (
            vehicle_no,
            capacity,
            rc_expiry,
            insurance_expiry,
            id
        ))

        conn.commit()

        return redirect("/vehicle_search")

    data = cursor.execute(
        "SELECT * FROM vehicles WHERE id=?",
        (id,)
    ).fetchone()

    return render_template("vehicle_edit.html", data=data)

@app.route("/vehicle_delete/<int:id>")
def vehicle_delete(id):

    cursor.execute(
        "DELETE FROM vehicles WHERE id=?",
        (id,)
    )

    conn.commit()

    return redirect("/vehicle_search")

@app.route("/driver_delete/<int:id>")
def driver_delete(id):

    cursor.execute(
        "DELETE FROM drivers WHERE id=?",
        (id,)
    )

    conn.commit()

    return redirect("/driver_search")

@app.route("/driver_edit/<int:id>", methods=["GET","POST"])
def driver_edit(id):

    if request.method == "POST":

        driver_name = request.form["driver_name"]
        mobile = request.form["mobile"]
        license_no = request.form["license_no"]

        cursor.execute("""
        UPDATE drivers
        SET driver_name=?,
            mobile=?,
            license_no=?
        WHERE id=?
        """,
        (
            driver_name,
            mobile,
            license_no,
            id
        ))

        conn.commit()

        return redirect("/driver_search")

    data = cursor.execute(
        "SELECT * FROM drivers WHERE id=?",
        (id,)
    ).fetchone()

    return render_template("driver_edit.html", data=data)

@app.route("/driver_search")
def driver_search():

    data = cursor.execute("SELECT * FROM drivers").fetchall()

    return render_template("driver_search.html", data=data)

@app.route("/trip_search")
def trip_search():

    data = cursor.execute(
        "SELECT * FROM trips"
    ).fetchall()

    return render_template("trip_search.html", data=data)

@app.route("/trip_edit/<int:id>", methods=["GET", "POST"])
def trip_edit(id):

    if request.method == "POST":

        vehicle_no = request.form["vehicle_no"]
        driver_name = request.form["driver_name"]
        loading_point = request.form["loading_point"]
        unloading_point = request.form["unloading_point"]

        cursor.execute("""
            UPDATE trips
            SET vehicle_no=?, driver_name=?, loading_point=?, unloading_point=?
            WHERE id=?
        """, (vehicle_no, driver_name, loading_point, unloading_point, id))

        conn.commit()

        return redirect("/trip_search")

    data = cursor.execute(
        "SELECT * FROM trips WHERE id=?",
        (id,)
    ).fetchone()

    return render_template("trip_edit.html", data=data)

@app.route("/trip_delete/<int:id>")
def trip_delete(id):

    cursor.execute(
        "DELETE FROM trips WHERE id=?",
        (id,)
    )

    conn.commit()

    return redirect("/trip_search")

@app.route("/attendance_search", methods=["GET", "POST"])
def attendance_search():

    if request.method == "POST":
        driver = request.form["driver_name"]

        data = cursor.execute(
            "SELECT * FROM attendance WHERE driver_name LIKE ?",
            ('%' + driver + '%',)
        ).fetchall()

    else:
        data = cursor.execute(
            "SELECT * FROM attendance"
        ).fetchall()

    return render_template(
        "attendance_search.html",
        data=data
    )

@app.route("/attendance_edit/<int:id>", methods=["GET", "POST"])
def attendance_edit(id):

    if request.method == "POST":
        attendance_date = request.form["date"]
        driver_name = request.form["driver_name"]
        status = request.form["status"]

        cursor.execute("""
            UPDATE attendance
            SET attendance_date = ?,
                driver_name = ?,
                status = ?
            WHERE id = ?
        """, (attendance_date, driver_name, status, id))

        conn.commit()
        return redirect("/attendance_search")

    data = cursor.execute(
        "SELECT * FROM attendance WHERE id=?",
        (id,)
    ).fetchone()

    return render_template(
        "attendance_edit.html",
        data=data
    )

@app.route("/attendance_delete/<int:id>")
def attendance_delete(id):

    cursor.execute(
        "DELETE FROM attendance WHERE id=?",
        (id,)
    )

    conn.commit()

    return redirect("/attendance_search")

@app.route("/vehicle_export")
def vehicle_export():

    data = cursor.execute("SELECT * FROM vehicles").fetchall()

    df = pd.DataFrame(data)

    file_name = "Vehicle_Report.xlsx"

    df.to_excel(file_name, index=False)

    return send_file(file_name, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)