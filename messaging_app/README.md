# Messaging App

This is a Django-based messaging application built using the Django Rest Framework (DRF). The application allows users to send and receive messages within conversations. It includes API endpoints to manage users, conversations, and messages.

## Project Setup

### 1. Initialize a New Django Project
- **Objective**: Create a new Django project called `messaging_app`.
- **Steps**: 
  - Run `django-admin startproject messaging_app` to initialize the project.

### 2. Install Django Rest Framework (DRF)
- **Objective**: Install and configure Django Rest Framework (DRF) to handle API functionalities.
- **Steps**:
  - Install DRF by running:
    ```bash
    pip install djangorestframework
    ```
  - Add `'rest_framework'` to the `INSTALLED_APPS` list in `settings.py`.

### 3. Create a New App for Messaging
- **Objective**: Create an app called `chats` for handling messaging functionality.
- **Steps**:
  - Run `python manage.py startapp chats` to create the app.
  - Add `'chats'` to the `INSTALLED_APPS` list in `settings.py`.

## Models

The project uses the following models for users, conversations, and messages:

- **User Model**: An extension of Django's `AbstractUser` to include additional user information.
- **Conversation Model**: Represents a conversation between users.
- **Message Model**: Represents a message within a conversation, containing the sender and the associated conversation.

### Location: `messaging_app/chats/models.py`

## Serializers

Serializers are used to define how the data will be structured for API responses and requests. The application uses serializers for users, conversations, and messages, ensuring that nested relationships (e.g., messages within a conversation) are handled properly.

### Location: `messaging_app/chats/serializers.py`

## API Endpoints

The project provides the following API endpoints:

- **GET /api/conversations/**: Lists all conversations.
- **GET /api/messages/**: Lists all messages.
- **POST /api/conversations/**: Creates a new conversation.
- **POST /api/messages/**: Sends a message to an existing conversation.

### Location: `messaging_app/chats/views.py`

## URL Routing

The URLs for conversations and messages are automatically generated using Django Rest Framework's `DefaultRouter`. The API is accessible via the `/api/` prefix.

### Location: `messaging_app/chats/urls.py`

## Running the Application

To run the application locally and test the functionality:

1. Apply migrations to set up the database:
   ```
   python manage.py makemigrations
   python manage.py migrate
    ```
2. Start the development server:
    ```
python manage.py runserver
    ```
3. Access the API at http://127.0.0.1:8000/api/.
    
## Debugging Errors
If you encounter any errors, carefully read the error messages, resolve any issues in the code, and rerun the server.
    
## License
This project is licensed under the MIT License - see the LICENSE file for details.







