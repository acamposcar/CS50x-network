function sendLike(post) {
  /*----------------
  Send email (POST)
  ----------------*/
  fetch(`api/posts/${post.id.substr(5)}/new_like`, {
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
        post.querySelector('.post-likes-heart').classList.add('liked')
      }
    });
}

function likePost(post){
  
  post.querySelector('.post-likes-form').onsubmit = () => {
    sendLike(post);
    return false;
  };
}

document.addEventListener('DOMContentLoaded', () => {
  // Use buttons to toggle between views

  // By default, load the inbox
  document.querySelectorAll('div.post').forEach(post => {
    likePost(post);

  })
});
