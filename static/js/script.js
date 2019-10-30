const imageNames = [];
const fetchInterval = 60000; // in ms, so 60000 is every minute

const run = () => {
    getImageNames();
    window.setInterval(() => {
        getImageNames();
    }, fetchInterval);
}

const onClickLeftArrow = () => {
    let idx = getCurrentImgsIndex();
    if(idx < 1) {
        idx = 0;
    } else {
        idx -= 1;
    }
    showImage(imageNames[idx]);
}

const onClickRightArrow = () => {
    let idx = getCurrentImgsIndex();
    if(idx >= imageNames.length - 1) {
        idx = imageNames.length - 1;
    } else {
        idx += 1;
    }
    showImage(imageNames[idx]);
}

const checkAndChangeButtonVisibility = () => {
    let idx = getCurrentImgsIndex();
    if(idx === 0) {
        disableButtonById("leftArrow");
    } else {
        enableButtonById("leftArrow");
    }
    if(idx === imageNames.length - 1) {
        disableButtonById("rightArrow");
    } else {
        enableButtonById("rightArrow");
    }
}

const disableButtonById = (id) => {
    let btn = document.getElementById(id);
    if(btn) {
        btn.disabled = true;
    }
}

const enableButtonById = (id) => {
    let btn = document.getElementById(id);
    if(btn) {
        btn.disabled = false;
    }
}

const getCurrentImgsIndex = () => {
    let imgHolder = document.getElementById("img");
    if(imgHolder.children.length === 0) {
        console.log("there is no current image");
        return -1;
    }
    if(imgHolder.children.length != 2) {
        console.log("image holder holds invalid data");
        return -1;
    }
    let imgNode = imgHolder.children[1];
    if(!imgNode.src) {
        console.log("image has no src attribute");
        return -1;
    }
    let imgName = imgNode.getAttribute("src");
    return imageNames.indexOf(imgName);
}

const getImageNames = () => {
    getRequest("/images", onGetImageNames);
}

const onGetImageNames = (images) => {
    let imagesArray = JSON.parse(images);
    if ( ! Array.isArray(imagesArray)) {
        console.log("error, result was no array");
        return;
    }
    if (imagesArray.length === 0) {
        return;
    }
    imageNames.length = 0;
    imageNames.push(...imagesArray);
    let imgIdx = getCurrentImgsIndex();
    if(imgIdx === -1) {
        showImage(imageNames[0]);
    }
}

const showImage = (img) => {
    let imgHolder = document.getElementById("img");
    let imgNode = document.createElement("img");
    let imgInfo = getImageDateFromName(img);
    imgNode.src = img;
    removeChildrenFromNode(imgHolder);
    imgHolder.appendChild(imgInfo);
    imgHolder.appendChild(imgNode);
    checkAndChangeButtonVisibility();
}

const getImageDateFromName = (img) => {
    let imgInfo = document.createElement("div");
    let startIdx = img.lastIndexOf("/") + 1;
    let endIdx = img.lastIndexOf(".");
    imgInfo.innerHTML = img.substring(startIdx, endIdx);
    return imgInfo;
}

const removeChildrenFromNode = (node) => {
    let child = node.lastElementChild;
    while(child) {
        node.removeChild(child);
        child = node.lastElementChild;
    }
}

const getRequest = (endpoint, onSuccess) => {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState === 4) {
        if (this.status === 200) {
            onSuccess(this.responseText);
        } else {
            console.log(this.status);
        }
    }
  };
  xhttp.open("GET", endpoint, true);
  xhttp.send();
}

