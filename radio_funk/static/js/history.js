if (window.location.href !== home) {
    document.getElementById('hback').classList.add('cursor-pointer');
    document.getElementById('hback').classList.add('text-primary');
    document.getElementById('hback').classList.remove('cursor-not-allowed');
  } else {
    document.getElementById('hback').classList.remove('cursor-pointer');
    document.getElementById('hback').classList.remove('text-primary');
    document.getElementById('hback').classList.add('cursor-not-allowed');
  }


  function back(url) {
    if (window.location.href !== home) {
        this.history.go(-1)
    }
  }


  if (window.history.length > 2 !== window.history.length) {
    document.getElementById('hforward').classList.remove('cursor-not-allowed');
    document.getElementById('hforward').classList.add('cursor-pointer', 'text-primary');
  } else {
    document.getElementById('hforward').classList.add('cursor-not-allowed');
    document.getElementById('hforward').classList.remove('cursor-pointer', 'text-primary');
  }

  function forward(url) {
    if ((window.history.length - 1) < window.history.length) {
      this.history.go(+1)
      document.getElementById('hforward').classList.add('cursor-not-allowed');
      document.getElementById('hforward').classList.remove('cursor-pointer', 'text-primary');
    }
  }
