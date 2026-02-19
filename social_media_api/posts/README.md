* Post API Documentation
*** 
This API provides a full backend for the social media posts
allowing users to post and interact via comments.

🔐 Authentication
This API uses JWT (JSON Web Tokens).
To access protected endpoints, include the following header in your requests:
Authorization: Bearer <your_access_token>

Endpoint,Method,Auth Required,Description
/api/accounts/register/,POST,No,Create a new user account.
/api/accounts/login/,POST,No,Exchange credentials for Access & Refresh tokens.