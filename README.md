# Intercept API

This repository is the back-end API for Intercept. Contained within is the Flask project that serves as the interface between the MongoDB database and the Angular front-end

### API Endpoints
/survey
  * represent a data model Survey: a set of questions given to a user, depending on the category of choice
  * (method) GET: takes an optional query 'categoryId', returns a set of questions (example: '/survey?categoryId=3')

/record
 * represent a data model Record: a survey completed and submitted by user, comes with a set of tags extracted from the user responses
 * (method) GET: takes a query 'recordId', returns a record that is not protected with password (example: '/record?id=4')
 * (method) POST: add a record; takes body data that consists of user responoses and applicable tags, creates a new Record document in DB

/record/{Id}
 * For a protected record, user must provide a password, which means it would use a POST method; so to differenciate it from newly adding a  record, which uses '/record' with POST (see above), created an additional endpoint that takes a required URL parameter for the record ID (example: 'record/4')

(To be implemented)
/tag

/organization

