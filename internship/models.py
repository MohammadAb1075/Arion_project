from django.db import models
from public.models import Users,Student
from public.models import Faculties,College,Major


class InternshipHead(models.Model):
    user    = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    request = models.OneToOneField('internship.Request',on_delete=models.DO_NOTHING)
    phone   = models.CharField(max_length=31)
    email   = models.EmailField()
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class State(models.Model):
    namestate = models.CharField(max_length=63)
    def __str__(self):
        return self.namestate



class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    namecity  = models.CharField(max_length=63)
    def __str__(self):
        return self.namecity


class InternShipPlace(models.Model):
    nameplace         = models.CharField(max_length=127)
    city              = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    address           = models.TextField()
    phone             = models.CharField(max_length=15)
    internShipWebSite = models.CharField(null=True,blank=True,max_length=127)
    def __str__(self):
        return self.nameplace

Semester = (
    ('1','First Semester'),
    ('2','Second Semester'),
    ('3','Summer'),
)


# State = (
#     ('1','1'),
#     ('2','2'),
#     ('3','3'),
# )



class Request(models.Model):
    internshipPlace        = models.ForeignKey(InternShipPlace,on_delete=models.DO_NOTHING)
    student                = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    term                   = models.CharField(choices=Semester, max_length=15)
    title                  = models.CharField(max_length=31)
    comment                = models.TextField(null=True,blank=True)#text ==>comment
    state                  = models.IntegerField(default=0)
    agreementUploadedUrl   = models.TextField(null=True,blank=True)
    reqdate                = models.DateTimeField()
    reqhash                = models.TextField(null=True,blank=True)

    def __str__(self):
            return "{} From : {}".format(
            self.title,
            self.student.user.first_name + ' ' + self.student.user.last_name
        )

class Opinion(models.Model):
    user         = models.ForeignKey(Users, on_delete=models.DO_NOTHING, related_name='Operson')
    request      = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='Orequest')
    opinion      = models.BooleanField(null=True,blank=True)
    seenDate     = models.DateTimeField(null=True,blank=True)
    opinionDate  = models.DateTimeField(null=True,blank=True)
    opinionText  = models.TextField(null=True,blank=True)

    def __str__(self):
        return "{} Request From {} To {}".format(self.request.title,self.request.student.user.first_name + ' ' + self.request.student.user.last_name,self.user.roles.all()[0])



class InternShip(models.Model):
    student                   = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    internshiphead            = models.ForeignKey(InternshipHead, on_delete=models.DO_NOTHING)
    gtOpinion                 = models.ForeignKey(Opinion, on_delete=models.DO_NOTHING)
    guideTeacher              = models.ForeignKey('internship.Choosing', on_delete=models.DO_NOTHING )#choosing
    studentFinalReport        = models.TextField(null=True,blank=True)
    studentObjectionText      = models.TextField(null=True,blank=True)
    studentObjectionDate      = models.DateTimeField(null=True,blank=True)
    supervisorReportUploadUrl = models.TextField(null=True,blank=True)
    internShipState           = models.BooleanField(null=True,blank=True)



class WeeklyConfirmarion(models.Model):
    internship                       = models.ForeignKey(InternShip, on_delete=models.DO_NOTHING)
    weekNumber                       = models.IntegerField()
    supervisorAttendanCeconfirmation = models.BooleanField(default=False)
    supervisorReportConfirmation     = models.BooleanField(default=False)



class AttendanceTable(models.Model):
    internShip             = models.ForeignKey(InternShip, on_delete=models.DO_NOTHING)
    startTime              = models.DateTimeField()
    endTime                = models.DateTimeField()
    weekNumber             = models.IntegerField()



class WeeklyReport(models.Model):
    internShip                = models.ForeignKey(InternShip, on_delete=models.DO_NOTHING)
    reportDate                = models.DateTimeField()
    weekNumber                = models.IntegerField()
    reportTitle               = models.CharField(max_length=63)
    reportText                = models.TextField()



class Choosing(models.Model):
    user       = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    student    = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    gtOpinion  = models.ForeignKey(Opinion, on_delete=models.DO_NOTHING)



class Student_InternShip(models.Model):
    internShip          = models.ForeignKey(InternShip ,on_delete=models.DO_NOTHING)
    gtgrade             = models.FloatField()
    gtgradeconfirmation = models.BooleanField()
