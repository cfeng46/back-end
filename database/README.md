# Query Methods

### get_questions()
Args:  
Returns all questions 

### insert_records()  
Args: location, populations, services, languages  
Inserts each collection of tags into the stored survey database

### get_org_by_id()
Args: id  
Retrieves a single org by the organization id

### get_orgs()
Args:  
Retrieves all organizations

### find_orgs_by_matching_tags()
Args: survey_id  
Retrieves organizations whose tags match those determined by the given survey

### get_orgs_near_location()
Args: orgs, survey_id  
Returns organizations that are geographically near the given location in the given survey

### find_orgs_with_one_service() 
Args: orgs, survey_id  
Returns oranizations from the list that match at least one tag as determined by the given survey

### update_password_by_id()  
Args: survey_id, new_password  
Updates the given survey's password

### get_survey_password()   
Args: password  
Retrieves the hashed password for the given survey
