from CPMS.helper_functions import validateUserDetails
from decimal import Context
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.models import User, auth
from django.core.exceptions import PermissionDenied, RequestAborted
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

#  Implemention file for the Reviewer View of the CPMS website. View function for each url call in the Reviewer view is found here.

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

# This function handles both GET and POST requests from the corresponding reviewer download papers page.
# The function provides a list of downloadable links for the assigned papers. 
def reviewerDownloadPapers(request):
    if not request.user.is_staff:
        raise PermissionDenied
    fs = FileSystemStorage()
    cursor = connection.cursor()
    cursor.execute("SELECT p.FileNameOriginal FROM  dbo.Review as rw, dbo.Reviewer as r, dbo.Paper as p WHERE p.PaperID = rw.PaperID AND r.ReviewerID = rw.ReviewerID AND r.EmailAddress = '{}'".format(str(request.user.email)))
    context = {'links': [{}]}
    context['links'].pop()
    for review in dictfetchall(cursor):
        context['links'] += {fs.url(review['FileNameOriginal'])}
    return render(request, 'reviewerDownloadPapers.html', context)

# This function handles both GET and POST requests from the corresponding Reviewer Modify Info page.
# The functions lets the user modify their information stored in the CPMS database and the Django User backend
def reviewerModifyInfo(request):
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method =='POST':
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
            return redirect('reviewerModifyInfo')
        if User.objects.filter(username=email).exists() and email != str(request.user.email):
            messages.error(request, 'email address already in use with a different account')
            return redirect('reviewerModifyInfo')
        else:
            request.user.first_name = fname
            request.user.last_name = lname
            request.user.email = email
            request.user.set_password(password)
            request.user.username = email
            request.user.save()
            auth.login(request, request.user)
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
    WHERE EmailAddress = '{}' """.format(True, fname, lname, mIntial, email, affiliation, department, address, city, state, zipCode, phone,
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
           , str(request.user.email)))
        messages.info(request, 'Information modified')
        return redirect('reviewerModifyInfo')
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM dbo.Reviewer WHERE EmailAddress = '{}'".format(str(request.user.email)))
        Context = {'reviewers': dictfetchall(cursor)}
        return render(request, 'reviewerModifyInfo.html', Context)

# This function handles both GET and POST requests from the corresponding Reviewer Register to Review Paper page.
# The function lets a user register to review papers. The form bacomes inactive once the registration is done
def reviewerRegisterToReviewPapers(request):
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method =='POST':
        address = request.POST['exampleAddress']
        affiliation = request.POST['exampleAffiliation']
        department = request.POST['exampleDepartment']
        city = request.POST['exampleCity']
        state = request.POST['exampleState']
        zipCode = request.POST['exampleZipCode']
        phone = request.POST['examplePhone']
        otherType = request.POST['exampleOtherType'] 
        valid = validateUserDetails(state, zipCode, "a", phone, '0')
        if valid != True:
            messages.error(request, valid)
            return redirect('reviewerRegisterToReviewPapers')
        cursor = connection.cursor()
        cursor.execute("""UPDATE dbo.Reviewer
   SET Active = '{}'
      ,Affiliation = '{}'
      ,Department = '{}'
      ,Address = '{}'
      ,City = '{}'
      ,State = '{}'
      ,ZipCode = '{}'
      ,PhoneNumber = '{}'
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
    WHERE EmailAddress = '{}' """.format(True, affiliation, department, address, city, state, zipCode, phone,
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
           , str(request.user.email)))
        messages.info(request,'Registration Successful')
        return redirect('reviewerRegisterToReviewPapers')
    else:
        cursor = connection.cursor()

        cursor.execute("SELECT FirstName, LastName, MiddleInitial, Affiliation FROM dbo.Reviewer WHERE EmailAddress = '{}'".format(str(request.user.email)))
        context = {'reviewers': dictfetchall(cursor)} 
        return render(request, 'reviewerRegisterToReviewPapers.html', context)

# This function handles both GET and POST requests from the corresponding Reviewer Review Papers page.
# This function provides the user with the Paper Review form. 
def reviewerReviewPapers(request):
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        titleID = int(request.POST['examplePaperID'])
        contentComments = request.POST['exampleContentComments']
        WDComments = request.POST['exampleWDComments']
        POPComments = request.POST['examplePOPComments']
        ORComments = request.POST['exampleORComments']
        cursor = connection.cursor()
        cursor.execute("SELECT ReviewerID FROM dbo.Reviewer WHERE EmailAddress = '{}'".format(str(request.user.email)))
        reviewerInfo = dictfetchall(cursor)
        reviewerID = reviewerInfo[0]['ReviewerID']
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
        WHERE PaperID = '{}' AND ReviewerID ='{}'
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
      ,int(request.POST['ClarityOfTheMainMessage']) 
      ,int(request.POST['Mechanics']) 
      ,WDComments
      ,int(request.POST['SuitabilityForPresentation']) 
      ,int(request.POST['PotentialInterestInTopic']) 
      ,POPComments
      ,int(request.POST['OverallRating']) 
      ,ORComments
      ,int(request.POST['ComfortLevelTopic']) 
      ,int(request.POST['ComfortLevelAcceptability']) 
      ,True, titleID, reviewerID ))
        messages.info(request, 'Review Submitted')
        return redirect('reviewerReviewPapers')
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT p.PaperID, p.Title FROM dbo.Review as rw, dbo.Paper as p, dbo.Reviewer as r WHERE rw.PaperID = p.PaperID AND rw.ReviewerID = r.ReviewerID AND r.EmailAddress = '{}' AND rw.Complete = 0 ".format(str(request.user.email)))
        Context = {'papers': dictfetchall(cursor)}
        cursor.execute("SELECT EnabledReviewers FROM dbo.Defaults")
        Context['Defaults'] = (dictfetchall(cursor))[0]
        return render(request, 'reviewerReviewPapers.html', Context)

