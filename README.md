-------
The idea is to develop an agent which generates sql code based on the columns and filters extracted and refers to the knowledge source for the sql code generation 
	Plan for the agent via RAG
	1. Ask/take/get input from user as pdf 
	2. Read the pdf and extract the column and send the column and filters to the user 
	3. Ask the user if the extracted columns and filters are suitable, if yes move to next step, else Take query 1 (regarding the correct column extraction) from the user
	4. Based on the query 1 create the response (say answer 1) and send to user again and repeat this till the extraction is complete
	5. Based on the extracted columns, create the sql code referring to the knowledge source, send this to the used and ask for the feed back (say query 2 is the feedback from the user)
	6. Take query 2 (regarding the query generation) from user 
	7. Then based on the and query 2 from the user, refer to the knowledge source again
	8. Take the feedback from the user and regenerate the result again and send to the user

