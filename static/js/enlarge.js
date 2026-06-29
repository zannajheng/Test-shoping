export  function enlargeImage(imageId) {
      var overlay = document.querySelector(".overlay");
      var enlargedImg = document.getElementById("enlargedImg");

      var imgUrl = document.getElementById(imageId);

      enlargedImg.src = imgUrl.src;
      console.log(imgUrl.src);
      overlay.style.display = "flex";
    }