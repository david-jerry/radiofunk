const wrapper = document.querySelector(".wrapper"),

musicImg = wrapper.querySelector(".img-area img"),
musicName = wrapper.querySelector(".song-details .name"),
musicDefine = wrapper.querySelector(".song-details .artist"),
playPauseBtn = wrapper.querySelector(".play-pause"),
prevBtn = wrapper.querySelector("#prev"),
nextBtn = wrapper.querySelector("#next"),
mainAudio = wrapper.querySelector("#main-audio"),
progressArea = wrapper.querySelector(".progress-area"),
progressBar = progressArea.querySelector(".progress-bar"),
musicList = wrapper.querySelector("#playlist"),


pauseSVG = "<path fill-rule='evenodd' d='M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z' clip-rule='evenodd'></path>";
playSVG = "<path fill-rule='evenodd' d='M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z' clip-rule='evenodd'></path>";

let musicIndex = sourceData[0].index;

isMusicPaused = true;

window.addEventListener("load", ()=>{
  loadMusic(musicIndex);
  // playingSong();
});

function loadMusic(index){
  // if(sourceData[index])
  for(let t = 0; t < sourceData.length; t++) {
    if (sourceData[t].id == index) {
      console.log(sourceData[t].id)
      musicName.innerText = "Ep-" + sourceData[t].index + " " + sourceData[t].name;
      musicDefine.innerText = sourceData[t].author;
      musicImg.src = sourceData[t].img;
      mainAudio.src = sourceData[t].uri;
    }
  }
};

function playMusic() {
  wrapper.classList.add("paused");
  playPauseBtn.querySelector("svg").innerHTML = pauseSVG;
  playPauseBtn.classList.add("animate-spin")
  musicDefine.innerText = "Playing"
  musicDefine.classList.add("text-green-400")
  musicDefine.classList.remove("text-live-bg", "dark:text-primary")
  mainAudio.play();
}


//pause music function
function pauseMusic(){
  wrapper.classList.remove("paused");
  playPauseBtn.querySelector("svg").innerHTML = playSVG;
  musicDefine.innerText = "Paused"
  musicDefine.classList.remove("text-green-400")
  musicDefine.classList.add("text-live-bg", "dark:text-primary")
  mainAudio.pause();
};

//prev music function
function prevMusic(){
  musicIndex--; //decrement of musicIndex by 1
  //if musicIndex is less than 1 then musicIndex will be the array length so the last music play
  musicIndex < 1 ? musicIndex = sourceData.length : musicIndex = musicIndex;
  loadMusic(musicIndex);
  playMusic();
  playingSong(musicIndex);
};

//next music function
function nextMusic(){
  musicIndex++; //increment of musicIndex by 1
  //if musicIndex is greater than array length then musicIndex will be 1 so the first music play
  musicIndex > sourceData.length ? musicIndex = 1 : musicIndex = musicIndex;
  loadMusic(musicIndex);
  playMusic();
  playingSong(musicIndex);
};

// play or pause button event
playPauseBtn.addEventListener("click", ()=>{
  const isMusicPlay = wrapper.classList.contains("paused");
  //if isPlayMusic is true then call pauseMusic else call playMusic
  isMusicPlay ? pauseMusic() : playMusic();
  playingSong();
});

//prev music button event
prevBtn.addEventListener("click", ()=>{
  prevMusic();
});

//next music button event
nextBtn.addEventListener("click", ()=>{
  nextMusic();
});

// update progress bar width according to music current time
mainAudio.addEventListener("timeupdate", (e)=>{
  const currentTime = e.target.currentTime; //getting playing song currentTime
  const duration = e.target.duration; //getting playing song total duration
  let progressWidth = (currentTime / duration) * 100;
  progressBar.style.width = `${progressWidth}%`;

  let musicCurrentTime = wrapper.querySelector(".current-time"),
  musicDuartion = wrapper.querySelector(".max-duration");
  mainAudio.addEventListener("loadeddata", ()=>{
    // update song total duration
    let mainAdDuration = mainAudio.duration;
    let totalMin = Math.floor(mainAdDuration / 60);
    let totalSec = Math.floor(mainAdDuration % 60);
    if(totalSec < 10){ //if sec is less than 10 then add 0 before it
      totalSec = `0${totalSec}`;
    }
    musicDuartion.innerText = `${totalMin}:${totalSec}`;
  });
  // update playing song current time
  let currentMin = Math.floor(currentTime / 60);
  let currentSec = Math.floor(currentTime % 60);
  if(currentSec < 10){ //if sec is less than 10 then add 0 before it
    currentSec = `0${currentSec}`;
  }
  musicCurrentTime.innerText = `${currentMin}:${currentSec}`;
});

// update playing song currentTime on according to the progress bar width
progressArea.addEventListener("click", (e)=>{
  let progressWidth = progressArea.clientWidth; //getting width of progress bar
  let clickedOffsetX = e.offsetX; //getting offset x value
  let songDuration = mainAudio.duration; //getting song total duration

  mainAudio.currentTime = (clickedOffsetX / progressWidth) * songDuration;
  playMusic(); //calling playMusic function
  playingSong();
});

function playingSong(trackIndex){
  if (musicList != null || musicList != undefined) {
    const Tracks = musicList.querySelectorAll(".list-group-item");
    for (let j = 0; j <= Tracks.length; j++) {

      if(Tracks[j].getAttribute("li-index") != trackIndex){
        if(Tracks[j].classList.contains("playing")) {
          let audioTag = Tracks[j].querySelector(".audio-duration");
          Tracks[j].querySelector("svg").innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>`
          Tracks[j].classList.remove("playing");
          Tracks[j].querySelector("svg").classList.remove("text-green-400", "animate-pulse");
          Tracks[j].querySelector(".date").classList.remove("text-green-400", "animate-pulse");
        }
        //audioTag.innerText = "Paused";
      }

      //if the li tag index is equal to the trackIndex then add playing class in it
      if(Tracks[j].getAttribute("li-index") === trackIndex){
        let audioTag = Tracks[j].querySelector(".audio-duration");
        Tracks[j].querySelector("svg").innerHTML = `<path stroke-linecap='round' stroke-linejoin='round' stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>`
        Tracks[j].classList.add("playing");
        Tracks[j].querySelector("svg").classList.add("text-green-400", "animate-pulse")
        Tracks[j].querySelector(".date").classList.add("text-green-400", "animate-pulse");
      }

      Tracks[j].setAttribute("onclick", "playpodcast(this)");
    };
  }
}

function playpodcast(element){
  let getLiIndex = element.getAttribute("li-index");
  element.classList.add("playing")
  trackIndex = getLiIndex; //updating current song index with clicked li index
  if (element.classList.contains("playing")) {
    loadMusic(trackIndex);
    playMusic();
    playingSong(trackIndex);

    // element.querySelector(".audio-duration").classList.add("text-green-400")
    // element.querySelector(".audio-duration").innerHTML = "Playing"
  } else {
    pauseMusic();
    // element.querySelector(".audio-duration").classList.remove("text-green-400")
    // element.querySelector(".audio-duration").innerHTML = "0.00"
  }
};





