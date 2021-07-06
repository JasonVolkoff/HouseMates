$( document ).ready(function() {
    // login.html js
    var modal = document.getElementById("myModal"); // Modal POPUP
    var btn = document.getElementsByClassName("myBtn");
    var span = document.getElementsByClassName("close")[0];
    for(var i = 0; i < btn.length; i++) {
        var b = btn[i];
        b.onclick = function() {
        modal.style.display = "block";
    }
    }
    
    span.onclick = function() {
        modal.style.display = "none";
    }
    window.onclick = function(event) {
        if (event.target == modal) {
        modal.style.display = "none";
        }
    } // Modal POPUP end

    // house.html js
    $('#price').on('change click keyup input paste',(function (event) {
    $(this).val(function (index, value) {
        return value.replace(/(?!\.)\D/g, "").replace(/(?<=\..*)\./g, "").replace(/(?<=\.\d\d).*/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    });
    }));
})




