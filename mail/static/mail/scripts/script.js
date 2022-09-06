
setTimeout(function(){
    document.body.className="";
},500);


function timerReloadEmail() {
    /* window.location.reload(); */
    setTimeout(timerReloadEmail, 500000)
}

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

function btnWriteClicked() {
    document.getElementById("wroteEmailDiv").style.display = "block";

}

function closePopWrtEmail() {
    document.getElementById("wroteEmailDiv").style.display = "none";
}

function selBox(sId, sToken) {
    console.log(sId, sToken);
    document.getElementById("sId").submit();
}

function selFileFromSystem() {
    document.getElementById("fileChooser").click();
}