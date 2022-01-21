function getSortedItems(items, sortField, sortDirection) {
    if (sortDirection === "asc" && sortField === 'Title') {
        items.sort(function(a, b) {
      const nameA = a['Title'];
      const nameB = b['Title'];
      if (nameA < nameB) {
        return -1;
      }
      if (nameA > nameB) {
        return 1;
      }
      return 0;
    });
    }
    if(sortDirection === "asc" && sortField === 'Description'){
        items.sort(function(a, b) {
      const nameA = a['Description'];
      const nameB = b['Description'];
      if (nameA < nameB) {
        return -1;
      }
      if (nameA > nameB) {
        return 1;
      }
      return 0;
    });
    }
    if(sortDirection === "desc" && sortField === 'Title'){
        items.sort(function(a, b) {
      const nameA = a['Title'];
      const nameB = b['Title'];
      if (nameB < nameA) {
        return -1;
      }
      if (nameB > nameA) {
        return 1;
      }
      return 0;
    });
    }
    if(sortDirection === "desc" && sortField === 'Description'){
       items.sort(function(a, b) {
      const nameA = a['Description'];
      const nameB = b['Description'];
      if (nameB < nameA) {
        return -1;
      }
      if (nameB > nameA) {
        return 1;
      }
      return 0;
    });
    }
    else if(sortDirection === "asc" && sortField === 'ViewNumber'){
        items.sort(function(a, b){return a['ViewNumber'] - b['ViewNumber']})
    }
    else if(sortDirection === "asc" && sortField === 'VoteCount'){
        items.sort(function(a, b){return a['VoteCount'] - b['VoteCount']})
    }
    else if(sortDirection === "desc" && sortField === 'ViewNumber'){
        items.sort(function(a, b){return b['ViewNumber'] - a['ViewNumber']})
    }
    else if(sortDirection === "desc" && sortField === 'VoteCount'){
        items.sort(function(a, b){return b['VoteCount'] - a['VoteCount']})
    }
    return items
}

function getFilteredItems(items, filterValue) {
    const specialChar = '!'
    const results = []

    for (let i=0; i<items.length; i++) {
        if(items[i]['Title'].includes(filterValue) || items[i]['Description'].includes(filterValue)){
            results.push(items[i])
    }
        if(filterValue.substring(0, "!Description:".length) === '!Description:'){
            return items.filter(it => !it['Description'].toLowerCase().includes(filterValue.substring("!Description:".length)))
    }
        if(filterValue.substring(0, "Description:".length) === 'Description:'){
            return items.filter(it => it['Description'].toLowerCase().includes(filterValue.substring("Description:".length)))
    }
        if(filterValue[0] === specialChar){
            return items.filter(it => !it['Title'].includes(filterValue.substring(1)));
    }
    }
    return results;
}

function toggleTheme() {
        let container = document.getElementById('font');
        let color = 'black';
        if(container.style.background !== color){
            container.style.background = color
            container.style.color = 'white'
        }else{
            container.style.background = 'white'
            container.style.color = color
        }
        console.log("toggle theme")
}

function increaseFont() {
    let max = 15
    let el = document.getElementById('font');
    let fontSize = window.getComputedStyle(el, null).getPropertyValue("font-size")
    fontSize = parseFloat(fontSize);
    console.log(fontSize)
    if (fontSize < max){
        console.log(fontSize)
        el.style.fontSize = (fontSize + 2) + 'px';
    }
    console.log("increaseFont")
}


function decreaseFont() {
    let min = 3
    let element = document.getElementById('font');
    let fontSize = window.getComputedStyle(element, null).getPropertyValue("font-size")
    fontSize = parseFloat(fontSize);
    if (fontSize > min){
        element.style.fontSize = (fontSize - 2) + 'px';
    }
    console.log("decreaseFont")
}