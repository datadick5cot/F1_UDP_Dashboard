/* 
	 7 segment digit display basic example
   
   Based on wiki: https://en.wikipedia.org/wiki/Seven-segment_display
   
   Suggested improvements:
   - Simplify/improve code
   - Make reusable display class
   - Make display resizeable, moveable, skewable
   - Make a clock / Timer / StopWatch

*/


/* 
	Intialize canvas context
*/
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

/* 
	Create 7 segment array
*/
const encodings = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F];
// a - mid 1
const segA = createSegment(35,16,40,12,6,true);
// b - right 1
const segB = createSegment(78,30,12,40,8);
// c - right 2
const segC = createSegment(78,88,12,40,8);
// d - mid 3
const segD = createSegment(35,130,40,12,6,true);
// e - left 2
const segE = createSegment(20,88,12,40,8);
// f - left 1 
const segF = createSegment(20,30,12,40,8);
// g - mid 2
const segG = createSegment(35,73,40,12,6,true);

const segments = [segA,segB,segC,segD,segE,segF,segG];

doCount(ctx, segments);



/* 
	Looping counter from 0 to 10
*/
async function doCount(context, segments) {

	setAllSegments(context, segments, false);
	var count = 0;
  
	while (true) {
    applyNumber(count, context, segments);
    await wait(1000);
    if (++count > 9) {
      count = 0;
    }
  }
	setAllSegments(context, segments, false);
}


/* 
	Applies given number to segments
  uses segment hexadecimal value to AND with 1 << index places
*/
function applyNumber(number, context, segments) {
  for (let i=0; i<7; i++) {
    setSegment(context, segments[i], (encodings[number] & (1 << i)) );
  }
}

/* 
	set all segments to either ON ot OFF
*/
function setAllSegments(context, segments, isOn) {
	for(let i=0; i<segments.length; i++) {
  	setSegment(context, segments[i], isOn);
  }    
}

/* 
	creates segment and returns as Path2D object
*/
function createSegment(x,y,width,height,pointDepth,horizontal) {

    let rectangle = new Path2D();
    rectangle.rect(x, y, width, height);
    rectangle.moveTo(x, y);
    if (horizontal) {
      // left triangle
      rectangle.lineTo(x - pointDepth, y + (height/2));
      rectangle.lineTo(x, y + height);
      // right triangle
      rectangle.moveTo(x+width, y);
      rectangle.lineTo(x+width+pointDepth,y + (height/2));
      rectangle.lineTo(x+width, y+height);
    } else {
      // top triangle
      rectangle.lineTo(x + (width/2), y-pointDepth);
      rectangle.lineTo(x+width, y);
      // bottom triangle
      rectangle.moveTo(x, y+height);
      rectangle.lineTo(x + (width/2), y+height+pointDepth);
      rectangle.lineTo(x+width, y+height);
    }
    
    rectangle.closePath();
    
    return rectangle;

} 

/* 
	sets an individual segments fill color
*/
function setSegment(context, segment, isOn) {
    var offColor = '#1E1E1E';
  	var onColor = 'red';

    context.strokeStyle = offColor;
    context.stroke(segment);
    
    if ( isOn ) {
    	context.fillStyle = onColor;
   } else {
    	context.fillStyle = offColor; 
    }
    context.fill(segment);
}

/* 
	utility wait method
*/
function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
