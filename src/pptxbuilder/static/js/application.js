
// back to top button - docs
$(function () {
  if ($('.docs-top').length) {
    _backToTopButton()
    $(window).on('scroll', _backToTopButton)
    function _backToTopButton () {
      if ($(window).scrollTop() > $(window).height()) {
        $('.docs-top').fadeIn()
      } else {
        $('.docs-top').fadeOut()
      }
    }
  }

  // doc nav js
  var $toc = $('#markdown-toc')
  var $window = $(window)
  $('.upload-dummy').on('click', function(e){
    e.stopPropagation();
    var blob = null;
    var xhr = new XMLHttpRequest();
    var loc = window.location.pathname;
    console.log(loc);
    xhr.open("GET", "static/pptx_builder_dummy_datafile.xlsx", {type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64"});
    xhr.responseType = "blob";//force the HTTP response, response-type header to be blob
    xhr.onload = function()
    {
      blob = xhr.response;//xhr.response is now a blob object
      console.log(blob);

      selectedFile = blob;
      var reader = new FileReader();
      reader.addEventListener('load', function () {
        $('input[name="file"]').val(reader.result);
        $('.upload-form').submit();
      });
      reader.readAsDataURL(selectedFile);
    }
    xhr.send();
  })

  if ($toc[0]) {
    $('#markdown-toc li').addClass('nav-item')
    $('#markdown-toc li > a').addClass('nav-link')

    maybeActivateDocNavigation()
    $window.on('resize', maybeActivateDocNavigation)

    function maybeActivateDocNavigation () {
      if ($window.width() > 768) {
        activateDocNavigation()
      } else {
        deactivateDocNavigation()
      }
    }

    function deactivateDocNavigation() {
      $window.off('resize.theme.nav')
      $window.off('scroll.theme.nav')
      $toc.css({
        position: '',
        left: '',
        top: ''
      })
    }

    function activateDocNavigation() {

      var cache = {}

      function updateCache() {
        cache.containerTop   = $('.docs-content').offset().top
        cache.containerRight = $('.docs-content').offset().left + $('.docs-content').width() + 40
        measure()
      }

      function measure() {
        var scrollTop = $window.scrollTop()
        var distance =  Math.max(scrollTop - cache.containerTop, 0)

        if (!distance) {
          $($toc.find('li a')[1]).addClass('active')
          return $toc.css({
            position: '',
            left: '',
            top: ''
          })
        }

        $toc.css({
          position: 'fixed',
          left: cache.containerRight,
          top: 0
        })
      }

      updateCache()

      $(window)
        .on('resize.theme.nav', updateCache)
        .on('scroll.theme.nav', measure)

      $('body').scrollspy({
        target: '#markdown-toc',
        children: 'li > a'
      })

      setTimeout(function () {
        $('body').scrollspy('refresh')
      }, 1000)
    }
  }
})
