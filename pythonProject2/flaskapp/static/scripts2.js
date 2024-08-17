//document.addEventListener('DOMContentLoaded', function() {
//    const filterLinks = document.querySelectorAll('.sentiment-filters a');
//
//    filterLinks.forEach(link => {
//        link.addEventListener('click', function(event) {
//            event.preventDefault();
//            const filter = this.getAttribute('href').split('=')[1];
//            const url = new URL(window.location.href);
//            url.searchParams.set('filter', filter);
//            window.location.href = url.toString();
//        });
//    });
//});
