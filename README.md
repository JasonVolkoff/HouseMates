# HouseMates
An application which allows users to create a virtual space with their roommates, then track &amp; manage expenses, store a running tally of who owes money to whom, and track ownership of who owns what. This python-based project utilizes Django web framework, including user registration, validation, and password encryption. 

<p align="center">
  <img width="100%" src="https://github.com/JasonVolkoff/HouseMates/blob/main/ezgif.com-gif-maker.gif" alt="animated" />
</p>

## Running the project

After cloning the project: `https://github.com/JasonVolkoff/HouseMates.git`, create and activate your virtual environment within your terminal
#### Unix/macOS:
```
python3 -m venv env
source env/bin/activate
```
#### Windows
```
py -m venv env
.\env\Scripts\activate
```
Next install dependencies located in the requirements.txt

`pip install -r requirements.txt`

Navigate to `.\HouseMates\housemates_proj\` directory within your terminal.

Lastly, run migrations command and start your server
```
py manage.py migrate
py manage.py runserver
```
From here, you can view the project on localhost:8000 in your browser by default

## **Minumum viable product:**
- Users can create an account
- Users can then create a virtual house and invite roommates
    - Inviting roommates will require a notification persistance system
- A user can prompt a purchase (such as a microwave) and other people within their virtual house can opt to help with the purchase.
    - Will also utilize notification system
- The application with then track and log the cost of the item, along with the amount owed by other people.
- Users can read past purchases, including item type, cost, time of purchase, and ownership


## **Features to add in the future:**
- Link accounts with paypal/venmo API to settle balances
- Allow amazon.com links as a viable alternative to manual form input (rather than typing out the item name and cost)
- Allow for recurring bills (such as internet bill split between all roommates, but is due to a single user)
- Notification and calandar system to prompt due dates
- View and sort permanent items (such as appliances)
- Categorize all expenses and provide a breakdown report
- Include user profile section to give ability to track personal bills
- Include a chat system
- Include chore notifications
- Add edit profile, edit house, and remove user privaleges 

