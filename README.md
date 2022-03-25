# CS50x-network

### CS50x Web Programming - Project 4 - Newtork

Design a Twitter-like social network website for making posts and following users.

- [Specifications](https://cs50.harvard.edu/web/2020/projects/4/network/)
- [Specifications Screencast](https://www.youtube.com/watch?v=1aWwQCOqypo)

## Live Demo

[Live Demo](https://acampos-cs50x-network.herokuapp.com/)

## Screenshots

- ### Pagination
![pagination](https://user-images.githubusercontent.com/9263545/160129870-052292dd-d01c-4ff9-b9f4-cdeefc2bec03.gif)

- ### New post, edit post and delete post
![new edit delete](https://user-images.githubusercontent.com/9263545/160129858-1bb63f2f-00a6-4f69-bb07-1b65d1bf03d5.gif)

- ### Likes and comments
![like comment](https://user-images.githubusercontent.com/9263545/160129882-578dae18-29a5-4cbc-92a2-202e7269c3f6.gif)

- ### Follow
![follow unfollow](https://user-images.githubusercontent.com/9263545/160129827-162f29c3-714e-475a-9e56-f0f83b66487e.gif)

- ### Profiles
![profile](https://user-images.githubusercontent.com/9263545/160129842-de761a73-8b2d-4f5f-8569-24feab61b625.gif)


## Installation

1. Clone the project

2. Install all necessary dependencies
    ```python
        pip3 install -r requirements.txt
    ```

3. Migrate database
    ```python
        python3 manage.py migrate
    ```

4. Run Django server
    ```python
        python3 manage.py runserver
    ```
