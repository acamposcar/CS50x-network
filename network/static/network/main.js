import {
  updateLike,
  createComment,
  editPost,
  deletePost,
  getComments,
} from './fetch.js';

import {
  avatarChangeColor,
} from './utils.js';


export function showEditPopup(post) {
  /**
    *  Show popup to edit post
    */
  const postContent = post.querySelector('.post-content').innerText.trim();
  const editPopup = document.querySelector('.edit-popup');
  editPopup.querySelector('#id_content').value = postContent;
  editPopup.style.display = 'block';

  // Edit button
  editPopup.onsubmit = () => {
    editPost(post, editPopup);
    return false;
  };

  // Cancel button
  editPopup.querySelector('.cancel-edit-button').onclick = () => {
    editPopup.querySelector('#id_content').value = '';
    editPopup.style.display = 'none';
  };
}

export function showDeletePopup(post) {
  /**
    *  Show popup to delete post
    */
  const deletePopup = document.querySelector('.delete-popup');
  deletePopup.style.display = 'block';

  // Delete button
  deletePopup.onsubmit = () => {
    deletePost(post, deletePopup);
    return false;
  };
  // Cancel button
  deletePopup.querySelector('.cancel-delete-button').onclick = () => {
    deletePopup.style.display = 'none';
  };
}


function updatePost(post) {
  // Add or remove likes
  if (post.querySelector('.post-likes-form') !== null) {
    post.querySelector('.post-likes-form').onsubmit = () => {
      updateLike(post);
      return false;
    };
  }

  // Create new comment
  if (post.querySelector('.form-comment') !== null) {
    post.querySelector('.form-comment').onsubmit = () => {
      createComment(post);
      return false;
    };
  }

  // Show comments
  if (post.querySelector('.post-comments-button') !== null) {
    post.querySelector('.post-comments-button').onclick = () => {
      getComments(post, 3);
      post.querySelector('.post-comments').classList.toggle('active');
    };
  }

  // Show edit popup
  if (post.querySelector('.post-edit-button') !== null) {
    post.querySelector('.post-edit-button').onclick = () => {
      showEditPopup(post);
    };
  }

  // Show delete popup
  if (post.querySelector('.post-delete-button') !== null) {
    post.querySelector('.post-delete-button').onclick = () => {
      showDeletePopup(post);
    };
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Update post depending on the actions made by the user
  document.querySelectorAll('div.post').forEach((post) => {
    updatePost(post);
  });

  // Change avatar color depending on username
  document.querySelectorAll('.user-avatar').forEach((item) => {
    const username = item.querySelector('.post-username').textContent;
    item.querySelector('.avatar').style.fill = avatarChangeColor(username);
  });
});
