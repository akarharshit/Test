1. This is my user registration api
2. In this we use django,django-rest-framework
3. In this Pillow library is used for image recognition
4. In views.py of app(user_roles_app) there are three api one is to register in which there are two roles (admin and normal)
   and here username is unique field
      Url : (http://127.0.0.1:8000/register/)
5. By adding username,password,and role user should able to register successfully and will get the authentication token and this token i   Is  used further to check whether the user is admin or normal
6. In profile api user should able to get the profile and post the profile
7. In grant permission api admin should grant the permission to normal user
     url : (http://localhost:8000/grant-permission/
     )
8. postman collection is also attaching with this repository.