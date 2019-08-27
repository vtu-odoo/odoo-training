import csv  
with open('contact.csv', mode='w') as csv_file:  
	fieldnames = ['name', 'mobile', 'email']  
	writer = csv.DictWriter(csv_file, fieldnames=fieldnames)  
	writer.writeheader()  
	writer.writerow({'name': 'vishnu', 'mobile': '9512545108', 'email': 'vishnuthuletiya1111@gmail.com'})
	writer.writerow({'name': 'prabhu', 'mobile': '9687165361', 'email': 'prabhu@gmail.com'})  
	writer.writerow({'name': 'kalpesh', 'mobile': '5874658512', 'email': 'kalpesh@gmail.com'})  
	writer.writerow({'name': 'mahesh', 'mobile': '2545159875', 'email': 'mahesh@gmail.com'})  
	writer.writerow({'name': 'rajesh', 'mobile': '2545856595', 'email': 'rajeshthuletiya@gmail.com'})  
	writer.writerow({'name': 'babu', 'mobile': '4595857562', 'email': 'baburathava@gmail.com'})  
	writer.writerow({'name': 'mukesh', 'mobile': '5654721545', 'email': 'mukeshthuletiya@gmail.com'})  
	writer.writerow({'name': 'jatin', 'mobile': '9575453685', 'email': 'vekariyajatin@gmail.com'})  
	writer.writerow({'name': 'uttam', 'mobile': '4562739128', 'email': 'uttamrabari@gmail.com'})  
	writer.writerow({'name': 'hardik', 'mobile': '5645788923', 'email': 'hardik@gmail.com'})    
	
