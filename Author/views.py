from decimal import Context
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.api import MessageFailure
from django.db import connection
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.core.files.storage import FileSystemStorage
from CPMS.helper_functions import validateUserDetails, validateFilename

# Implemention file for the Author View of the CPMS website. View function for each url call in the Author view is found here.

# Uility function used to collect all the rows into a dictionary returned from performing raw SQL queries
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# Logs out a user
@login_required
def logout(request):
    auth.logout(request)
    messages.info(request, 'Logged Out')
    return redirect('/')

# This function handles both GET and POST requests from the corresponding Author Modify Info page.
# The functions lets the user modify their information stored in the CPMS database and the Django User backend
@login_required
def authorModifyInfo(request):
    if request.method == 'POST':
        fname = request.POST["exampleFirstName"]
        lname = request.POST['exampleLastName']
        mIntial = request.POST['exampleMiddleInitial']
        email = request.POST['exampleInputEmail']
        address = request.POST['exampleAddress']
        affiliation = request.POST['exampleAffiliation']
        department = request.POST['exampleDepartment']
        city = request.POST['exampleCity']
        state = request.POST['exampleState']
        zipCode = request.POST['exampleZipCode']
        phone = request.POST['examplePhone']
        password = request.POST['examplePassword']
        valid = validateUserDetails(state, zipCode, mIntial, phone, password)
        if valid != True:
                messages.error(request, valid)
                return redirect('authorModifyInfo')
        if User.objects.filter(username=email).exists() and email != str(request.user.email):
            messages.error(request, 'email address already in use with a different account')
            return redirect('authorModifyInfo')
        else:
            request.user.first_name = fname
            request.user.last_name = lname
            request.user.email = email
            request.user.set_password(password)
            request.user.username = email
            request.user.save()
            auth.login(request, request.user)
            
        cursor = connection.cursor()
        cursor.execute("UPDATE dbo.Author SET FirstName = '{}', LastName = '{}', MiddleInitial = '{}', Affiliation = '{}', Department = '{}', Address = '{}', City = '{}', ZipCode = '{}', State = '{}', PhoneNumber = '{}', EmailAddress = '{}', Password = '{}' WHERE EmailAddress = '{}'".format
            (fname, lname, mIntial, affiliation, department, address, city, zipCode, state, phone, email, password, str(request.user.email)))
        messages.info(request,'Information Updated')  
        return redirect('authorModifyInfo')
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM dbo.Author WHERE EmailAddress = '{}'".format(str(request.user.email)) )
        Context = {'authors' :dictfetchall(cursor)}
        return render(request, 'authorModifyInfo.html', Context)

# This function handles both GET and POST requests from the corresponding Reviewer Register to Submit Paper page.
# The function lets a user register to submit papers. The form becomes inactive once the registration is done
@login_required
def authorRegisterToSubmitPaper(request):
    if request.method =='POST':
        address = request.POST['exampleAddress']
        affiliation = request.POST['exampleAffiliation']
        department = request.POST['exampleDepartment']
        city = request.POST['exampleCity']
        state = request.POST['exampleState']
        zipCode = request.POST['exampleZipCode']
        phone = request.POST['examplePhone']
        valid = validateUserDetails(state, zipCode, "a", phone, '0')
        if valid != True:
            messages.error(request, valid)
            return redirect('authorRegisterToSubmitPaper')
        cursor = connection.cursor()
        cursor.execute("UPDATE dbo.Author SET Affiliation = '{}', Department = '{}', Address = '{}', City = '{}', ZipCode = '{}', State = '{}', PhoneNumber = '{}' WHERE EmailAddress = '{}'".format
            (affiliation, department, address, city, zipCode, state, phone, str(request.user.email)))
        messages.info(request,'Registration Successful')
        return redirect('authorRegisterToSubmitPaper')
    else:
        cursor = connection.cursor()

        cursor.execute("SELECT FirstName, LastName, MiddleInitial, Affiliation FROM dbo.Author WHERE EmailAddress = '{}'".format(str(request.user.email)))
        context = {'authors': dictfetchall(cursor)} 
        return render(request, 'authorRegisterToSubmitPaper.html', context)

