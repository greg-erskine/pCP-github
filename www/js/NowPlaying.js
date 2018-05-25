/*  NowPlaying.js

    Some Code derrived from https://github.com/Logitech/slimserver 
    Logitech Media Server Copyright 2001-2009 Logitech
    Used under the GPLv2 License.

*/
var url = null;
var playerName = null;
var xhttp = null;
var req_timer = null;
var req_timer_running = false;
var refresh_timer = null;
var refresh_timer_running = false;
var page_visible = false;
var repeat = {
        value: 0,
        btn_class: '',
        command: '',
        tooltip: ""
    };
var shuffle = {
        value: 0,
        btn_class: '',
        command: '',
        tooltip: ''
    };

var tags = [ "tags:ub", "tags:cgABbehldiqtyrSuoKLNJ" ];

var playerStatus = {
        image_url: "",
        Title: "", 
        Artist: "", 
        Album: "", 
        Bitrate: "", 
        PlayNum: 0, 
        SongCount: 0,
        duration: 1,
        ellapsed: 0,
        volume: 50,
        volume_class: "ctrlVolume1",
        power: 0,
        playing: "",
        can_seek: 0,
    };

function SetUpdates(update) {
    if ((!page_visible) && (update)) {
        loadPlayerStatus(1);
        Refresh_Page();
        page_visible = true;
    } else if (!update){
        if (req_timer) clearTimeout(req_timer);
        req_timer_running = false;
        if (refresh_timer) clearTimeout(refresh_timer);
        refresh_timer_running = false;
        page_visible = false;
    }
}

function getObjPosition(element) {
    var obj = document.getElementById(element);
    var pos = {};
    pos.x = obj.offsetLeft;
    pos.width = obj.offsetWidth;
    while (obj.offsetParent) {
        pos.x = pos.x + obj.offsetParent.offsetLeft;
        if ( obj == document.getElementsByTagName("body")[0]) {
            break;
        } else {
            obj = obj.offsetParent;
        }
    }
    return pos;
}

function setProgress(event) {
    if (playerStatus.can_seek==1) {
//Progress width is set -20 from actual width above
        var pos = getObjPosition("ctrlProgress");
        var cX = event.clientX - pos.x;
        var amount = ( cX / (pos.width - 15) );
//      console.log("box=" + pos.x + ", " + pos.width + " x=" + event.clientX + ", " + cX + " :" + amount);
        var newtime = Math.round (playerStatus.duration * amount);
        generate_lms_command( "time", newtime );
        ellapsed = newtime;
    }
}

function setVolume(event) {
    var pos = getObjPosition("ctrlVolume");
//volume slider image is 91px wide with 7px dead zone left and right
    var cX = event.clientX - pos.x - 7;
    var amount = Math.round( cX / 77 * 10 );
    amount = ( amount < 1 ? 0 : amount);
    amount = ( amount > 10 ? 10 : amount);
//console.log("box=" + pos.x + "x=" + cX + ":" + amount);
    generate_lms_command("mixer", "volume", amount * 10 );
    playerStatus.volume_class = "ctrlVolume" + amount.toString();
    document.getElementById("ctrlVolume").className = playerStatus.volume_class;
}

function updateShuffle() {
    if (arguments.length > 0) {
        if (shuffle.value == 3 ) {
           generate_lms_command.apply(null, shuffle.command );
        } else {
            shuffle.value = ( shuffle.value === 0 ? 1 : ( shuffle.value == 1 ? 2 : 0 ) );
            generate_lms_command("playlist", "shuffle", shuffle );
        }
    }
    if ( shuffle.value === 0 ) {
        document.getElementById("btn-shuffle").className = "btn-shuffle-0";
        document.getElementById("btn-shuffle-text").title = "Do Not Shuffle Playlist";
    } else if ( shuffle.value == 1 ) {
        document.getElementById("btn-shuffle").className = "btn-shuffle-1";
        document.getElementById("btn-shuffle-text").title = "Shuffle by Song";
    } else if ( shuffle.value == 2 ) {
        document.getElementById("btn-shuffle").className = "btn-shuffle-2";
        document.getElementById("btn-shuffle-text").title = "Shuffle by Album";
    } else {
        //custom button
        document.getElementById("btn-shuffle").className = shuffle.btn_class;
        document.getElementById("btn-shuffle-text").title = shuffle.tooltip;
    }
}

function updateRepeat() {
    if (arguments.length > 0) {
        if (repeat.value == 3 ) {
            generate_lms_command.apply(null, repeat.command );
        } else {
            repeat.value = ( repeat.value === 0 ? 1 : ( repeat.value == 1 ? 2 : 0 ) );
            generate_lms_command("playlist", "repeat", repeat );
        }
    }
    if ( repeat.value === 0 ) {
        document.getElementById("btn-repeat").className = "btn-repeat-0";
        document.getElementById("btn-repeat-text").title = "Repeat Off";
        } else if ( repeat.value == 1 ) {
        document.getElementById("btn-repeat").className = "btn-repeat-1";
        document.getElementById("btn-repeat-text").title = "Repeat Current Song";
    } else if ( repeat.value == 2 ) {
        document.getElementById("btn-repeat").className = "btn-repeat-2";
        document.getElementById("btn-repeat-text").title = "Repeat Playlist";
    } else {
        //custom button
        document.getElementById("btn-repeat").className = repeat.btn_class;
        document.getElementById("btn-repeat-text").title = repeat.tooltip;
    }
}

