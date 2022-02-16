/* Project specific Javascript goes here. */
console.log(radioStations);

let radioCard = document.querySelector("#radioCard");

const wrapper = document.querySelector("#musicList"),
musicImg = wrapper.querySelector(".img-area img"),
musicName = wrapper.querySelector(".song-details .name"),
musicDefine = wrapper.querySelector(".song-details .artist"),
playPauseBtn = wrapper.querySelector(".play-pause"),
prevBtn = wrapper.querySelector("#prev"),
nextBtn = wrapper.querySelector("#next"),
mainAudio = wrapper.querySelector("#main-audio"),
progressArea = wrapper.querySelector(".progress-area"),
progressBar = progressArea.querySelector(".progress-bar"),
musicList = wrapper.querySelector("#list"),
moreMusicBtn = wrapper.querySelector("#moreMusic"),
closemoreMusic = wrapper.querySelector("#close");

pauseSVG = "<path fill-rule='evenodd' d='M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z' clip-rule='evenodd'></path>";
playSVG = "<path fill-rule='evenodd' d='M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z' clip-rule='evenodd'></path>";

let musicIndex = Math.floor((Math.random() * radioStations.length) + 1);
isMusicPaused = true;

window.addEventListener("load", ()=>{
  loadMusic(musicIndex);
  playingSong();
});

function loadMusic(indexNumb){
  musicName.innerText = radioStations[indexNumb - 1].name;
  musicDefine.innerText = radioStations[indexNumb - 1].artist;
  musicImg.src = radioStations[indexNumb - 1].img;
  mainAudio.src = radioStations[indexNumb - 1].src;
};

//play music function
function playMusic(){
  wrapper.classList.add("paused");
  playPauseBtn.querySelector("svg").innerHTML = pauseSVG;
  playPauseBtn.classList.add("animate-spin")
  musicDefine.innerText = "Playing"
  musicDefine.classList.add("text-green-400")
  musicDefine.classList.remove("text-red-400")
  mainAudio.play();

};

//pause music function
function pauseMusic(){
  wrapper.classList.remove("paused");
  playPauseBtn.querySelector("svg").innerHTML = playSVG;
  musicDefine.innerText = "Paused"
  musicDefine.classList.remove("text-green-400")
  musicDefine.classList.add("text-red-400")
  mainAudio.pause();
};

//prev music function
function prevMusic(){
  musicIndex--; //decrement of musicIndex by 1
  //if musicIndex is less than 1 then musicIndex will be the array length so the last music play
  musicIndex < 1 ? musicIndex = radioStations.length : musicIndex = musicIndex;
  loadMusic(musicIndex);
  playMusic();
  playingSong(musicIndex);
};

