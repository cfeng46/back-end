#Intercept API

This repository is the back-end API for Intercept. Contained within is the Flask project that serves as the interface between the MongoDB database and the Angular front-end

#Methods

###questions()
Route: /questions  
Provides all questions in JSON format to front-end for display.

###organization()
Route: /organization  
Args: id: Optional  
If ID of an organization is provided, will return that organization's data. Otherwise, will return all organizations. 

###show\_survey\_results()
Route: /surveyOrgResults  
Args: id  
Retrieves all organizations that are relevant to needs determined by the given survey ID.
