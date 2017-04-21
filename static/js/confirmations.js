        var elems = document.getElementsByClassName('confirmations');
        var confirmIt = function (e) {
            if (!confirm('Are you sure you want to log out?')) e.preventDefault();
        };
        for (var i = 0, l = elems.length; i < l; i++) {
            elems[i].addEventListener('click', confirmIt, false);
        }
