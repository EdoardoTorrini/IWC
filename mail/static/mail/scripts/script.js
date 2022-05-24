
setTimeout(function(){
    document.body.className="";
},500);


function showPhoneMenu() {
    document.getElementById("phoneMenu").style.display = "block";
    document.getElementsByClassName("aside_alt")[0].innerHTML = "X";
    document.getElementsByClassName("aside_alt")[0].onclick = function() {
        hidePhoneMenu();
    };
}

function hidePhoneMenu() {
    document.getElementById("phoneMenu").style.display = "none";
    document.getElementsByClassName("aside_alt")[0].innerHTML = "MENU";
    document.getElementsByClassName("aside_alt")[0].onclick = function() {
        showPhoneMenu();
    };
}