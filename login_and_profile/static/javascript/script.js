$( document ).ready(function() {
    // login.html js
    const triggers = document.getElementsByClassName('myBtn');
    const triggerArray = Array.from(triggers).entries();
    const modals = document.getElementsByClassName('modal');
    const closeButtons = document.getElementsByClassName('close');

    for (let [index, trigger] of triggerArray) {
    const openModal = () => {
        modals[index].style.display = 'block';
    }
    const closeModal = () => {
        modals[index].style.display = 'none';
    }
    trigger.addEventListener("click", openModal);
    closeButtons[index].addEventListener("click", closeModal);
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




