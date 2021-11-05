# University Project

- Quizzes 
    - Create (Professor)
    - Answer (Student)
    - Review
        - As Student You Can Review Your Answers What You Did Right And What You Did Wrong
        - As Professor You Add Or Edit Or Delete Question Or Choice Before Starting The Quiz

- Assignments 
    - Create (Professor)

- Announcement
    - Professors Can Create Course Announcement Or Public Announcement

- Grades
    - Quizzes Grades
    - Assignment Grades
    - Midterm Grades
    - Final Grade

- Charts
    - Semester Charts
    - Course Charts
        - Quizzes
        - Assignments
        - Midterm
        - Pie Chart For Course

To Start The Project First Create DB
```
python manage.py makemigrations
```
Then
```
python manage.py migrate
```
Create Superuser
```
python manage.py createsuperuser
```
Now You Can Run The Project
```
python manage.py runserver
```