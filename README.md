# All-In-One
SPM Project


## Getting Started


### Setting up development environemnt 
1. Check your python version    
   ```sh 
   python --version
   ``` 
   
If you do not have python or python version is below 3.3, install the latest version [here](https://www.python.org/downloads/)


### Setting up virtual environment 

1. Create virtual environment     
   ```sh
   python3 -m venv venv OR
   python -m venv venv
   
2. Activate virtual environment  
   ```sh
   source venv/bin/activate (for Mac)
   venv\Scripts\activate.bat (for Win)
   
3. Install modules in requirements.txt     
   ```sh
   pip install -r requirements.txt

### Setting up the Database
1. Import Import_LMS_Data.sql (either through phpmyadmin or SQL Workbench or any SQL management tool)

2. Go to SQL Workbench or Import through phpmyadmin

   - For SQL Workbench:
      - On the SCHEMAS tab on the left, right click on 'course'
      - Table Data Import Wizard
      - Import the courses.csv (inside Raw_Data folder)
      - Click on the course table and verify that it is populated now
      - Repeat the above steps for each table IN THIS EXACT ORDER: role --> staff --> registration

   - For phpmyadmin:
      - From the database list, click on is212_all_in_one, click on 'course' table
      - click import on the navbar, you should see that it says ' Importing into the table "course" '
      - Import the courses.csv file (inside Raw_Data folder)
      - Under Partial Import tab, set the field 'Skip this number of queries (for SQL) starting from the first one' to 1
      - Click 'Go' to execute the import
      - Click on the course table and verify that it is populated now
      - Repeat the above steps for each table IN THIS EXACT ORDER: role --> staff --> registration

4. Import Create_LJPS_Data.sql


### Setting up the HTTP Server

   1. Python HTTP-Server: Run this command in another terminal
   ```sh
   python -m http.server 8008 --bind 127.0.0.1
   ```
   2. Create another terminal and run the following command
   ```sh
   python backend/app.py
   ```

### Testing the app

   1. Use your favourite browser and type the link below: 
   ```sh
   127.0.0.1:8008/frontend/role_toggle.html
   ```
   2. Choose according to the user role you want to access, to use the different functions available to the different roles.


### Alternative method of Setting up and Testing the app if you receive a CORS-error

    ### Setting up the HTTP Server and Testing the app

   1. Run this command in your terminal
    ``` sh
    npm install http-server -g
    ```

   2. Run this in your terminal
   ```sh
   http-server --cors
   ```

   3. Split terminal and run this in another terminal
   ```sh
    cd backend
   ```
   ```sh
   python app.py
   ```

   4. Use your favourite brower and type the link below:
   ```sh
   http://127.0.0.1:8080/frontend/role_toggle.html
   ```


## Linter Badge
[![GitHub Super-Linter](https://github.com/alimsihui/All-In-One/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)


