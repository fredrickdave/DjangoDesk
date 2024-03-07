# DjangoDesk

DjangoDesk is a simple and elegant help desk ticketing system built with Django. It allows users to create, update, assign, and manage tickets.

## Features

- User authentication and authorization
- Ticket creation, assignment, and status tracking
- File attachments support for tickets
- Search and filter tickets by keywords, categories, statuses, and more
- Responsive design and mobile-friendly interface
- Time Zone support

## Upcoming Features

- Email notifications and replies
- Improved Dashboard with statistics and charts
- Rich text editor for ticket descriptions and comments
- Automated Ticket workflow and monitoring
- And more...

## Installation

To install DjangoDesk, you need to have Python 3.8 or higher and pip installed on your system. You also need to clone this repository or download the zip file.

1. Clone this repository: `git clone https://github.com/fredrickdave/DjangoDesk.git`
2. Change directory to the project folder: `cd DjangoDesk`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
5. Install the required dependencies: `pip install -r requirements.txt`
6. Create a .env file in the project root directory and add the following environment variables:
   - `SECRET_KEY=your_secret_key`
   - `DEBUG=True`
   - `ALLOWED_HOSTS=\*`
   - `DATABASE_URL=your_DB_URL`
7. Initialize the database: `python manage.py migrate`
8. Create a superuser account: `python manage.py createsuperuser`
9. Run the application: `python manage.py runserver`
10. Open your browser and go to http://127.0.0.1:8000

## Usage

To run the Django server, use the following command:

python manage.py runserver

Then, open your browser and go to http://127.0.0.1:8000/ to access the web app. You can log in with your superuser credentials or register for a new user account. You can also access the admin panel at http://127.0.0.1:8000/admin/.

To create a ticket, click on the “New Ticket” button on the navbar. You can fill in the ticket details, such as the subject, description, category, priority, and customer email. You can also attach files to the ticket. Once you create the ticket.

To view and manage your tickets, click on the “My Tickets” button on the navbar. You can see the list of tickets assigned to you, as well as their statuses and categories. You can also search and filter tickets by keywords, categories, and statuses. To view the details of a ticket, click on its subject. You can see the ticket description, comments, and attachments. You can also change the ticket status, details, and category. You can also add comments to the ticket if you need to add more details.

To view the Account Profile and Settings, click on the "Account" button on the navbar. Here, you can modify your account details, change email, reset password, and set your preferred Time Zone.

## Live Demo Link

The app is hosted on a free instance on Render, so please allow a minute or two for the web app to initially load when you open the Live Demo link.

Link: https://djangodesk.onrender.com
