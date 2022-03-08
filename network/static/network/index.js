function getAllPosts() {
  /*----------------
  Gets email information from database
  ----------------*/
    document.querySelector('form').onsubmit = () => {
    createNewPost();
    return false;
  };
fetch(`/api/posts`)
    .then((response) => response.json())
    .then((posts) => {

      if (posts.error) {
          pass
        // document.querySelector('#alert-email').style.display = 'block';
        // document.querySelector('#alert-email').textContent = emails.error;
      } else if (posts.length !== 0) {
        posts.forEach((post) => createPostContainer(post));
      } else {
        pass
        // document.querySelector('#no-emails').style.display = 'flex';
      }
    });
}

function createPostContainer(post) {
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


  document.querySelector('.container-posts').appendChild(postContainer);
}


/* --------------------
CREATE NEW POST
 -----------------------*/

function createNewPost() {
  /*----------------
  Send email (POST)
  ----------------*/
  fetch('/api/new_post', {
    method: 'POST',
    body: JSON.stringify({
      content: document.querySelector('#new-post-content').value,
      image_url: document.querySelector('#new-post-image').value,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      if (result.error) {
        document.querySelector('#alert-compose').style.display = 'block';
        document.querySelector('#alert-compose').textContent = result.error;
      } else {
        getAllPosts();
      }
    });
}



document.addEventListener('DOMContentLoaded', () => {
  // Use buttons to toggle between views

  // By default, load the inbox
  pass

})

