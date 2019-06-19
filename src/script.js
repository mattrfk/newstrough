;'use strict';

let curpub = -1
let curart = -1
let pubs = undefined
let arts = undefined

let selected = undefined

let tags = ""
window.onload = function() {
	document.addEventListener('keydown', keypress)

	pubs = document.body.getElementsByClassName("source")
}

function select(e) {
	function addSelectStyle(e) {
		e.style.background = "lightgrey"
	}

	function removeSelectStyle(e) {
		e.style.background = null
	}

	if( selected !== undefined ){
		removeSelectStyle(selected)
	}
	selected = e
	addSelectStyle(selected)

	if(!isElementVisible(e)) {
		e.scrollIntoView()
	}
}

function up(){
	function pubUp() {
		if( curpub > 0 ) {
			curpub--
			if (pubs[curpub].open) {
				open(pubs[curpub])
				curart = arts.length - 1
				select(arts[curart])
			} else {
				select(pubs[curpub])
			}
		}
	}

	function artUp() {
		curart--
		select(arts[curart])
	}

	if ( curpub >= 0 && pubs[curpub].open && curart > 0 ) {
		artUp()
	} else {
		pubUp()
	}

	event.preventDefault()
}

function down() {
	function pubDown(){
		if( curpub < pubs.length - 1 ) {
			curpub++
			if (pubs[curpub].open) {
				open(pubs[curpub]) // this reinits the articles
				select(arts[curart])
			} else {
				select(pubs[curpub])
			}
		}
	}

	function artDown() {
		curart++
		select(arts[curart])
	}

	if( curpub >= 0 && pubs[curpub].open && curart < arts.length - 1 ) {
		artDown()
	} else {
		pubDown()
	}

	event.preventDefault()
}

function left() {
	if(curpub >= 0){
		pubs[curpub].open = false
		select(pubs[curpub])
		curart = -1
		arts = undefined

		event.preventDefault()
	}
}

function open(pub) {
	pub.open = true
	arts = pub.getElementsByTagName("li")
	curart = 0
}

function right() {
	if(curpub >= 0) {
		current = pubs[curpub]
		if(current) {
			// already open, so follow the link that is selected
		}

		open(current)
		select(arts[curart])
		
		event.preventDefault()
	}
}

function keypress(event) {
	switch(event.key) {
		case "k":
		case "ArrowUp":
			up()
			break
		case "j":
		case "ArrowDown":
			down()
			break
		case "h":
		case "ArrowLeft":
			left()
			break
		case "l":
		case "ArrowRight":
			right()
			break
	}
}

// https://stackoverflow.com/a/15203639/1487030
function isElementVisible(el) {
    var rect     = el.getBoundingClientRect(),
        vWidth   = window.innerWidth || doc.documentElement.clientWidth,
        vHeight  = window.innerHeight || doc.documentElement.clientHeight,
        efp      = function (x, y) { return document.elementFromPoint(x, y) };     

    // Return false if it's not in the viewport
    if (rect.right < 0 || rect.bottom < 0 
            || rect.left > vWidth || rect.top > vHeight)
        return false;

    // Return true if all of its four corners are visible
    return (
          el.contains(efp(rect.left,  rect.top))
      ||  el.contains(efp(rect.right, rect.top))
      ||  el.contains(efp(rect.right, rect.bottom))
      ||  el.contains(efp(rect.left,  rect.bottom))
    );
}
