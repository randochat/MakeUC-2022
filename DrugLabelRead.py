'''

Created by: Saaras Pakanati (Github Id: randochat)
Data: 22nd October(Techtober) 2022

Credits:
Anand Jagadeesan (https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/) 
Google (https://developers.google.com/calendar/api/guides/create-events)

'''

# Import required packages
from __future__ import print_function
from typing import Concatenate
import cv2
import pytesseract
import numpy as np
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/calendar']

def GoogleCalendarAppend(WarningsData, ExpiryDate):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the firsts
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Calling the Calendar API.
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        datetimevalStrt = ExpiryDate + 'T09:00:00-07:00'
        datetimevalEnd = ExpiryDate + 'T17:00:00-07:00'


        # Setting up the meta data for the event.
        event = {
        'summary': 'THROW AWAY THE MEDICATION',
        'location': '',
        'description': WarningsData,
        'start': {
            'dateTime': datetimevalStrt,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': datetimevalEnd,
            'timeZone': 'America/New_York',
        },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))


    except HttpError as error:
        print('An error occurred: %s' % error)



def ReadTheIMG(imagename):

    # Mention the installed location of Tesseract-OCR in your system
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\tesseract.exe"

    # Read image from which text needs to be extracted
    img = cv2.imread(imagename)

    # Image Processing
    lower = np.array([0, 0, 0])
    upper = np.array([100, 100, 100])
    gray = cv2.inRange(img, lower, upper)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_NONE)

    # Creating a copy of image
    im2 = gray.copy()

    # A text file is created and flushed
    file = open("recognized.txt", "w+")
    file.write("")
    file.close()

    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]
        
        # Open the file in append mode
        file = open("recognized.txt", "a")
        
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)
        
        # Appending the text into file
        file.write(text)
        file.write("\n")
        
        # Close the file
        file.close

    # Opening the file with the data.
    file = open("recognized.txt", "r")

    # Non extensive list of possible warnings by FDA.
    DrugWarningsName = ['DROWSINESS' , 'BREATHING']
    DrugWarningsLink = ['https://www.health.harvard.edu/medications/what-to-do-when-medication-makes-you-sleepy' , 
'https://medlineplus.gov/ency/article/000007.htm#:~:text=Loosen%20any%20tight%20clothing.,breath%20sounds%2C%20such%20as%20wheezing.']

    # Opening a new file with all the warnings in it for the Google Calendar Event.  
    WarningFile = open('Warnings.txt' , "a+")

    # Searching and adding the warnings to the list.
    for i in file.readlines():
        for j in i.split(" "):
            for k in DrugWarningsName:
                if k in j:
                    tempstr = str(DrugWarningsLink[DrugWarningsName.index(k)])
                    WarningDataIndividualList = [str(k) , ':' , str(tempstr) , '\n']
                    WarningDataIndividual = " ".join(WarningDataIndividualList)
                    WarningFile.write(WarningDataIndividual)
    WarningFile.close()
    WarningFile = open('Warnings.txt' , "r")
    WarningsData = WarningFile.read()
    print(WarningsData)
    WarningFile.close()

    # Calling the Google Calander Function to create an event.
    GoogleCalendarAppend(WarningsData, ExpiryDate)

#Test condition
imagenameinitial = input('Enter the name of the file')
ExpiryDate = input('Enter date of expiry in format YYYY-MM-DD')
ReadTheIMG(imagenameinitial)

# Purging the data for the next run.
WarningFile = open('Warnings.txt' , 'w')
WarningFile.write(' ')
WarningFile.close()

# End of code

########################################################################################