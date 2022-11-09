1. Import Import_LMS_Data.sql (either thru phpmyadmin or SQL Workbench or wtv yall use)

2. Go to SQL Workbench

3. Do these:
a. On the SCHEMAS tab on the left, right click on 'course'
b. Table Data Import Wizard
c. Import the course.csv (inside Raw_Data folder)
d. Done then make sure u can see course table populated now
e. then repeat for each csv IN THIS EXACT ORDER: role --> staff --> registration

4. Import Create_LJPS_Data.sql

5. If you need more data, just add to Create_LJPS_Data.sql then re-import Create_LJPS_Data.sql