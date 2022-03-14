import { getComments } from './fetch.js';

document.addEventListener('DOMContentLoaded', () => {
  // Update post depending on the actions made by the user
  const post = document.querySelector('div.post');
  getComments(post, 'all');
  post.querySelector('.post-comments').classList.toggle('active');
});
