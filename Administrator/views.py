from CPMS.helper_functions import validateUserDetails, validateFilename
from decimal import Context
from typing import Coroutine
from django import contrib
from django.contrib import messages
from django.contrib.messages.api import info
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.models import User, auth
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage

# Implemention file for the Administrator View of the CPMS website. View function for each url call in the Administrator view is found here.

# Uility function used to collect all the rows into a dictionary returned from performing raw SQL queries
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# Logs out a user 
def logout(request):
    auth.logout(request)
    messages.info(request, 'Logged Out')
    return redirect('/')

# View function for the Author maintenance page. The page contains three forms used for Add/Modify/Delete actions on Authors. 
# Seperate functions are used to perform each action. This function handles GET requests to the corresponding maintainAuthor page
def maintainAuthors(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dbo.Author")
    context = {'authors': dictfetchall(cursor)}
    return render(request, 'maintainAuthors.html', context)

# Inserts an Author into the CPMS database and creates a Django User. This function handles the POST requests coming from the insert author form
# from the corresponding maintainAuthor page 
def insertAuthors(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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
        return redirect('maintainAuthors')

    if User.objects.filter(username=email).exists():
        messages.error(request, 'email address already in use with a different account')
        return redirect('maintainAuthors')
    else:
        user = User.objects.create_user(username=email, password=password, email=email, first_name=fname, last_name=lname)
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO dbo.Author (FirstName, LastName, MiddleInitial, Password, EmailAddress, Address, Affiliation, Department, City
    , State, ZipCode, PhoneNumber) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(fname, lname
    , mIntial, password, email, address, affiliation, department, city, state, zipCode, phone))
    messages.info(request, 'Author Created')
    return redirect('maintainAuthors')

# Deletes an Author from the CPMS database. This function handles the POST requests coming from the delete author form
# from the corresponding maintainAuthor page
def deleteAuthors(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    ID = request.POST['exampleAuthorID']
    cursor = connection.cursor()
    cursor.execute("DELETE FROM dbo.Author  WHERE AuthorID = '{}' ".format(ID))
    messages.info(request, 'Author Deleted')
    return redirect('maintainAuthors')

# Modifies an Author in the CPMS database and in the Django User backend. This function handles the POST requests coming from the update author form
# from the corresponding maintainAuthor page
def updateAuthors(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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
    ID = request.POST['exampleAuthorID']
    password = request.POST['examplePassword']
    valid = validateUserDetails(state, zipCode, mIntial, phone, password)
    if valid != True:
        messages.error(request, valid)
        return redirect('maintainAuthors')
    cursor = connection.cursor()
    cursor.execute("SELECT EmailAddress FROM dbo.Author WHERE AuthorID = '{}'".format(ID))
    authors = dictfetchall(cursor)
    updateUser = User.objects.get(username=authors[0].EmailAddress)
    if User.objects.filter(username=email).exists() and email != authors[0].EmailAddress:
        messages.error(request, 'email address already in use with a different account')
        return redirect('maintainAuthors')
    else:
        updateUser.first_name = fname
        updateUser.last_name = lname
        updateUser.email = email
        updateUser.set_password(password)
        updateUser.username = email
        updateUser.save()
     
    cursor = connection.cursor()
    cursor.execute("UPDATE dbo.Author SET FirstName = '{}', LastName = '{}', MiddleInitial = '{}', Affiliation = '{}', Department = '{}', Address = '{}', City = '{}', ZipCode = '{}', State = '{}', PhoneNumber = '{}', EmailAddress = '{}', Password = '{}' WHERE AuthorID = '{}'".format
            (fname, lname, mIntial, affiliation, department, address, city, zipCode, state, phone, email, password, ID))
    
    messages.info(request,'Author Information Updated')
    return redirect('maintainAuthors')

# View function for the Paper maintenance page. The page contains three forms used for Add/Modify/Delete actions on Papers. 
# Seperate functions are used to perform each action. This function handles GET requests to the corresponding maintainPaper page
def maintainPapers(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dbo.Paper")
    context = {'papers': dictfetchall(cursor)}
    return render(request, 'maintainPapers.html', context)

# Inserts a Paper into the CPMS database. This function handles the POST requests coming from the insert paper form
# from the corresponding maintainPaper page
def insertPapers(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    uploaded_file = request.FILES['exampleInputFile']
    filename = uploaded_file.name
    if not validateFilename(filename):
            messages.error(request, "Incorrect file type, please upload a pdf/doc/docx/txt file")
            return redirect('insertPapers')
    fs = FileSystemStorage()
    filename = fs.save(uploaded_file.name, uploaded_file)
    authorID = request.POST['exampleAuthorID']
    title = request.POST['examplePaperTitle']
    otherType = request.POST['exampleOtherType']
    cursor = connection.cursor()
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
    messages.info(request,"Paper added")
    return redirect('maintainPapers')

# Modifies a Paper in the CPMS database. This function handles the POST requests coming from the update paper form
# from the corresponding maintainPaper page
def updatePapers(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    authorID = request.POST['exampleAuthorID']
    paperID = request.POST['examplePaperID']
    uploaded_file = request.FILES['exampleInputFile']
    filename = uploaded_file.name
    if not validateFilename(filename):
            messages.error(request, "Incorrect file type, please upload a pdf/doc/docx/txt file")
            return redirect('updatePapers')
    fs = FileSystemStorage()
    filename = fs.save(uploaded_file.name, uploaded_file)
    title = request.POST['examplePaperTitle']
    otherType = request.POST['exampleOtherType']
    cursor = connection.cursor()
    cursor.execute("""UPDATE dbo.Paper
   SET AuthorID = '{}'
      ,Active = '{}'
      ,FilenameOriginal = '{}'
      ,Filename = '{}'
      ,Title = '{}'
      ,Certification = '{}'
      ,NotesToReviewers = '{}'
      ,AnalysisOfAlgorithms = '{}'
      ,Applications = '{}'
      ,Architecture = '{}'
      ,ArtificialIntelligence = '{}'
      ,ComputerEngineering = '{}'
      ,Curriculum = '{}'
      ,DataStructures = '{}'
      ,Databases = '{}'
      ,DistanceLearning = '{}'
      ,DistributedSystems = '{}'
      ,EthicalSocietalIssues = '{}'
      ,FirstYearComputing = '{}'
      ,GenderIssues = '{}'
      ,GrantWriting = '{}'
      ,GraphicsImageProcessing = '{}'
      ,HumanComputerInteraction = '{}'
      ,LaboratoryEnvironments = '{}'
      ,Literacy = '{}'
      ,MathematicsInComputing = '{}'
      ,Multimedia = '{}'
      ,NetworkingDataCommunications = '{}'
      ,NonMajorCourses = '{}'
      ,ObjectOrientedIssues = '{}'
      ,OperatingSystems = '{}'
      ,ParallelsProcessing = '{}'
      ,Pedagogy = '{}'
      ,ProgrammingLanguages = '{}'
      ,Research = '{}'
      ,Security = '{}'
      ,SoftwareEngineering = '{}'
      ,SystemsAnalysisAndDesign = '{}'
      ,UsingTechnologyInTheClassroom = '{}'
      ,WebAndInternetProgramming = '{}'
      ,Other = '{}'
      ,OtherDescription = '{}'
    WHERE PaperID = '{}' """.format(authorID, True, filename, filename, title, "", "",
        True if request.POST.__contains__('analysisOfAlgorithms') else False
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
           , otherType
           , paperID))
    messages.info(request, 'Paper updated')
    return redirect('maintainPapers')

# Deletes a Paper from the CPMS database. This function handles the POST requests coming from the delete paper form
# from the corresponding maintainPaper page
def deletePapers(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    ID = request.POST['examplePaperID']
    cursor = connection.cursor()
    cursor.execute("DELETE FROM dbo.Paper WHERE PaperID = '{}' ".format(ID))
    messages.info(request, 'Paper Deleted')
    return redirect('maintainPapers')

# View function for the Reviewers maintenance page. The page contains three forms used for Add/Modify/Delete actions on Reviewers. 
# Seperate functions are used to perform each action. This function handles GET requests to the corresponding maintainReviewers page
def maintainReviewers(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dbo.Reviewer")
    context = {'reviewers': dictfetchall(cursor)}
    return render(request, 'maintainReviewers.html', context)

# Inserts a Reviewer into the CPMS database and creates a Django User. This function handles the POST requests coming from the insert reviewer form
# from the corresponding maintainReviewers page
def insertReviewers(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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
    otherType = request.POST['exampleOtherType']
    password = request.POST['examplePassword']
    valid = validateUserDetails(state, zipCode, mIntial, phone, password)
    if valid != True:
        messages.error(request, valid)
        return redirect('maintainReviewers')    
    if User.objects.filter(username=email).exists():
        messages.error(request, 'email address already in use with a different account')
        return redirect('maintainReviewers')
    else:
        user = User.objects.create_user(username=email, password=password, email=email, first_name=fname, last_name=lname)
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO dbo.Reviewer
           (Active
           ,FirstName
           ,LastName
           ,MiddleInitial
           ,EmailAddress
           ,Affiliation
           ,Department
           ,Address
           ,City
           ,State
           ,ZipCode
           ,PhoneNumber
           ,Password
           ,AnalysisOfAlgorithms
           ,Applications
           ,Architecture
           ,ArtificialIntelligence
           ,ComputerEngineering
           ,Curriculum
           ,DataStructures
           ,Databases
           ,DistancedLearning
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
           ,ParallelProcessing
           ,Pedagogy
           ,ProgrammingLanguages
           ,Research
           ,Security
           ,SoftwareEngineering
           ,SystemsAnalysisAndDesign
           ,UsingTechnologyInTheClassroom
           ,WebAndInternetProgramming
           ,Other
           ,OtherDescription
           ,ReviewsAcknowledged) 
           VALUES 
           ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'
           , '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'
           , '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(
           True, fname, lname, mIntial, email, affiliation, department, address, city, state, zipCode, phone, password
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
           , otherType, False ))
   
    messages.info(request,"Reviewer added")
    return redirect('maintainReviewers')

# Modifies a Reviewer in the CPMS database and in the Django User backend. This function handles the POST requests coming from the update
#  reviewer form from the corresponding maintainReviewers page
def updateReviewers(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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
    otherType = request.POST['exampleOtherType'] 
    reviewerID = request.POST['exampleReviewerID']
    password = request.POST['examplePassword']
    cursor = connection.cursor()
    cursor.execute("SELECT EmailAddress FROM dbo.Reviewer WHERE ReviewerID = '{}'".format(reviewerID))
    reviewers = dictfetchall(cursor)
    updateUser = User.objects.get(username=reviewers[0]['EmailAddress'])
    valid = validateUserDetails(state, zipCode, mIntial, phone, password)
    if valid != True:
        messages.error(request, valid)
        return redirect('maintainReviewers')
    if User.objects.filter(username=email).exists() and email != reviewers[0].EmailAddress:
        messages.error(request, 'email address already in use with a different account')
        return redirect('maintainReviewers')
    else:
        updateUser.first_name = fname
        updateUser.last_name = lname
        updateUser.email = email
        updateUser.set_password(password)
        updateUser.username = email
        updateUser.save()
        
    cursor = connection.cursor()
    cursor.execute("""UPDATE dbo.Reviewer
   SET Active = '{}'
      ,FirstName = '{}'
      ,LastName = '{}'
      ,MiddleInitial = '{}'
      ,EmailAddress = '{}'
      ,Affiliation = '{}'
      ,Department = '{}'
      ,Address = '{}'
      ,City = '{}'
      ,State = '{}'
      ,ZipCode = '{}'
      ,PhoneNumber = '{}'
      ,Password = '{}'
      ,AnalysisOfAlgorithms = '{}'
      ,Applications = '{}'
      ,Architecture = '{}'
      ,ArtificialIntelligence = '{}'
      ,ComputerEngineering = '{}'
      ,Curriculum = '{}'
      ,DataStructures = '{}'
      ,Databases = '{}'
      ,DistancedLearning = '{}'
      ,DistributedSystems = '{}'
      ,EthicalSocietalIssues = '{}'
      ,FirstYearComputing = '{}'
      ,GenderIssues = '{}'
      ,GrantWriting = '{}'
      ,GraphicsImageProcessing = '{}'
      ,HumanComputerInteraction = '{}'
      ,LaboratoryEnvironments = '{}'
      ,Literacy = '{}'
      ,MathematicsInComputing = '{}'
      ,Multimedia = '{}'
      ,NetworkingDataCommunications = '{}'
      ,NonMajorCourses = '{}'
      ,ObjectOrientedIssues = '{}'
      ,OperatingSystems = '{}'
      ,ParallelProcessing = '{}'
      ,Pedagogy = '{}'
      ,ProgrammingLanguages = '{}'
      ,Research = '{}'
      ,Security = '{}'
      ,SoftwareEngineering = '{}'
      ,SystemsAnalysisAndDesign = '{}'
      ,UsingTechnologyInTheClassroom = '{}'
      ,WebAndInternetProgramming = '{}'
      ,Other = '{}'
      ,OtherDescription = '{}'
      ,ReviewsAcknowledged = '{}'
    WHERE ReviewerID = '{}' """.format(True, fname, lname, mIntial, email, affiliation, department, address, city, state, zipCode, phone, password,
        True if request.POST.__contains__('analysisOfAlgorithms') else False
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
           , otherType
           , False
           , reviewerID))
    
    messages.info(request, 'Reviewer Information modified')
    return redirect( 'maintainReviewers')

# Deletes a Reviewer from the CPMS database. This function handles the POST requests coming from the delete reviewer form
# from the corresponding maintainReviewers page
def deleteReviewers(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    ID = request.POST['exampleReviewerID']
    cursor = connection.cursor()
    cursor.execute("DELETE FROM dbo.Reviewer WHERE ReviewerID = '{}' ".format(ID))
    
    messages.info(request, 'Reviewer Deleted')
    return redirect( 'maintainReviewers')

# View function for the Review maintenance page. The page contains three forms used for Add/Modify/Delete actions on Rveiews. 
# Seperate functions are used to perform each action. This function handles GET requests to the corresponding maintainReviews page
def maintainReviews(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dbo.Review")
    context = {'reviews': dictfetchall(cursor)}
    return render(request, 'maintainReviews.html',context)

# Inserts a Review into the CPMS database. This function handles the POST requests coming from the insert review form
# from the corresponding maintainReviews page
def insertReviews(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    paperID = request.POST['examplePaperID']
    contentComments = request.POST['exampleContentComments']
    WDComments = request.POST['exampleWDComments']
    POPComments = request.POST['examplePOPComments']
    ORComments = request.POST['exampleORComments']
    reviewerID = request.POST['exampleReviewerID']
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO dbo.Review
           (PaperID
           ,ReviewerID
           ,AppropriatenessOfTopic
           ,TimelinessOfTopic
           ,SupportiveEvidence
           ,TechnicalQuality
           ,ScopeOfCoverage
           ,CitationOfPreviousWork
           ,Originality
           ,ContentComments
           ,OrganizationOfPaper
           ,ClarityOfMainMessage
           ,Mechanics
           ,WrittenDocumentComments
           ,SuitabilityForPresentation
           ,PotentialInterestInTopic
           ,PotentialForOralPresentationComments
           ,OverallRating
           ,OverallRatingComments
           ,ComfortLevelTopic
           ,ComfortLevelAcceptability
           ,Complete)
     VALUES
           ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' )
    """.format(
        paperID, reviewerID
      ,int(request.POST['AppropriatenessOfTopic'])
      ,int(request.POST['TimelinessOfTopic']) 
      ,int(request.POST['SupportiveEvidence']) 
      ,int(request.POST['TechnicalQuality']) 
      ,int(request.POST['ScopeOfCoverage']) 
      ,int(request.POST['CitationOfPreviousWork']) 
      ,int(request.POST['Originality']) 
      ,contentComments 
      ,int(request.POST['OrganizationOfPaper']) 
      ,int(request.POST['ClarityOfMainMessage']) 
      ,int(request.POST['Mechanics']) 
      ,WDComments
      ,int(request.POST['SuitabilityForPresentation']) 
      ,int(request.POST['PotentialInterestInTopic']) 
      ,POPComments
      ,int(request.POST['OverallRating']) 
      ,ORComments
      ,int(request.POST['ComfortLevelTopic']) 
      ,int(request.POST['ComfortLevelAcceptability']) 
      ,True if request.POST.__contains__('exampleIsComplete') else False
    ))
    messages.info(request, 'Review added')   
    return redirect( 'maintainReviews')

# Modifies a Review in the CPMS database. This function handles the POST requests coming from the update review form
# from the corresponding maintainReviews page
def updateReviews(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    reviewID = request.POST['exampleReviewID']
    contentComments = request.POST['exampleContentComments']
    WDComments = request.POST['exampleWDComments']
    POPComments = request.POST['examplePOPComments']
    ORComments = request.POST['exampleORComments']
    cursor = connection.cursor()
    cursor.execute(""" UPDATE dbo.Review SET 
      AppropriatenessOfTopic = '{}'
      ,TimelinessOfTopic = '{}'
      ,SupportiveEvidence = '{}'
      ,TechnicalQuality = '{}'
      ,ScopeOfCoverage = '{}'
      ,CitationOfPreviousWork = '{}'
      ,Originality = '{}'
      ,ContentComments = '{}'
      ,OrganizationOfPaper = '{}'
      ,ClarityOfMainMessage = '{}'
      ,Mechanics = '{}'
      ,WrittenDocumentComments = '{}'
      ,SuitabilityForPresentation = '{}'
      ,PotentialInterestInTopic = '{}'
      ,PotentialForOralPresentationComments = '{}'
      ,OverallRating = '{}'
      ,OverallRatingComments = '{}'
      ,ComfortLevelTopic = '{}'
      ,ComfortLevelAcceptability = '{}'
      ,Complete = '{}'
        WHERE ReviewID = '{}'
        """.format(
       int(request.POST['AppropriatenessOfTopic'])
      ,int(request.POST['TimelinessOfTopic']) 
      ,int(request.POST['SupportiveEvidence']) 
      ,int(request.POST['TechnicalQuality']) 
      ,int(request.POST['ScopeOfCoverage']) 
      ,int(request.POST['CitationOfPreviousWork']) 
      ,int(request.POST['Originality']) 
      ,contentComments 
      ,int(request.POST['OrganizationOfPaper']) 
      ,int(request.POST['ClarityOfMainMessage']) 
      ,int(request.POST['Mechanics']) 
      ,WDComments
      ,int(request.POST['SuitabilityForPresentation']) 
      ,int(request.POST['PotentialInterestInTopic']) 
      ,POPComments
      ,int(request.POST['OverallRating']) 
      ,ORComments
      ,int(request.POST['ComfortLevelTopic']) 
      ,int(request.POST['ComfortLevelAcceptability']) 
      ,True if request.POST.__contains__('exampleIsComplete') else False, reviewID ))
    messages.info(request, 'Review Updated')
    return redirect( 'maintainReviews')

# Deletes a Review from the CPMS database. This function handles the POST requests coming from the delete review form
# from the corresponding maintainReviews page
def deleteReviews(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    ID = request.POST['exampleReviewID']
    cursor = connection.cursor()
    cursor.execute("DELETE FROM dbo.Review WHERE ReviewID = '{}' ".format(ID))
    messages.info(request, 'Review Deleted')
    return redirect('maintainReviews')

# This function handles both GET and POST requests from the corresponding manage Paper/Review Acceptance page.
# The funtions gives the Admin user functionality for turning on/off  paper/review submission.
def managePaperReviewAcceptance(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        try:
            reviewA = request.POST['exampleReviewAcceptance']
            paperA = request.POST['examplePaperAcceptance']
            cursor = connection.cursor()
            cursor.execute("UPDATE dbo.Defaults SET EnabledReviewers = '{}', EnabledAuthors = '{}'".format(int(reviewA), int(paperA)))
            messages.info(request, 'Acceptance Updated')
        except:
            messages.error(request, 'An error occured while processing the form data, please redo the form correctly')

        return redirect('managePaperReviewAcceptance')
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM dbo.Defaults")
        Context = {'defaults': dictfetchall(cursor)}
        return render(request, 'managePaperReviewAcceptance.html', Context)

# This function handles both GET and POST requests from the corresponding match papers with reviewers page.
# This fucntion provides the admin user the functionality to view papers and reviewers and assign reviews for papers to the reviewers
def matchPaperWithReviewers(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        paperID = request.POST['examplePaperID']
        reviewerID  = request.POST['exampleReviewerID']
        cursor = connection.cursor()
        cursor.execute("INSERT INTO dbo.Review (PaperID, ReviewerID, Complete) VALUES ('{}', '{}', '{}')".format(paperID, reviewerID, False))
        messages.info(request, 'Paper matched with reviewer')
        return redirect('matchPaperWithReviewers' )
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM dbo.Paper")
        Context = {'papers': dictfetchall(cursor)}
        cursor.execute("SELECT * FROM dbo.Reviewer")
        Context['reviewers'] = dictfetchall(cursor)
        return render(request, 'matchPaperWithReviewers.html', Context)

# This function handles both GET and POST requests from the corresponding Authors Report page.
# This function displays the Authors Report
def authorsReport(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dbo.Author")
    context = {'authors': dictfetchall(cursor)}
    return render(request, 'authorsReport.html', context)

# This function handles both GET and POST requests from the corresponding Reviewers Comments Report page.
# This function displays the Reviewers Comments Report
def reviewersCommentsReport(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dbo.Review as rw, dbo.Reviewer as r, dbo.Paper as p WHERE rw.ReviewerID = r.ReviewerID AND rw.PaperID = P.PaperID")
    context = {'reviews': dictfetchall(cursor)}
    return render(request, 'reviewersCommentsReport.html', context)

# This function handles both GET and POST requests from the corresponding Reviewers Report page.
# This function displays the Reviewrs Report
def reviewersReport(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dbo.Reviewer")
    context = {'reviewers': dictfetchall(cursor)}
    return render(request, 'reviewersReport.html', context)

# This function handles both GET and POST requests from the corresponding Reviews Summary Report page.
# This function displays the Reviews Summary Report
def reviewsSummaryReport(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    cursor = connection.cursor()
    cursor.execute("""SELECT p.Title, AVG(rw.AppropriatenessOfTopic) as AppropriatenessOfTopic, AVG(rw.TimelinessOfTopic) as TimelinessOfTopic,
    AVG(rw.SupportiveEvidence) as SupportiveEvidence, AVG(rw.TechnicalQuality) as TechnicalQuality, AVG(rw.ScopeOfCoverage) as ScopeOfCoverage, 
    AVG(rw.CitationOfPreviousWork) as CitationOfPreviousWork, AVG(rw.Originality) as Originality, AVG(rw.OrganizationOfPaper) as OrganizationOfPaper, 
    AVG(rw.ClarityOfMainMessage) as ClarityOfMainMessage, AVG(rw.Mechanics) as Mechanics, AVG(rw.SuitabilityForPresentation) as SuitabilityForPresentation, 
    AVG(rw.PotentialInterestInTopic) as PotentialInterestInTopic, AVG(rw.OverallRating) as OverallRating, 
    p.Filename, (((AVG(rw.AppropriatenessOfTopic) + AVG(rw.PotentialInterestInTopic) / 2) * 0.5) + (AVG(rw.OverallRating)*0.5)) as WeightedScore
    FROM dbo.Review as rw, dbo.Paper as p
    WHERE rw.PaperID = p.PaperID
    GROUP BY rw.PaperID, p.Title, p.Filename
    """)
    context = {'reviews': dictfetchall(cursor)}
    return render(request, 'reviewsSummaryReport.html', context)