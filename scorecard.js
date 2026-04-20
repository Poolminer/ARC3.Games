let scorecard = [];

let scorecardTemplate = window._arc3_offline ? '' : `
${document.getElementById('scorecard_content').innerHTML}
<br>
<br>
<table id="scorecard_table">
    <tr>
        <th>Level</th>
        <th>You</th>
        <th>Record</th>
        <th>Your score</th>
    </tr>
    #HTML
</table>
#FINAL_SCORE
`;

function generateScorecard(final=false){
    if(window._arc3_offline){
        return;
    }
    let htmlTable = '';
    let htmlFinalScore = '';

    let level = 1;
    for(let entry of scorecard){
        htmlTable += `
            <tr>
                <td><b>${level++}</b></td>
                <td>${entry.actions}</td>
                <td>${entry.record}</td>
                <td>${entry.score === -1 ? '...' : entry.score.toFixed(2) + '%'}</td>
            </tr>
        `;
    }
    if(final){
        let finalScore = 0;

        for(let entry of scorecard){
            finalScore += entry.score;
        }
        finalScore /= scorecard.length;

        htmlFinalScore = `
            <br>
            You final score is ${finalScore.toFixed(2) + '%'}!
        `;
    }
    document.getElementById('scorecard_content').innerHTML = scorecardTemplate.replace('#HTML', htmlTable).replace('#FINAL_SCORE', htmlFinalScore);
}

function scorecardReset(){
    if(window._arc3_offline){
        return;
    }
    scorecard.length = 0;
}

function scorecardEnter(final=false){
    if(window._arc3_offline){
        return;
    }
    if(scorecard.length !== 0){
        let entry = scorecard[scorecard.length - 1];
        entry.score = entry.record / entry.actions * 100;
    }
    if(!final){
        scorecard.push({
            actions: 0,
            record: autoplayActions.length,
            score: -1
        });
    }
    generateScorecard(final);
}

function scorecardClose(){
    if(window._arc3_offline){
        return;
    }
    scorecardEnter(true);
}

function scorecardRefresh(){
    if(window._arc3_offline || scorecard.length === 0){
        return;
    }
    let entry = scorecard[scorecard.length - 1];

    entry.actions = levelActionSequence.length;
    generateScorecard();
}