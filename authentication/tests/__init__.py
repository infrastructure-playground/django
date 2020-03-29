registration_data = {'username': 'armadadean',
                     'password': 'pass1234',
                     'confirm_password': 'pass1234',
                     'email': 'armadadean@yahoo.com',
                     'first_name': 'Dean Christian',
                     'last_name': 'Armada'}
create_user_data = registration_data.copy()
del create_user_data['confirm_password']
login_credentials = {'username': 'armadadean', 'password': 'pass1234'}
