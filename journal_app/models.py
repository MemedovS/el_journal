
# from django.db import models
# from django.contrib.auth.models import User
#
# class Student(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     student_id = models.CharField(max_length=10, unique=True)
#     date_of_birth = models.DateField()
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"
#
# class Subject(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
# class Teacher(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"{self.user.username} - {self.subject.name}"
#
# class TeachingAssignment(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assignments')
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignments')
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = ('teacher', 'student', 'subject')
#
#     def __str__(self):
#         return f"{self.teacher} - {self.student} ({self.subject})"
#
# class Grade(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     grade = models.PositiveSmallIntegerField()
#     date = models.DateField()
#
#     def __str__(self):
#         return f"{self.student} - {self.subject}: {self.grade}"
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=10, unique=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.subject.name}"

class StudentGroup(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TeachingAssignment(models.Model):
    group = models.ForeignKey(StudentGroup, null=True, on_delete=models.CASCADE, related_name='assignments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('group', 'student', 'subject')

    def __str__(self):
        return f"{self.group.teacher} - {self.student} ({self.subject})"

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade}"
