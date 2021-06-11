# HouseMates
An application which allows users to create a virtual space with their roommates, then track &amp; manage expenses, store a running tally of who owes money to whom, and track ownership of who owns what. This python-based project utilizes Django web framework, including user registration, validation, and password encryption. 


## **Minumum viable product:**
- Users can create an account
- Users can then create a virtual house and invite roommates
    - Inviting roommates will require a notification persistance system
- A user can prompt a purchase (such as a microwave) and other people within their virtual house can opt to help with the purchase.
    - Will also utilize notification system
- The application with then track and log the cost of the item, along with the amount owed by other people.
- Users can read past purchases, including item type, cost, time of purchase, and ownership


## **Additional optional features:**
- Link accounts with paypal/venmo API to settle balances
- Allow amazon.com links as a viable alternative to manual form input (rather than typing out the item name and cost)
- Allow for recurring bills (such as internet bill split between all roommates, but is due to a single user)
- Notification and calandar system to prompt due dates
- View and sort permanent items (such as appliances)
- Categorize all expenses and provide a breakdown report
- Include user profile section to give ability to track personal bills
- Include a chat system
- Include chore notifications