# Intercept API

This repository is the back-end API for Intercept. Contained within is the Flask project that serves as the interface between the MongoDB database and the Angular front-end

# Methods

### create_password()
Route: /createPassword  
Method: GET   
Args: id, password  
Allows users to anonymously store survey results for later retreival

### login()
Route: /login   
Method: GET   
Args: id, password  
Allows the user to enter a previous survey ID and pasword, and view saved results.

### organization()
Route: /organization  
Method: GET   
Args: id: Optional  
If ID of an organization is provided, will return that organization's data. Otherwise, will return all organizations. 

### questions()
Route: /questions  
Method: GET   
Provides all questions in JSON format to front-end for display.

### save_survey()  
route /surveySubmit  
Method: POST  
Args: Survey submit form  
Saves the survey with the password and all tags

### show_survey_results()
Route: /surveyOrgResults  
Method: GET   
Args: id  
Retrieves all organizations that are relevant to needs determined by the given survey ID


