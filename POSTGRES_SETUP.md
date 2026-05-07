# PostgreSQL Setup Guide for Timetable Generator

## **STEP 1: Download & Install PostgreSQL**

### On Windows:

1. **Download PostgreSQL:**
   - Go to: https://www.postgresql.org/download/windows/
   - Click **"Download the installer"**
   - Download **PostgreSQL 15** or latest version (currently v16)

2. **Run the installer:**
   - Double-click `postgresql-15.x-x64-setup.exe` (or your downloaded version)
   - Follow the installation wizard:
     - **Installation Directory:** Leave default (C:\Program Files\PostgreSQL\15)
     - **Components:** Make sure all are selected
     - **Data Directory:** Leave default
     - **Port:** Leave as **5432** (important!)
     - **Locale:** English, United States
     - **Password:** Set a password for `postgres` user
       - **RECOMMENDED:** Use `postgres` (simple for development)
       - Write this down if you use something different!
     - **Port:** Confirm **5432**

3. **Complete Installation:**
   - Let the installer finish
   - You can skip "Stack Builder" if prompted

---

## **STEP 2: Create the Database**

After PostgreSQL is installed, open **PowerShell** and run:

```powershell
psql -U postgres
```

When prompted for password, enter the password you set during installation (default: `postgres`)

Then run these commands:

```sql
CREATE DATABASE timetable_db ENCODING 'UTF8';
\q
```

---

## **STEP 3: Verify PostgreSQL Connection**

```powershell
psql -U postgres -d timetable_db -c "SELECT version();"
```

You should see PostgreSQL version info. If successful, you're ready!

---

## **STEP 4: Environment Configuration (Optional)**

If you used a different password or host, create a `.env` file in the backend directory:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=timetable_db
DB_USER=postgres
DB_PASSWORD=your_password_here
```

---

## **STEP 5: Start the Application**

### Open PowerShell and run:

```powershell
cd "c:\Users\GUGAN\OneDrive\Documents\Timetable generator\timetable-generator-master"

# Activate virtual environment
& ".\.venv\Scripts\Activate.ps1"

# Go to backend
cd backend

# Start backend
python app.py
```

### In another PowerShell window:

```powershell
cd "c:\Users\GUGAN\OneDrive\Documents\Timetable generator\timetable-generator-master"

# Start frontend
npm start
```

---

## **TROUBLESHOOTING**

### PSql command not found?
- PostgreSQL might not be added to PATH
- Use full path: `"C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres`

### Connection refused?
- Check if PostgreSQL service is running
- On Windows, search for "Services" and look for "postgresql-x64-15" (or your version)
- If not running, right-click → Start

### Wrong password?
- Windows search → "pgAdmin 4"
- Use pgAdmin GUI to reset the password

### Port already in use?
- PostgreSQL uses port 5432 by default
- If another app uses it, change PostgreSQL port during reinstall or run:
  ```sql
  SELECT * FROM pg_settings WHERE name = 'port';
  ```

---

## **Quick Test**

After everything is set up, test the backend:

1. Start backend: `python app.py`
2. In another terminal:
   ```powershell
   Invoke-WebRequest http://localhost:8000/get-courses -Headers @{}
   ```
3. You should see: `[]` (empty array, which is correct for new database)

---

## **Need Help?**

Run these commands to verify each step:

```powershell
# Check PostgreSQL is installed
psql --version

# Check database exists
psql -U postgres -c "SELECT datname FROM pg_database;"

# Check tables are created
psql -U postgres -d timetable_db -c "\dt"

# Check connection with Python
python -c "import psycopg2; print('psycopg2 OK')"
```

---

**Once PostgreSQL is running, the application should work without the Network Error!**
