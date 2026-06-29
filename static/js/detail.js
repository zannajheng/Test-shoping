const middle = document.querySelector('.goods_detail_pic')
const layer = document.querySelector('.layer')
const tage = document.querySelector('.tage')
/*middle.addEventListener('mouseenter', function (){
    tage.style.display = 'block'
    layer.style.display = 'block'
})*/
/*
middle.addEventListener('mouseleave', function () {
    layer.style.display = 'none'
    tage.style.display = 'none'
})
middle.addEventListener('mousemove', function (e) {
    let x = e.pageX - middle.getBoundingClientRect().left
    let y = e.pageY - middle.getBoundingClientRect().top - document.documentElement.scrollTop
    if (x >= 0 && x <= 350 && y >= 0 && y <= 350) {
        let mx = 0, my = 0
        if (x < 75) mx = 0
        if (x >= 75 && x <= 275) mx = x - 75
        if (x > 275) mx = 200
        if (y < 75) my = 0
        if (y >= 75 && y <= 275) my = y - 75
        if (y > 275) my = 200
        layer.style.left = mx + 'px'
        layer.style.top = my + 'px'
        tage.style.backgroundPositionX = -2 * mx + 'px'
        tage.style.backgroundPositionY = -2 * my + 'px'
      }
})
*/