//next music function
function nextMusic(){
  musicIndex++; //increment of musicIndex by 1
  //if musicIndex is greater than array length then musicIndex will be 1 so the first music play
  musicIndex > radioStations.length ? musicIndex = 1 : musicIndex = musicIndex;
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

//show music list onclick of music icon
moreMusicBtn.addEventListener("click", ()=>{
  musicList.classList.toggle("hidden");
});
closemoreMusic.addEventListener("click", ()=>{
  musicList.classList.toggle("hidden");
});

//change loop, shuffle, repeat icon onclick
// const repeatBtn = wrapper.querySelector("#repeat-plist");
// repeatBtn.addEventListener("click", ()=>{
//   let getText = repeatBtn.innerText; //getting this tag innerText
//   switch(getText){
//     case "repeat":
//       repeatBtn.innerText = "repeat_one";
//       repeatBtn.setAttribute("title", "Song looped");
//       break;
//     case "repeat_one":
//       repeatBtn.innerText = "shuffle";
//       repeatBtn.setAttribute("title", "Playback shuffled");
//       break;
//     case "shuffle":
//       repeatBtn.innerText = "repeat";
//       repeatBtn.setAttribute("title", "Playlist looped");
//       break;
//   }
// });

//code for what to do after song ended
// mainAudio.addEventListener("ended", ()=>{
//   // we'll do according to the icon means if user has set icon to
//   // loop song then we'll repeat the current song and will do accordingly
//   let getText = repeatBtn.innerText; //getting this tag innerText
//   switch(getText){
//     case "repeat":
//       nextMusic(); //calling nextMusic function
//       break;
//     case "repeat_one":
//       mainAudio.currentTime = 0; //setting audio current time to 0
//       loadMusic(musicIndex); //calling loadMusic function with argument, in the argument there is a index of current song
//       playMusic(); //calling playMusic function
//       break;
//     case "shuffle":
//       let randIndex = Math.floor((Math.random() * radioStations.length) + 1); //genereting random index/numb with max range of array length
//       do{
//         randIndex = Math.floor((Math.random() * radioStations.length) + 1);
//       }while(musicIndex == randIndex); //this loop run until the next random number won't be the same of current musicIndex
//       musicIndex = randIndex; //passing randomIndex to musicIndex
//       loadMusic(musicIndex);
//       playMusic();
//       playingSong();
//       break;
//   }
// });


const ulTag = wrapper.querySelector("ul");
// let create li tags according to array length for list
for (let i = 0; i <= radioStations.length; i++) {
  //let's pass the song name, artist from the array

  let liTag = `<li li-index="${i + 1}" class="z-[60] flex items-center justify-between space-x-15 cursor-pointer hover:bg-white/10 py-2 px-4 rounded-lg group transition ease-out">
                <div class="flex items-center">
                  <img
                    src="${radioStations[i].img}"
                    alt=""
                    height="48"
                    width="48"
                    objectFit="contain"
                    class="rounded-xl h-12 w-12 object-cover mr-3"
                  />
                  <div>
                    <h4 class="text-white text-sm font-semibold truncate max-w-[120px]">
                    ${radioStations[i].name}
                    </h4>
                    <p
                      class="text-[rgb(179,179,179)] text-[13px] font-semibold group-hover:text-white"
                    >
                    <span id="radio${i}" class="audio-duration">3:40</span>
                    </p>
                  </div>
                </div>
                <svg class="hover:scale-130 w-6 h-6 text-[#868686] hover:text-red-600 ml-auto relative cursor-pointer group-hover:border-white/40" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"></path></svg>
                <audio class="radio${i}" src="${radioStations[i].src}"></audio>
              </li>`;

  ulTag.insertAdjacentHTML("beforeend", liTag); //inserting the li inside ul tag

  let liAudioDuartionTag = ulTag.querySelector(`#radio${i}`);
  let liAudioTag = ulTag.querySelector(`.radio${i}`);
  liAudioTag.addEventListener("loadeddata", ()=>{
    let duration = liAudioTag.duration;
    let totalMin = Math.floor(duration / 60);
    let totalSec = Math.floor(duration % 60);
    if(totalSec < 10){ //if sec is less than 10 then add 0 before it
      totalSec = `0${totalSec}`;
    };
    liAudioDuartionTag.innerText = `${totalMin}:${totalSec}`; //passing total duation of song
    liAudioDuartionTag.setAttribute("t-duration", `${totalMin}:${totalSec}`); //adding t-duration attribute with total duration value
  });
};

//play particular song from the list onclick of li tag
function playingSong(musicIndex){
  const allLiTag = ulTag.querySelectorAll("li");


  for (let j = 0; j < allLiTag.length; j++) {
    let audioTag = allLiTag[j].querySelector(".audio-duration");

    if(allLiTag[j].classList.contains("playing")){
      allLiTag[j].classList.remove("playing");
      let adDuration = audioTag.getAttribute("t-duration");
      audioTag.classList.remove("text-green-400")
      audioTag.innerText = adDuration;
      //audioTag.innerText = "Paused";
    }

    //if the li tag index is equal to the musicIndex then add playing class in it
    if(allLiTag[j].getAttribute("li-index") == musicIndex){
      allLiTag[j].classList.add("playing");
      audioTag.classList.add("text-green-400")
      audioTag.innerText = "Playing";
    }

    allLiTag[j].setAttribute("onclick", "clicked(this)");
  }
};


//particular li clicked function
function clicked(element){
  let getLiIndex = element.getAttribute("li-index");
  musicIndex = getLiIndex; //updating current song index with clicked li index
  loadMusic(musicIndex);
  playMusic();
  playingSong(musicIndex);
};

function mapPlay(element){
  let getIndex = element.getAttribute("data-index");
  radioIndex = getIndex; //updating current song index with clicked li index
  loadMusic(radioIndex);
  playMusic();
  playingSong(radioIndex);
};

function tapped(element){
  let getIndex = element.getAttribute("data-index");
  element.classList.toggle("playing")
  radioIndex = getIndex; //updating current song index with clicked li index
  if (element.classList.contains("playing")) {
    loadMusic(radioIndex);
    playMusic();
    playingSong(radioIndex);
    // element.classList.add("animate-pulse")
    // element.innerHTML = pauseSVG;
  } else {
    pauseMusic();
    // element.classList.remove("animate-pulse")
    // element.innerHTML = playSVG;
  }
};

