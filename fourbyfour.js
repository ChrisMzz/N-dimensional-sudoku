function highlightCellmates(event) {
    cell = document.getElementById(event.target.id);
    position = JSON.parse(cell.id);
    for (var i=0;i<4;i++) {
        for (var j=0;j<4;j++) {
            if (i == position[0]) {
                document.getElementById('['+i+','+String(position[1])+','+j+']').style['background-color'] = 'paleturquoise';
                document.getElementById('['+i+','+j+','+String(position[2])+']').style['background-color'] = 'lightcoral';
            } else {
                document.getElementById('['+i+','+String(position[1])+','+j+']').style['background-color'] = 'lightcyan';
                document.getElementById('['+i+','+j+','+String(position[2])+']').style['background-color'] = 'rgb(255, 210, 200)';
            }
            document.getElementById('['+i+',b,'+j+']').innerHTML = document.getElementById('['+i+','+String(position[1])+','+j+']').innerHTML;
            document.getElementById('['+i+','+j+',r]').innerHTML = document.getElementById('['+i+','+j+','+String(position[2])+']').innerHTML;
            document.getElementById('['+i+',b,'+j+']').style["font-size"] = document.getElementById('['+i+','+String(position[1])+','+j+']').style["font-size"];
            document.getElementById('['+i+','+j+',r]').style["font-size"] = document.getElementById('['+i+','+j+','+String(position[2])+']').style["font-size"];
            document.getElementById('['+i+',b,'+j+']').style["color"] = document.getElementById('['+i+','+String(position[1])+','+j+']').style["color"];
            document.getElementById('['+i+','+j+',r]').style["color"] = document.getElementById('['+i+','+j+','+String(position[2])+']').style["color"];
            
        }
        document.getElementById('['+String(position[0])+',b,'+i+']').style['background-color'] = 'paleturquoise';
        document.getElementById('['+String(position[0])+','+i+',r]').style['background-color'] = 'lightcoral';
    }
    document.getElementById('['+String(position[0])+','+String(position[1])+',r]').style['background-color'] = 'yellow';
    document.getElementById('['+String(position[0])+',b,'+String(position[2])+']').style['background-color'] = 'yellow';
    cell.style['background-color'] = 'yellow';
}

function unhighlightCellmates(event) {
    cell = document.getElementById(event.target.id);
    position = JSON.parse(cell.id);
    for (var i=0;i<4;i++) {
        for (var j=0;j<4;j++) {
            columnCell = document.getElementById('['+i+','+String(position[1])+','+j+']');
            lineCell = document.getElementById('['+i+','+j+','+String(position[2])+']');
            if (selected.includes(columnCell)) { 
                columnCell.style['background-color'] = 'yellow';
            } else {
                columnCell.style['background-color'] = '';
            }
            if (selected.includes(lineCell)) { 
                lineCell.style['background-color'] = 'yellow';
            } else {
                lineCell.style['background-color'] = '';
            }
            document.getElementById('['+i+',b,'+j+']').innerHTML = '';
            document.getElementById('['+i+','+j+',r]').innerHTML = '';
        }
        document.getElementById('['+i+','+String(position[1])+','+String(position[2])+']').style['background-color'] = '';
        document.getElementById('['+String(position[0])+',b,'+i+']').style['background-color'] = '';
        document.getElementById('['+String(position[0])+','+i+',r]').style['background-color'] = '';
    }
    document.getElementById('['+String(position[0])+','+String(position[1])+',r]').style['background-color'] = '';
    document.getElementById('['+String(position[0])+',b,'+String(position[2])+']').style['background-color'] = '';
    if (selected.includes(cell)) { 
        cell.style['background-color'] = 'yellow';
    }
    
}

function addToSelection(event) {
    cell = document.getElementById(event.target.id);
    if (selected.includes(cell)) {
        selected = selected.filter(function (e) {return e != cell});
    } else {
        selected.push(cell);
    }
    
}

function updateSelection(event) {
    console.log(event)
    if (!('1234567890'.includes(event.key)) && !('1234567890'.includes(event.code[5]))) {return}
    if (selected.length > 1) {
        for (i=0;i<selected.length;i++) {
            cell = selected[i];
            if (event.code.substring(0,5) == 'Digit') { // '25'
                if (cell.style["font-size"] == "66%" && !cell.innerHTML.includes(event.code[5])) {
                    cell.innerHTML += event.code[5];
                    ordered = cell.innerHTML.split('');
                    ordered.sort();
                    cell.innerHTML = ordered.join('');
                } else if (cell.style["font-size"] == "66%") {
                    ordered = cell.innerHTML.split('');
                    cell.innerHTML = ordered.filter(function (e) {return e != event.code[5]}).join('');
                } else {
                    cell.innerHTML = event.code[5];
                }
            } else {
                if (cell.style["font-size"] == "66%" && !cell.innerHTML.includes(event.key)) {
                    cell.innerHTML += event.key;
                    ordered = cell.innerHTML.split('');
                    ordered.sort();
                    cell.innerHTML = ordered.join('');
                } else if (cell.style["font-size"] == "66%") {
                    ordered = cell.innerHTML.split('');
                    cell.innerHTML = ordered.filter(function (e) {return e != event.key}).join('');
                } else {
                cell.innerHTML = event.key;
                }
            }
            cell.style["color"] = "green";
            cell.style["font-size"] = "66%";
        }
    } else {
        cell = selected[0];
        if (event.code.substring(0,5) == 'Digit') {
            cell.innerHTML = event.code[5];
        } else {
            cell.innerHTML = event.key;
        }
        cell.style["font-size"] = "100%";
        if ((cell.innerHTML != cell.getAttribute("solution")) && (cell.innerHTML != '0')) {cell.style["color"]="red"} else {cell.style["color"]="black"}  
    }
}

