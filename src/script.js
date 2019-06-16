;'use strict';

function gebi(id) { return document.getElementById(id) }

let tags = ""
window.onload = function() {
	document.addEventListener('keydown', keypress)
	tags = document.body.getElementsByTagName("summary")
}


const arrows = {
	up: 'ArrowUp',
	right: 'ArrowRight',
	down: 'ArrowDown',
	left: 'ArrowLeft',
}

function keypress(event) {
	if( event.key in Object.values(arrows) ) {
		console.log(event.key)


		event.preventDefault()
	}
}
