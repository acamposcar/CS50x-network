function getAllPosts() {
  /*----------------
  Gets email information from database
  ----------------*/
fetch(`/posts`)
    .then((response) => response.json())
    .then((posts) => {
        console.log(posts)
      if (posts.error) {
          pass
        // document.querySelector('#alert-email').style.display = 'block';
        // document.querySelector('#alert-email').textContent = emails.error;
      } else if (posts.length !== 0) {
        posts.forEach((post) => createPost(post));
      } else {
        pass
        // document.querySelector('#no-emails').style.display = 'flex';
      }
    });
}

function createPost(post) {
  /*----------------
  Creates email container for every email
  ----------------*/

  // If the mail has already been read, add the class 'read'
    const postContainer = document.createElement('div');
    postContainer.classList.add('post-container');

    const user = document.createElement('div');
    user.classList.add('post-user');
    user.textuser = post.user;
    postContainer.appendChild(user);

    const content = document.createElement('div');
    content.classList.add('post-content');
    content.textContent = post.content;
    postContainer.appendChild(content);

    const time = document.createElement('div');
    time.classList.add('post-time');
    time.textContent = post.timestamp;
    postContainer.appendChild(time);


  document.querySelector('.container').appendChild(postContainer);
}

document.addEventListener('DOMContentLoaded', () => {
  // Use buttons to toggle between views

  // By default, load the inbox
  getAllPosts();
});