# This function handles both GET and POST requests from the corresponding Author submit Papers page.
# This function provides the user with the Paper Submission form. 
@login_required
def authorSubmitPaper(request):
    if request.method =='POST':
        cursor = connection.cursor()
        cursor.execute("SELECT AuthorID FROM dbo.Author WHERE EmailAddress = '{}'".format(str(request.user.email)))
        authorID = 0
        otherType = request.POST['exampleOtherType'] 
        for author in dictfetchall(cursor):
            authorID = author['AuthorID']
        uploaded_file = request.FILES['exampleInputFile']
        filename = uploaded_file.name
        if not validateFilename(filename):
            messages.error(request, "Incorrect file type, please upload a pdf/doc/docx/txt file")
            return redirect('authorSubmitPaper')
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        fileUrl = fs.url(filename) #url to the file

        title = request.POST['examplePaperTitle']
        cursor.execute("""INSERT INTO dbo.Paper
           (AuthorID
           ,Active
           ,FilenameOriginal
           ,Filename
           ,Title
           ,Certification
           ,NotesToReviewers
           ,AnalysisOfAlgorithms
           ,Applications
           ,Architecture
           ,ArtificialIntelligence
           ,ComputerEngineering
           ,Curriculum
           ,DataStructures
           ,Databases
           ,DistanceLearning
           ,DistributedSystems
           ,EthicalSocietalIssues
           ,FirstYearComputing
           ,GenderIssues
           ,GrantWriting
           ,GraphicsImageProcessing
           ,HumanComputerInteraction
           ,LaboratoryEnvironments
           ,Literacy
           ,MathematicsInComputing
           ,Multimedia
           ,NetworkingDataCommunications
           ,NonMajorCourses
           ,ObjectOrientedIssues
           ,OperatingSystems
           ,ParallelsProcessing
           ,Pedagogy
           ,ProgrammingLanguages
           ,Research
           ,Security
           ,SoftwareEngineering
           ,SystemsAnalysisAndDesign
           ,UsingTechnologyInTheClassroom
           ,WebAndInternetProgramming
           ,Other
           ,OtherDescription) 
           VALUES 
           ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', 
           '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' )""".format(authorID
           , True
           , filename
           , ""
           , title
           , ""
           , ""
           , True if request.POST.__contains__('analysisOfAlgorithms') else False
           , True if request.POST.__contains__('applications') else False
           , True if request.POST.__contains__('architecture') else False
           , True if request.POST.__contains__('artificialIntelligence') else False
           , True if request.POST.__contains__('computerEngineering') else False
           , True if request.POST.__contains__('curriculum') else False
           , True if request.POST.__contains__('dataStructures') else False
           , True if request.POST.__contains__('databases') else False
           , True if request.POST.__contains__('distanceLearning') else False
           , True if request.POST.__contains__('distributedSystems') else False
           , True if request.POST.__contains__('ethicalSocietalIssues') else False
           , True if request.POST.__contains__('firstYearComputing') else False
           , True if request.POST.__contains__('genderIssues') else False
           , True if request.POST.__contains__('grantWriting') else False
           , True if request.POST.__contains__('graphicsImageProcessing') else False
           , True if request.POST.__contains__('humanComputerInteraction') else False
           , True if request.POST.__contains__('laboratoryEnvironments') else False
           , True if request.POST.__contains__('literacy') else False
           , True if request.POST.__contains__('mathematicsInComputing') else False
           , True if request.POST.__contains__('multimedia') else False
           , True if request.POST.__contains__('networkingDataCommunications') else False
           , True if request.POST.__contains__('nonMajorCourses') else False
           , True if request.POST.__contains__('objectOrientedIssues') else False
           , True if request.POST.__contains__('operatingSystems') else False
           , True if request.POST.__contains__('parallelsProcessing') else False
           , True if request.POST.__contains__('pedagogy') else False
           , True if request.POST.__contains__('programmingLanguages') else False
           , True if request.POST.__contains__('research') else False
           , True if request.POST.__contains__('security') else False
           , True if request.POST.__contains__('softwareEngineering') else False
           , True if request.POST.__contains__('systemsAnalysisAndDesign') else False
           , True if request.POST.__contains__('usingTechnologyInTheClassroom') else False
           , True if request.POST.__contains__('webAndInternetProgramming') else False
           , True if request.POST.__contains__('other') else False
           , otherType ))
        messages.info(request,"Paper submitted")
        messages.info(request, fileUrl)
        return redirect('authorSubmitPaper')
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT EnabledAuthors FROM dbo.Defaults")
        Context = {"Defaults": (dictfetchall(cursor))[0]}
        return render(request, 'authorSubmitPaper.html', Context)