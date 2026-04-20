let host = window.location.hostname.endsWith('arc3.games') ? window.location.host : 'arc3.games';
let apiUrl = `https://${host}/api.php`;
let submitUrl = `https://${host}/submit.php`;

function downloadFile(url, fn) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            fn(xhr.response);
        } else {
            fn(null);
        }
    };
    xhr.send();
}

function apiGetSequence(fn) {
    let game_id = metadata.game_id;
    let level = levelsCompleted + 1;

    let params = new URLSearchParams({
        action: 'getTopSequences',
        gameId: game_id,
        level: level,
        limit: 1
    });

    let xhr = new XMLHttpRequest();
    xhr.open('POST', apiUrl);
    xhr.responseType = 'json';
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    let _levelsCompleted = levelsCompleted;

    xhr.onload = () => {
        if (xhr.status === 200 && xhr.response?.ok && xhr.response.data.length > 0 && metadata.game_id === game_id && levelsCompleted === _levelsCompleted) {
            fn(xhr.response.data[0]);
        } else {
            fn(null);
        }
    };
    xhr.send(params.toString());
}

function apiGetLevelStats(fn) {
    let game_id = metadata.game_id;
    let level = levelsCompleted + 1;

    let params = new URLSearchParams({
        action: 'getLevelStats',
        gameId: game_id,
        level: level
    });

    let xhr = new XMLHttpRequest();
    xhr.open('POST', apiUrl);
    xhr.responseType = 'json';
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    let _levelsCompleted = levelsCompleted;

    xhr.onload = () => {
        if (xhr.status === 200 && xhr.response?.ok && metadata.game_id === game_id && levelsCompleted === _levelsCompleted) {
            fn(xhr.response.data);
        } else {
            fn(null);
        }
    };
    xhr.send(params.toString());
}

function apiGetStatsSum(fn) {
    let params = new URLSearchParams({
        action: 'getStatsSum'
    });

    let xhr = new XMLHttpRequest();
    xhr.open('POST', apiUrl);
    xhr.responseType = 'json';
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    xhr.onload = () => {
        if (xhr.status === 200 && xhr.response?.ok) {
            fn(xhr.response.data);
        } else {
            fn(null);
        }
    };
    xhr.send(params.toString());
}

function downloadGame() {
    if (metadata === null) {
        return;
    }
    let split = metadata.game_id.split('-')
    let name = split[0]
    let version = split[1]

    let pyUrl = `./environment_files/${name}/${version}/${name}.py`;
    let metaUrl = `./environment_files/${name}/${version}/metadata.json`;

    downloadFile(metaUrl, (metaData) => {
        if (metaData === null) {
            return;
        }
        downloadFile(pyUrl, (pyData) => {
            if (pyData === null) {
                return;
            }
            let zip = new JSZip();

            zip.file(`${name}/${version}/${name}.py`, pyData);
            zip.file(`${name}/${version}/metadata.json`, metaData);

            zip.generateAsync({ type: 'blob' }).then(function (content) {
                saveAs(content, `${metadata.game_id}.zip`);
            });
        });
    });
}

function submitSequence(gameId, sequence, gameState) {
    if (window._arc3_offline || autoplay) {
        return;
    }
    let xhr = new XMLHttpRequest();
    xhr.open("POST", submitUrl);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 201) {
            console.log(JSON.parse(xhr.responseText));
        } else {
            console.log(`Error: ${xhr.status}`);
        }
    };
    xhr.send(`gameId=${gameId}&sequence=${JSON.stringify(sequence)}&gameState=${gameState}`);
}