function togglePause() {
    if ( playerStatus.playing == "play" ) {
        playerStatus.playing = "pause";
        generate_lms_command("pause");
        document.getElementById("toggleplay").className = "btn-play";
        document.getElementById("btn-toggle-play").title = "Play";
    } else {
        playerStatus.playing = "play";
        generate_lms_command("play");
        document.getElementById("toggleplay").className = "btn-pause";
        document.getElementById("btn-toggle-play").title = "Pause";
    }
}

function Power() {
    if (arguments.length > 0) { playerStatus.power = (playerStatus.power == 1 ? 0 : 1 ); }
    if ( playerStatus.power == 1 ) {
        document.getElementById("btn-pwr").className = "btn-power";
        document.getElementById("btn-pwr-text").title = "Power: On";
    } else {
        document.getElementById("btn-pwr").className = "btn-power-off";
        document.getElementById("btn-pwr-text").title = "Power: Off";
    }
}

function Refresh_Page() {
    if ( playerStatus.playing == "play" ) {
        document.getElementById("toggleplay").className = "btn-pause";
        document.getElementById("btn-toggle-play").title = "Pause";
    } else {
        document.getElementById("toggleplay").className = "btn-play";
        document.getElementById("btn-toggle-play").title = "Play";
    }
    document.getElementById("ctrlVolume").className = playerStatus.volume_class;
    Power();
    updateRepeat();
    updateShuffle();

    //Add 1 sec to the ellapsed time
    if ( (playerStatus.playing == "play") && (playerStatus.ellapsed <= playerStatus.duration) ) {
        playerStatus.ellapsed += 1;
    } else if (playerStatus.playing == "stop") {
        playerStatus.ellapsed = 0;
    }
    var ctrlPlaytime = formatTime(Math.round(playerStatus.ellapsed));
    var ctrlRemainingTime = 0;
    if ( Math.round(playerStatus.duration) > 0 ) {
        var timeleft = Math.round(playerStatus.duration - playerStatus.ellapsed);
        ctrlRemainingTime = formatTime( (timeleft < 0 ? 0 : timeleft) );
        if ( timeleft < 0 ) loadPlayerStatus(1);
    } 
    document.getElementById("ctrlPlaytime").innerHTML = ctrlPlaytime.toString();
    if ( ctrlRemainingTime === 0 ) {
        document.getElementById("ctrlRemainingTime").innerHTML = "";
    } else {
        document.getElementById("ctrlRemainingTime").innerHTML = "-" + ctrlRemainingTime.toString();
    }
    var width = document.getElementById("ctrlProgress").offsetWidth - 20;
    var percent, left, right;
	if ( playerStatus.duration > 0 ) {
        percent = (playerStatus.ellapsed / playerStatus.duration);
        left = Math.round(width * percent);
        right = width - left;
    } else {
        left = 0;
        right = width;
    }
    document.getElementById("fill_left").style = "width:" + left.toString() + "px;";
    document.getElementById("fill_right").style = "width:" + right.toString() + "px;";

    refresh_timer = setTimeout("Refresh_Page()", 980);
}

function formatTime(seconds) {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return [
        h,
        m > 9 ? m : (h ? "0" + m : m || "0"),
        s > 9 ? s : "0" + s,
        ].filter(a => a).join(":");
}

function RandomPlay() {
    generate_lms_command("randomplay" , "tracks");
}

function getImageUrl(r) {
    var t = ((r || {}).remoteMeta || {}).artwork_url;
    if (t) { 
        if (t[0] == '/') return t; else return '/' + t;
    }
    t = ((r || {}).playlist_loop["0"] || {}).artwork_track_id;
    if (t) return "/music/" + t + "/cover.jpg";
    return playerStatus.image_url;
}

function getArtist(r) {
    var t = ((r || {}).remoteMeta || {}).artist;
    if (t) return t;
    t = ((r || {}).playlist_loop["0"] || {}).artist;
    if (t) return t;
    t = ((r || {}).playlist_loop["0"] || {}).albumartist;
    if (t) return t;
    return playerStatus.Artist;
}

function getTitle(r) {
    var t = ((r || {}).remoteMeta || {}).title;
    if (t) return t;
    t = ((r || {}).playlist_loop["0"] || {}).title;
    if (t) return t;
    return playerStatus.Title;
}

function getAlbum(r) {
    var t = ((r || {}).remoteMeta || {}).album;
    if (t) return t;
    t = ((r || {}).playlist_loop["0"] || {}).album;
    if (t) return t;
    return playerStatus.Album 
}

