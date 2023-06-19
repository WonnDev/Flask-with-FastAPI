/* Product */
// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();

function openDetails(evt, menuItem) {
    // Declare all variables
    var i, tabcontent, tablinks;
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(menuItem).style.display = "block";
    evt.currentTarget.className += " active";
}
/*slick slide*/

$(document).ready(function () {
    $('.slick-item').slick({
        dots: false,
        slidesToShow: 1,
        infinite: true, 
    });
})

 /*  show menu navbar mobile */
 function myFunctionNavbarMobile() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}
/* login */



/******** cart ********/
// if(typeof(Storage) !== "undefined") {
//     // Store
//     localStorage.setItem("name-item-1", "Dầu Nhớt Fuchs Silkolene 10w40 và 10w30 chính hãng nhập khẩu từ Châu Âu");
//     // Retrieve
//     document.getElementById("result").innerHTML = localStorage.getItem("name-item-1");
//   } else {
//     document.getElementById("result").innerHTML = "Sorry, your browser does not support Web Storage...";
//   }


