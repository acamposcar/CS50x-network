function sendLike(post) {
  /*----------------
  Send email (POST)
  ----------------*/
  fetch(`/api/posts/${post.id.substr(5)}/new_like`, {
    method: 'POST',
    body: JSON.stringify({
      post: post.id.substr(5),
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      if (result.error) {
        console.log(result)
      } else { 
        console.log(result)
        post.querySelector('.post-like-count').textContent = result.like_count;
        post.querySelector('.post-like-heart').classList.toggle('liked');
      }
    });
}

function newComment(post) {
  /*----------------
  Send email (POST)
  ----------------*/
  fetch(`/api/posts/${post.id.substr(5)}/new_comment`, {
    method: 'POST',
    body: JSON.stringify({
      comment: post.querySelector('#id_content').value,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      if (result.error) {
        console.log(result)
      } else { 
        // Clear text from form
        post.querySelector('#id_content').value = "";

        // Update comments count
        post.querySelector('.post-comment-count').textContent = result.comment_count;

        // Update all comments to show the new one
        getComments(post);
      }
    });
}

function createCommentContainer(comment, post){

  container = post.querySelector('.container-comments');
  container.innerHTML = container.innerHTML + `
                      <div class="comment" id="comment_${ comment.id }">
                        <div class="post-header d-flex justify-content-between">
                            <a class="post-username" href="{% url 'user_profile' ${comment.user} %}">${comment.user}</a>
                            <span class="post-date" href="">${comment.timestamp}</span>
                        </div>
                        <div class="post-content">
                            ${comment.content.replace(/(\r\n|\n|\r)/g,"<br />")}
                        </div>
                      </div>
    `;
}

function deletePost(post) {
  /*----------------
  Send email (POST)
  ----------------*/
  fetch(`/api/posts/${post.id.substr(5)}/delete`, {
    method: 'DELETE',})
    .then((response) => response.json())
    .then((result) => {
      if (result.error) {
        //console.log(result)
      } else { 

        // Hide post
        post.style.display = 'none'

      }
    });
}

function editPost(post, editPopup) {
  /*----------------
  Send email (POST)
  ----------------*/
  content = editPopup.querySelector('#id_content').value.trim();
  fetch(`/api/posts/${post.id.substr(5)}/edit`, {
    method: 'POST',
    body: JSON.stringify({
      content: content,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      if (result.error) {
        //console.log(result)
      } else { 
        // Clear text from form
        

        // Hide popup and clear edit form content
        editPopup.style.display = 'none';
        editPopup.querySelector('#id_content').value = "";

        // Update post to show the new one
        post.querySelector('.post-content').innerText = content
        

      }
    });
}

function cancelEditPopup(editPopup){

  editPopup.querySelector('#id_content').value = "";
  editPopup.style.display = 'none';
}

function showEditPopup(post){
  postContent = post.querySelector('.post-content').innerText.trim();
  editPopup = document.querySelector('.edit-popup');
  editPopup.querySelector('#id_content').value = postContent;
  editPopup.style.display = 'block';
  console.log(editPopup)
  editPopup.onsubmit = () => {
    editPost(post, editPopup);
    return false;
  };

  editPopup.querySelector('.cancel-edit-button').onclick = () => {
    cancelEditPopup(editPopup);

  };
}


function getComments(post){
    fetch(`/api/posts/${post.id.substr(5)}/comments`)
    .then((response) => response.json())
    .then((comments) => {
      if (comments.error) {
          console.log(comments.error);
      } else {

        // Clear old comments from HTML
        post.querySelector('.container-comments').innerHTML = "";

        // Show all updated comments in HTML
          let i = 0;
          for (const comment of comments){
            createCommentContainer(comment, post);
            i++;
            if (i>2){
              post.querySelector('.post-comment-more').style.display = 'block';
              break;
            }
          }
      }
    });
}

function updateLikePost(post){
  // Add or remove likes
  post.querySelector('.post-likes-form').onsubmit = () => {
    sendLike(post);
    return false;
  };

  // Create new comment
  post.querySelector('.post-comment-form').onsubmit = () => {
    newComment(post);
    return false;
  };

  // Show comments 
  post.querySelector('.post-comments-button').onclick = () => {
    getComments(post);
    post.querySelector('.post-comments').classList.toggle('active');

  };
  
  // Show edit popup if the edit button exists (only is current user is the post author)
  if ( post.querySelector('.post-edit-button') !== null) {
      post.querySelector('.post-edit-button').onclick = () => {
        showEditPopup(post);
      };
  }
  if ( post.querySelector('.post-delete-button') !== null) {
      post.querySelector('.post-delete-button').onclick = () => {
        deletePost(post);
      };
  }
  
}


document.addEventListener('DOMContentLoaded', () => {
  // Use buttons to toggle between views
  
  // By default, load the inbox

  document.querySelectorAll('div.post').forEach(post => {
    updateLikePost(post);
  });
  
});
