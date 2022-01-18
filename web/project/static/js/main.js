$(document).ready( async () =>{

    $('#play').click(playClickHandler)

    $('.checkbox-group')
    .mouseenter(checkboxMouseenterHandler)
    .mouseleave(checkboxMouseleaveHandler)
    .click(checkboxClickHandler)

    $('#number_send').change(numberSendHandler)

    $('#file_send').change(fileSendHandler)

    let channel = parseInt($('.main')[0].id)
    $(`#save`).on('click', function(e) {
        localStorage.setItem(`button_${channel}_disabled`, true)
        disableSaveButton()

        e.preventDefault()
        $.getJSON(`/background_save/${channel}`,
            function(data) {
          //do nothing
        })
        return false
    })
    
    let songs = await getSongs(2)
    let playing_songs = songs
    $('#song_title').html(playing_songs[channel])
    changeImages(channel)

    if (localStorage.getItem(`button_${channel}_disabled`) == 'true') {
        disableSaveButton()
    } else {
        enableSaveButton()
    }

    setInterval(async () => {
        songs = await getSongs(2)
        console.log('print')
        if (localStorage.getItem(`button_${channel}_disabled`) == 'false') {
            enableSaveButton()
        }
        $('#song_title').html(playing_songs[channel])
        changeImages(channel)
        for (let i = 1; i < 3; i++) {
            if (songs[i] !== playing_songs[i]) {
                playing_songs[i] = songs[i]
                localStorage.setItem(`button_${i}_disabled`, false)
            }
        }
    }, 3000)
})


function playClickHandler() {
    var myAudio = document.getElementById('my-audio')
    if ($('#play').text() == 'play') {
        myAudio.muted = false
        $('#play').text('stop') 
    } else {
        myAudio.muted = true
        $('#play').text('play')
    }
}

function numberSendHandler() {
        if (Number($('#number_send').val()) == 0 || $('#number_send').val() == '') {
            $('#number_send').css('background-color', 'grey')
        } else {
            $('#file_send').val('')
            $('#file_send').css('background-color', 'grey')
            $('#file_button').css('background-color', 'grey')
            $('#number_send').css('background-color', 'dimgray')
        }
}

function fileSendHandler() {
    if( document.getElementById("file_send").files.length == 0 ) {
        $('#file_button').css('background-color', 'grey')
    } else {
        $('#number_send').val('0');
        $('#file_button').css('background-color', 'dimgray')
        $('#number_send').css('background-color', 'grey')
    }
}

function checkboxMouseenterHandler(event) {
    const checkmark  = event.currentTarget.querySelector('.checkmark')
    const checkbox = event.currentTarget.querySelector('.checkbox')
    if (!($(checkbox).is(':checked'))) {
        $(checkmark).css('background-color', 'dimgrey')
    }
}

function checkboxMouseleaveHandler(event) {
    const checkmark  = event.currentTarget.querySelector('.checkmark')
    const checkbox = event.currentTarget.querySelector('.checkbox')
    if (!($(checkbox).is(':checked'))) {
        $(checkmark).css('background-color', 'grey')
    }
}

function checkboxClickHandler(event) {
    const checkmark  = event.currentTarget.querySelector('.checkmark')
    const checkbox = event.currentTarget.querySelector('.checkbox')
    if ($(checkbox).is(':checked')) {
        $(checkmark).css('background-color', 'red')
    } else {
        $(checkmark).css('background-color', 'dimgrey')
    }
}

async function getSong(n) {
    let output 
    await $.getJSON('http://lon1.apankov.net:8090/status-json.xsl', function(result){
        let data = result.icestats.source[n - 1].title.slice(2)
        data = JSON.parse(data)
        let artist = data['artist']
        let album = data['album']
        let year = data['year']
        let song = data['song_title']
        let label = data['label']
        output = `${artist}<br>${song}<br><br>${year} -- ${album}<br><br>[${label}]`
})
    return output
}

async function getSongs(n) {
    let output = ['', '', '', '']
    let data = ['', '', '', '']
    let artist, album, year, song, label = ''
    await $.getJSON('http://lon1.apankov.net:8090/status-json.xsl', function(result){
        for (let i = 1; i < n + 1; i++) {
            data[i] = result.icestats.source[i - 1].title.slice(3)
            console.log('test', i, data[i])
            json_data = JSON.parse(data[i])
            console.log('test2', i, json_data)
            artist = json_data['artist']
            album = json_data['album']
            year = json_data['year']
            song = json_data['song_title']
            label = json_data['label']
            console.log('label', label)
            output[i] = `${artist}<br>${song}<br><br>${year} -- ${album}<br><br>[${label}]`
        }
})
    return output
}

function changeImages(channel) {
    $('#cover1').attr('src', `http://lon1.apankov.net:8092/covers/cover-${channel}-1.jpg?random=` + new Date().getTime())
    $('#cover2').attr('src', `http://lon1.apankov.net:8092/covers/cover-${channel}-2.jpg?random=` + new Date().getTime())
    $('#cover3').attr('src', `http://lon1.apankov.net:8092/covers/cover-${channel}-3.jpg?random=` + new Date().getTime())
}

function enableSaveButton() {
    $(`#save`).css('background-color', 'grey')
    $(`#save`).removeAttr('disabled')
    $(`#save`).addClass('button')
}

function disableSaveButton() {
    $(`#save`).css('background-color', 'dimgray')
    $(`#save`).attr('disabled', 'disabled')
    $(`#save`).removeClass('button')
}
