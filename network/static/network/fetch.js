import { createCommentContainer, getCookie } from './utils.js';

export function updateLike(post) {
  /*----------------
  Send email (POST)
  ----------------*/
  const csrftoken = getCookie('csrftoken');

  fetch(`/posts/${post.id.substr(5)}`, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrftoken },
    body: JSON.stringify({
      post: post.id.substr(5),
    }),

  })
    .then((response) => response.json())
    .then((result) => {
      if (result.error) {
        console.log(result);
      } else {

        if (result.like_count === 1) {
          post.querySelector('.post-like-count').textContent = `${result.like_count} Like`;
        } else {
          post.querySelector('.post-like-count').textContent = `${result.like_count} Likes`;
        }
        post.querySelector('.post-like-heart').classList.toggle('liked');
      }
    });
}

export function createComment(post) {
  /*----------------
  Create new comment (POST)
  ----------------*/
  const csrftoken = getCookie('csrftoken');

  fetch(`/posts/${post.id.substr(5)}/comments`, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrftoken },
    body: JSON.stringify({
      comment: post.querySelector('#id_content').value.trim(),
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      if (result.error) {
        console.log(result);
      } else {
        // Clear text from form
        post.querySelector('#id_content').value = '';

        // Update comments count
        if (result.comment_count === 1) {
          post.querySelector('.post-comment-count').textContent = `${result.comment_count} Comment`;
        } else {
          post.querySelector('.post-comment-count').textContent = `${result.comment_count} Comments`;
        }
        

        // Update all comments to show the new one
        getComments(post);
      }
    });
}

export function deletePost(post, deletePopup) {
  /*----------------
  Send email (POST)
  ----------------*/
  const csrftoken = getCookie('csrftoken');

  fetch(`/posts/${post.id.substr(5)}`, {
    method: 'DELETE',
    headers: { 'X-CSRFToken': csrftoken },
  })
    .then((response) => response.json())
    .then((result) => {
      if (result.error) {
        // console.log(result)
      } else {
        // Hide popup
        deletePopup.style.display = 'none';
        // Hide post
        post.style.display = 'none';
      }
    });
}

export function editPost(post, editPopup) {
  /*----------------
  Send email (POST)
  ----------------*/
  const csrftoken = getCookie('csrftoken');

  const content = editPopup.querySelector('#id_content').value.trim();
  fetch(`/posts/${post.id.substr(5)}`, {
    method: 'PUT',
    headers: { 'X-CSRFToken': csrftoken },
    body: JSON.stringify({
      content,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      if (result.error) {
        // console.log(result)
      } else {
        // Clear text from form

        // Hide popup and clear edit form content
        editPopup.style.display = 'none';
        editPopup.querySelector('#id_content').value = '';

        // Update post to show the new one
        post.querySelector('.post-content').innerText = content;
      }
    });
}

export function getComments(post, quantity) {
  fetch(`/posts/${post.id.substr(5)}/comments`)
    .then((response) => response.json())
    .then((comments) => {
      if (comments.error) {
        console.log(comments.error);
      } else {
        // Clear old comments from HTML
        post.querySelector('.container-comments').innerHTML = '';

        // Hide 'more comments button'
        post.querySelector('.post-comment-more').style.display = 'none';

        let i = 0;
        for (const comment of comments) {
          createCommentContainer(comment, post);
          i++;

          // Show last {quantity} comments or all
          if (i > quantity - 1 && quantity !== 'all') {
            // Show 'more comments button' if comment count is bigger than quantity
            post.querySelector('.post-comment-more').style.display = 'block';
            break;
          }
        }
      }
    });
}
