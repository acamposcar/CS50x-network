export function createCommentContainer(comment, post) {
  const container = post.querySelector('.container-comments');
  container.innerHTML += `

                      
                      <div class="comment" id="comment_${comment.id}">
                        <div class="d-flex gap-2">
                          <img class="mt-3" width="14" height="14" src='/static/network/icons/corner-down-right.svg' alt="Delete Post">
                          <div>
                          <div class="post-header d-flex align-items-center gap-2 user-avatar">
                            <img class="comment-image" src="${ comment.profile_image }" alt="Profile Image">
                            <div>
                                <div class="d-flex align-items-baseline gap-1">
                                  <a class="post-name" href="/users/${comment.username}">${comment.first_name} ${ comment.last_name }</a>
                                  <a class="post-username" href="/users/${comment.username}"><small>@${ comment.username }</small></a>
                                  
                                </div>
                                <span class="post-date"><small>${ comment.timestamp }</small></span>
                              </div>  
                          </div>  
                          <div class="comment-content">
                            ${comment.content.replace(/(\r\n|\n|\r)/g, '<br />')}
                          </div>
                        </div>
                        </div>
                      </div>
    `;
}


export function getCookie(name) {
  /**
    *  Get cookie by name
    *  Used to get csfr token
    *  From: https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
    */
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export function removeFadeOut( element, speed ) {
  /**
    *  Remove element with transition
    *  From: https://stackoverflow.com/a/33424474/12474129
    */
    const seconds = speed/1000;
    element.style.transition = "opacity "+seconds+"s ease";

    element.style.opacity = 0;
    setTimeout(function() {
        element.remove();
    }, speed);
}