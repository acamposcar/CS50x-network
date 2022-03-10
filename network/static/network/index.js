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


function showComments (post) {

  const commentsDisplay = post.querySelector('.post-comments').style.display;
  
  if (commentsDisplay === 'block') {
    post.querySelector('.post-comments').style.display = 'none';
  } else {
    post.querySelector('.post-comments').style.display = 'block';
  }

}
function updateLikePost(post){
  post.querySelector('.post-likes-form').onsubmit = () => {
    sendLike(post);
    return false;
  };

  post.querySelector('.post-comments-button').onclick = () => {
    showComments(post);
    showCommentsReact(post);
  };

}


document.addEventListener('DOMContentLoaded', () => {
  // Use buttons to toggle between views
  
  // By default, load the inbox

  document.querySelectorAll('div.post').forEach(post => {
    updateLikePost(post);
  });
  
});
