;'use strict';

function gebi(id) { return document.getElementById(id) }

let tags = ""
window.onload = function() {
	document.addEventListener('keydown', keypress)

	pubs = document.body.getElementsByClassName("source")

	selected = -1
}

function addBorder(e) {
	for(let i = 0; i < pubs.length; i++) {
		pubs[i].style.border = "1px solid transparent"
	}

	e.style.border= "1px solid black" 
}

function up(){
	if( selected < 0 ){
		return
	}

	if( selected > 0 ) {
		selected--
		addBorder(pubs[selected])
	} 

	event.preventDefault()
}

function down() {
	if( selected < pubs.length - 1 ) {
		selected++
		addBorder(pubs[selected])
	}

	event.preventDefault()
}

function left() {
	if(selected >= 0){
		pubs[selected].open = false
		event.preventDefault()
	}
}

function right() {
	if(selected >= 0){
		pubs[selected].open = true
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
