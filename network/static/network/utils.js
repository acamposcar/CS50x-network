export function createCommentContainer(comment, post) {
  const container = post.querySelector('.container-comments');
  container.innerHTML += `
                      <div class="comment" id="comment_${comment.id}">
                        <div class="post-header d-flex justify-content-between">
                            <a class="post-username" href="{% url 'user_profile' ${comment.user} %}">${comment.user}</a>
                            <span class="post-date" href="">${comment.timestamp}</span>
                        </div>
                        <div class="post-content">${comment.content.replace(/(\r\n|\n|\r)/g, '<br />')}
                        </div>
                      </div>
    `;
}

export function avatarChangeColor(name) {
  /**
    *  Transform any string into a HEX Color
    *  From: https://stackoverflow.com/a/17880920/12474129
    */
  const n = 'abcdefghijklmnopqrstuvwxyz'.split('');
  const r = name
    .split('')
    .map((e) => n.indexOf(e))
    .join('');
  const l = parseFloat(`0.${(r * r * 1000).toString().replace(/^0/, '')}`);
  return `#${Math.floor(l * 16777215).toString(16)}`;
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