function getBitrate(r) {
    var t = ((r || {}).remoteMeta || {}).bitrate;
    if (t) return r.remoteMeta.bitrate + ", " + r.remoteMeta.type;
    t = ((r || {}).playlist_loop["0"] || {}).bitrate;
    if (t) return r.playlist_loop["0"].bitrate + ", " + r.playlist_loop["0"].type;
    return playerStatus.Bitrate;
}

function Player_Status_Handler(){
    req_timer_running = false;
    loadPlayerStatus(0);
}

function loadPlayerStatus(force) {
    if (force == 1) {
        if (req_timer) clearTimeout(req_timer);
        req_timer_running = false;
    }
    if (!req_timer_running) {
        var req_tags = ( force == 1 ? 1 : 0 );
        xhttp = new XMLHttpRequest();
        xhttp.timeout = 2500;
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var myObj = JSON.parse(this.responseText);
                var result = myObj.result;

                playerStatus.Title = getTitle(result);
                playerStatus.Album = getAlbum(result);
                playerStatus.Artist = getArtist(result);
                playerStatus.image_url = getImageUrl(result);
               
                playerStatus.PlayNum = parseInt(myObj.result.playlist_cur_index, 10) + 1;
                playerStatus.SongCount = myObj.result.playlist_tracks;

                if ( req_tags == 1) { 
                    playerStatus.Bitrate = getBitrate(result);
                }

                //detect if we need full tags
                if ( document.getElementById("ctrlCurrentTitle").innerHTML != playerStatus.Title ){
                    document.getElementById("ctrlCurrentTitle").innerHTML = playerStatus.Title;
                    if (force!=1) {
                        loadPlayerStatus(1);
                        return;
                    }
                }

                document.getElementById("image").src = url.concat(playerStatus.image_url);
                document.getElementById("ctrlCurrentTitle").innerHTML = playerStatus.Title;
                document.getElementById("ctrlCurrentArtist").innerHTML = playerStatus.Artist;
                document.getElementById("ctrlCurrentAlbum").innerHTML = playerStatus.Album;
                document.getElementById("ctrlBitrate").innerHTML = playerStatus.Bitrate;
                document.getElementById("ctrlPlayNum").innerHTML = playerStatus.PlayNum.toString();
                document.getElementById("ctrlSongCount").innerHTML = playerStatus.SongCount;

                //Get Current Volume
                playerStatus.volume = parseInt(result["mixer volume"] / 10 );
                playerStatus.volume_class = "ctrlVolume" + playerStatus.volume.toString();
                //Get Current Power
                playerStatus.power = parseInt(result.power);
                //Duration timer
                playerStatus.duration = result.duration;
                playerStatus.ellapsed = result.time;
                playerStatus.playing = result.mode;
                playerStatus.can_seek = (result.can_seek == 1 ? 1 : 0);

                //Custom Buttoms i.e. Pandora
                if ( ((result || {}).playlist_loop["0"] || {}).buttons ) {
                    repeat.command = result.playlist_loop["0"].buttons.repeat.command;
                    if ( result.playlist_loop["0"].buttons.repeat.jiveStyle == "thumbsUp" ) {
                        repeat.btn_class = "btn-thumbsUp";
                    } else {
                        repeat.btn_class = "btn-thumbsUp";
                    }
                    repeat.tooltip = result.playlist_loop["0"].buttons.repeat.tooltip;
                    repeat.value = 3;
                } else {
                    repeat.value = parseInt(result["playlist repeat"]);
                    repeat.btn_class = "";
                    repeat.command = "";
                }
                if ( ((result || {}).playlist_loop["0"] || {}).buttons ) {
                    shuffle.command = result.playlist_loop["0"].buttons.shuffle.command;

                    if ( result.playlist_loop["0"].buttons.shuffle.jiveStyle == "thumbsDown" ) {
                        shuffle.btn_class = "btn-thumbsDown";
                    } else {
                        shuffle.btn_class = "btn-thumbsDown";
                    }
                    shuffle.tooltip = result.playlist_loop["0"].buttons.shuffle.tooltip;
                    shuffle.value = 3;
                } else {
                    var i = parseInt(result["playlist shuffle"]);
                    shuffle.value = ( i > 3  ? 0 : i );
                    shuffle.btn_class = "";
                    shuffle.command = "";
                }
            }
            xhttp.ontimeout = function (e) {
                // If request for full tags timed out, then try again.
                if (req_tags == 1) {
                    loadPlayerStatus(1);
                }
            }
        }

        xhttp.open("POST", url + "/jsonrpc.js", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

        var data = {"id":1,"method":"slim.request","params": [ playerName, [ "status", "-", "1", tags[req_tags] ]]};
        var jsondata = JSON.stringify(data);
        try {
            xhttp.send(jsondata);
        } catch(err) {
            document.getElementById("track").innerHTML = "Set CSRF to None in LMS settings";
            document.getElementById("artist").innerHTML = "";
            document.getElementById("album").innerHTML = "";
        }

        req_timer_running = true;
        req_timer = setTimeout("Player_Status_Handler()", 5000);
    }
}
