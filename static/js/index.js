window.onscroll = function () {
    const toolkitItem = document.querySelector('.toolkit_item:last-child');
    if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
        toolkitItem.style.display = "block";
    } else {
        toolkitItem.style.display = "none";
    }
}

document.querySelector('.toolkit_item:last-child').onclick = function () {
    window.scrollTo({top: 0, behavior: 'smooth'});
};
(function () {
    const list = document.querySelector('.center_con ul')
    list.addEventListener('click', function (e) {
        console.log(document.querySelector(`.list_${e.target.className}`).offsetTop)
        top_list = document.querySelector(`.list_${e.target.className}`).offsetTop
        console.log(top_list)
        document.documentElement.scrollTop = top_list
    })
})()